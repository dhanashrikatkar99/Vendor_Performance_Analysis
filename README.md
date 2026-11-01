# 📊 Vendor Performance Analysis

An end-to-end data analytics project focused on evaluating vendor performance, inventory efficiency, purchasing patterns, and profitability to derive actionable business insights.

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Business Problem & Objectives](#-business-problem--objectives)
3. [Tools & Technologies](#-tools--technologies)
4. [Dataset Description](#-dataset-description)
5. [Project Workflow](#-project-workflow)
6. [How to Run the Project](#-how-to-run-the-project)


---

## 📌 Project Overview

Vendor Performance Analysis is a data analytics project that examines sales transactions, purchasing activities, inventory levels, and vendor contributions to understand business performance.

The project focuses on identifying profitable and underperforming brands, evaluating vendor contribution, analyzing bulk purchasing benefits, and identifying slow-moving inventory.

Using Python for data ingestion and analysis and MySQL for data storage and querying, the project transforms multiple raw CSV datasets into meaningful business insights.

**The ultimate goal is to support data-driven decisions related to vendor management, pricing strategies, inventory optimization, and profitability improvement.**

## 🎯 Business Problem & Objectives

Businesses in the retail and wholesale industry often face challenges related to inventory management, vendor dependency, pricing inefficiencies, and inconsistent profitability.

This analysis addresses the following business questions:

- Which brands have low sales but high profit margins and may benefit from promotional strategies?
- Which vendors contribute the most to total purchases and sales?
- Does bulk purchasing result in lower unit purchase costs?
- Which vendors have slow-moving inventory and high unsold inventory value?
- How do profit margins differ between top-performing and low-performing vendors?
- Are the observed differences in vendor profitability statistically significant?

## 🛠️ Tools & Technologies

| Tool / Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | CSV processing and data manipulation |
| SQLAlchemy | Database connectivity and data ingestion |
| MySQL | Data storage and querying |
| MySQL Workbench | Database management and SQL execution |
| Matplotlib / Visualization libraries | Data visualization |
| Jupyter Notebook | Analysis environment (if used) |
| Git & GitHub | Version control and project documentation |

## 📂 Dataset Description

The analysis uses CSV datasets containing information about inventory, purchases, sales, product pricing, and vendor invoices.

| Dataset | Description |
|---|---|
| `begin_inventory.csv` | Opening inventory information |
| `end_inventory.csv` | Closing inventory information |
| `purchase_prices.csv` | Product purchase price information |
| `purchases.csv` | Purchase transaction records |
| `sales.csv` | Sales transaction records |
| `vendor_invoice.csv` | Vendor invoice and freight cost information |

The datasets are processed using Python and loaded into MySQL for structured storage and further analysis.

The datasets used in this project are obtained from Kaggle:

[Vendor Performance Analysis – Kaggle](https://www.kaggle.com/datasets/harshmadhavan/vendor-performance-analysis)

## ⚙️ Project Workflow

The project follows a structured data analytics workflow:

1. **Data Ingestion**
   - Read multiple CSV files using Python and Pandas.
   - Process large datasets using chunk-based ingestion.
   - Establish database connectivity using SQLAlchemy.
   - Load the datasets into MySQL tables.

2. **Data Preparation**
   - Examine data distributions and summary statistics.
   - Identify negative, zero, and inconsistent values.
   - Investigate extreme values and potential data quality issues.
   - Apply the filtering criteria documented in the analysis.

3. **Exploratory Data Analysis (EDA)**
   - Analyze numerical distributions and descriptive statistics.
   - Investigate outliers and correlations.
   - Examine purchase and sales patterns.

4. **Business Analysis**
   - Evaluate brand-level performance.
   - Identify major vendor contributions.
   - Analyze bulk purchasing and unit costs.
   - Investigate unsold inventory.
   - Compare vendor profitability.

5. **Statistical Analysis**
   - Calculate confidence intervals for vendor profit margins.
   - Perform hypothesis testing to evaluate differences between vendor groups.

6. **Insights & Recommendations**
   - Translate analytical findings into business recommendations.
   - Identify opportunities for better pricing, vendor diversification, and inventory management.




## 🚀 How to Run the Project

### Prerequisites

- Python 3.x
- MySQL Server
- MySQL Workbench (optional)
- Git

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Vendor-Performance-Analysis
```
### 2. Usage

- Download the dataset from Kaggle (see Dataset section).
- Use scripts/ for Python-based analysis or open vendor_Performance.pbix in Power BI.
- Explore interactive dashboards to gain actionable insights on vendor performance.



## 👩‍💻 Author

**Dhanashri Katkar**

Computer Engineering Graduate | Aspiring Data Analyst

[LinkedIn](https://www.linkedin.com/in/dhanashri-katkar-b15a3b290/)
