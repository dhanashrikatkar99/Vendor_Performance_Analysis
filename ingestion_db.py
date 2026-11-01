import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time
import urllib.parse

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

raw_password = "Dhanu@999"
safe_password = urllib.parse.quote_plus(raw_password)
engine =create_engine(f'mysql+pymysql://root:{safe_password}@localhost:3306/inventory')

# def ingest_db(df, table_name, engine):
#     '''this function will ingest the dataframe into database table'''
#     df.to_sql(table_name, con = engine, if_exists = 'replace', index = False)

def ingest_db(df, table_name, engine):
    '''this function will ingest the dataframe into database table'''
    # Set chunksize (e.g., 10,000 or 20,000 rows at a time) to prevent MemoryError
    df.to_sql(
        table_name, 
        con=engine, 
        if_exists='replace', 
        index=False, 
        chunksize=10000
    )

def load_raw_data():
    '''this function will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df = pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            ingest_db(df, file[:-4], engine)
    end = time.time()
    total_time = (end - start)/60
    logging.info('---------------------Ingestion Complete---------------------')
    
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ == '__main__':
    load_raw_data()
 