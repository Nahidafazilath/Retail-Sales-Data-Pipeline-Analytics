import pandas as pd
import psycopg2
from psycopg2 import extras
import os
from datetime import datetime

def ingest_csv_to_postgres(file_path):
    try:
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST", "localhost"),
            database=os.getenv("PG_DB", "retail_db"),
            user=os.getenv("PG_USER", "user"),
            password=os.getenv("PG_PASSWORD", "password")
        )
        cur = conn.cursor()

        # Create table if not exists (run DDL from SQL file)
        with open('../sql/create_raw_tables.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()

        df = pd.read_csv(file_path)

        # Convert to list of tuples for executemany
        # Ensure column order matches your table schema
        records = [tuple(row) for row in df[['sale_id', 'transaction_date', 'product_id',
                                            'product_name', 'category', 'price',
                                            'quantity', 'customer_id', 'customer_name', 'region']].values]

        insert_sql = """
        INSERT INTO raw_sales (sale_id, transaction_date, product_id, product_name,
                            category, price, quantity, customer_id, customer_name, region)
        VALUES %s
        ON CONFLICT (sale_id) DO NOTHING; -- Handle potential duplicates gracefully
        """
        extras.execute_values(cur, insert_sql, records)
        conn.commit()
        print(f"Successfully ingested {len(records)} records from {file_path} into raw_sales.")

    except Exception as e:
        print(f"Error ingesting data: {e}")
        raise
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    # This script will be called by Airflow, passing the file_path
    # For local testing, you might run it with a dummy path:
    # ingest_csv_to_postgres('../data/raw/sales_data_20240101.csv')
    pass # Airflow will provide the file path
