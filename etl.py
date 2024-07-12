# Import libraries
import pyodbc
import pandas as pd
import os
from sqlalchemy import create_engine

# SQL Server database details
driver = "{ODBC Driver 17 for SQL Server}"
server = "localhost\\SQLEXPRESS"
database = "AdventureWorksDW2019"

# Function to extract data from SQL Server
def extract():
    try:
        # Establish connection to SQL Server
        connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        src_conn = pyodbc.connect(connection_string)
        print("Koneksi berhasil:", src_conn)
        src_cursor = src_conn.cursor()

        # Query to get table names
        src_cursor.execute("""
            SELECT t.name AS table_name
            FROM sys.tables t
            WHERE t.name IN ('DimProduct', 'DimProductSubcategory', 'DimProductCategory', 'DimSalesTerritory', 'FactInternetSales')
        """)

        # Fetch all table names
        src_tables = src_cursor.fetchall()

        # Iterate through each table and extract data
        for tbl in src_tables:
            table_name = tbl.table_name
            df = pd.read_sql_query(f'SELECT * FROM {table_name}', src_conn)
            load(df, table_name)

    except Exception as e:
        print("Data extract error:", e)
    finally:
        if 'src_conn' in locals():
            src_conn.close()

# Function to load data into PostgreSQL
def load(df, table_name):
    try:
        # Establish connection to PostgreSQL
        uid = 'postgres'  # Ganti dengan nama pengguna PostgreSQL Anda
        pwd = 'admin'  # Ganti dengan kata sandi PostgreSQL Anda
        engine = create_engine(f'postgresql://{uid}:{pwd}@localhost:5432/postgres')

        # # Save DataFrame to PostgreSQL
        # df.to_sql(name=f'stg_{table_name}', con=engine, if_exists='replace', index=False)
        # print(f"Data imported successfully for table {table_name}")

         # Save DataFrame to PostgreSQL with specified schema
        df.to_sql(name=f'stg_{table_name}', con=engine, if_exists='replace', index=False, schema="adventureworks2019(au)")
        print(f"Data imported successfully for table {table_name}")

    except Exception as e:
        print("Data load error:", e)

# Main function to run extract and load
def main():
    try:
        extract()
    except Exception as e:
        print("Error while extracting and loading data:", e)

if __name__ == "__main__":
    main()
