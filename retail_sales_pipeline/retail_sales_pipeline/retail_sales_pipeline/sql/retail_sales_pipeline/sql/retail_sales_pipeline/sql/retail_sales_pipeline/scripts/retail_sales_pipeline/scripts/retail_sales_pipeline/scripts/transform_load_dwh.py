import pandas as pd
import psycopg2
from psycopg2 import extras
import os
from datetime import datetime

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        database=os.getenv("PG_DB", "retail_db"),
        user=os.getenv("PG_USER", "user"),
        password=os.getenv("PG_PASSWORD", "password")
    )

def load_dim_date(cur, conn):
    print("Loading dim_date...")
    # Generate dates up to today, assuming data won't be from the future
    dates_df = pd.DataFrame(
        pd.date_range(start='2023-01-01', end=datetime.now().strftime('%Y-%m-%d'), freq='D')
    )
    dates_df.columns = ['full_date']
    dates_df['date_key'] = dates_df['full_date'].dt.strftime('%Y%m%d').astype(int)
    dates_df['day_of_week'] = dates_df['full_date'].dt.dayofweek + 1
    dates_df['day_name'] = dates_df['full_date'].dt.day_name()
    dates_df['day_of_month'] = dates_df['full_date'].dt.day
    dates_df['month'] = dates_df['full_date'].dt.month
    dates_df['month_name'] = dates_df['full_date'].dt.month_name()
    dates_df['quarter'] = dates_df['full_date'].dt.quarter
    dates_df['year'] = dates_df['full_date'].dt.year

    records = [tuple(row) for row in dates_df[[
        'date_key', 'full_date', 'day_of_week', 'day_name', 'day_of_month',
        'month', 'month_name', 'quarter', 'year'
    ]].values]

    insert_sql = """
    INSERT INTO dim_date (date_key, full_date, day_of_week, day_name, day_of_month,
                          month, month_name, quarter, year)
    VALUES %s
    ON CONFLICT (date_key) DO NOTHING;
    """
    extras.execute_values(cur, insert_sql, records)
    conn.commit()
    print("dim_date loaded.")


def transform_and_load_dwh():
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # 1. Create DWH tables if not exists
        with open('../sql/create_dwh_tables.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()

        # 2. Load Dimension Tables
        load_dim_date(cur, conn)

        print("Loading dim_product...")
        cur.execute("""
            INSERT INTO dim_product (product_key, product_name, category)
            SELECT DISTINCT product_id, product_name, category
            FROM raw_sales
            ON CONFLICT (product_key) DO UPDATE SET
                product_name = EXCLUDED.product_name,
                category = EXCLUDED.category;
        """)
        conn.commit()
        print("dim_product loaded.")

        print("Loading dim_customer...")
        cur.execute("""
            INSERT INTO dim_customer (customer_key, customer_name)
            SELECT DISTINCT customer_id, customer_name
            FROM raw_sales
            ON CONFLICT (customer_key) DO UPDATE SET
                customer_name = EXCLUDED.customer_name;
        """)
        conn.commit()
        print("dim_customer loaded.")

        print("Loading dim_region...")
        cur.execute("""
            INSERT INTO dim_region (region_key, region_name)
            SELECT DISTINCT region, region
            FROM raw_sales
            ON CONFLICT (region_key) DO NOTHING;
        """)
        conn.commit()
        print("dim_region loaded.")


        # 3. Load Fact Table
        print("Loading fact_sales...")
        # Use transaction_date to filter for recent data, preventing re-processing all raw data
        # Adjust this logic if you have complex CDC (Change Data Capture) requirements
        cur.execute("""
            INSERT INTO fact_sales (date_key, product_key, customer_key, region_key,
                                    sale_id, quantity_sold, unit_price, total_sales)
            SELECT
                TO_CHAR(rs.transaction_date, 'YYYYMMDD')::INT AS date_key,
                rs.product_id AS product_key,
                rs.customer_id AS customer_key,
                rs.region AS region_key,
                rs.sale_id,
                rs.quantity,
                rs.price,
                rs.quantity * rs.price AS total_sales
            FROM raw_sales rs
            WHERE NOT EXISTS (SELECT 1 FROM fact_sales fs WHERE fs.sale_id = rs.sale_id);
            -- This ensures only new sales are inserted.
            -- For updates to existing sales, you'd need a more complex strategy (e.g., SCD Type 2 or upserts on fact table).
        """)
        conn.commit()
        print("fact_sales loaded.")

    except Exception as e:
        print(f"Error transforming and loading DWH: {e}")
        raise
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    transform_and_load_dwh()
