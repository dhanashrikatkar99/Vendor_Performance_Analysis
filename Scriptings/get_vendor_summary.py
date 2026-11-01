import logging
import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
from ingestion_db import ingest_db
import urllib.parse
import numpy as np

# Configure logging to write logs in append mode
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)


def get_mysql_engine():
    """Creates a SQLAlchemy engine optimized for MySQL transactions."""
    # TODO: Replace with your actual MySQL credentials and database name
    username = "root"
    raw_password = "Dhanu@999"
    safe_password = urllib.parse.quote_plus(raw_password)
    host = "localhost"
    port = "3306"
    database = "inventory"

    # MySQL connection string structure
    connection_string = (
        f"mysql+mysqlconnector://{username}:{safe_password}@{host}:{port}/{database}"
    )
    return create_engine(connection_string)


def create_vendor_summary(engine):
    """Executes an optimized CTE query to avoid temp disk errors on massive MySQL tables."""
    logging.info("Starting query execution for vendor summary table extraction...")

    # Using Common Table Expressions (CTEs) to pre-aggregate rows before joining
    # This prevents the "disk full" operational errors seen in raw nested joins
    query = """
    WITH FreightSummary AS (
        SELECT 
        VendorNumber, 
        SUM(Freight) AS Total_Freight 
    FROM vendor_invoice 
    GROUP BY VendorNumber
    ),
    PurchaseSummary AS (
        SELECT 
            p.VendorNumber,
            p.VendorName,
            p.brand,
            p.Description,
            p.PurchasePrice,
            pp.Price as ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
    JOIN purchase_prices pp
        ON p.Brand = pp.Brand
    WHERE p.PurchasePrice > 0
    GROUP BY 
        p.VendorNumber, 
        p.VendorName, 
        p.Brand, 
        p.Description,
        p.PurchasePrice, 
        pp.Volume, 
        pp.Price
    ),
    SalesSummary AS (
        SELECT
        VendorNo,
        Brand,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
    )
   SELECT
    ps.VendorNumber,
    ps.VendorName,
    ps.Brand,
    ps.Description,
    ps.PurchasePrice,
    ps.ActualPrice,
    ps.Volume,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesDollars,
    ss.TotalSalesPrice,
    ss.TotalExciseTax,
    fs.Total_Freight AS FreightCost
FROM PurchaseSummary ps
LEFT JOIN SalesSummary ss
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
LEFT JOIN FreightSummary fs
    ON ps.VendorNumber = fs.VendorNumber
ORDER BY ps.TotalPurchaseDollars DESC;"""

    df = pd.read_sql_query(query, engine)
    logging.info(
        f"Successfully extracted {len(df)} rows from base tables. Preview:\n{df.head().to_string()}"
    )
    return df


def clean_data(df):
    """Cleans up data frames, updates typing schemas, and engineers analytical features."""
    logging.info("Initiating data cleaning and categorical corrections...")

    # Convert volume to float securely
    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").astype(
            "float64"
        )

    # Fill un-sold or un-purchased metric holes with zero values
    fill_cols = [
        "TotalSalesQuantity",
        "TotalSalesDollars",
        "TotalPurchaseQuantity",
        "TotalPurchaseDollars",
        "TotalSalesPrice",
        "TotalExciseTax"
    ]
    df[fill_cols] = df[fill_cols].fillna(0)

    # Clean whitespace variances often present in raw string databases
    if "VendorName" in df.columns:
        df["VendorName"] = df["VendorName"].astype(str).str.strip()

    logging.info("Engineering analytical KPIs (Margins, Turnovers)...")

    # Feature Engineering Formulas
    df["GrossProfit"] = df["TotalSalesDollars"] - df["TotalPurchaseDollars"]

   # FIX: Using np.select guarantees true mathematical protection against infinity (-inf/inf) exceptions
    df["ProfitMargin"] = np.select(
        [df["TotalSalesDollars"] == 0], 
        [0.0], 
        default=(df["GrossProfit"] / df["TotalSalesDollars"]) * 100
    )

    df["StockTurnover"] = np.select(
        [df["TotalPurchaseQuantity"] == 0], 
        [0.0], 
        default=df["TotalSalesQuantity"] / df["TotalPurchaseQuantity"]
    )
    
    df["SalestoPurchaseRatio"] = np.select(
        [df["TotalPurchaseDollars"] == 0], 
        [0.0], 
        default=df["TotalSalesDollars"] / df["TotalPurchaseDollars"]
    )

    logging.info(
        f"Cleaning phase finished. Structured dataframe summary:\n{df.head().to_string()}"
    )
    return df





if __name__ == "__main__":
    # Initialize connection pipeline engine
    mysql_engine = get_mysql_engine()

    # Step 1: Extract summary aggregates across massive logs
    summary_df = create_vendor_summary(mysql_engine)

    # Step 2: Clean metrics and build feature models
    cleaned_df = clean_data(summary_df)

    # Step 3: Insert final master back to MySQL server
    ingest_db(cleaned_df, "vendor_sales_summary", mysql_engine)
    logging.info("Database ingestion pipeline execution completed successfully.")
