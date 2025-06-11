-- Dimension Tables
CREATE TABLE IF NOT EXISTS dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE,
    day_of_week INT,
    day_name VARCHAR(10),
    day_of_month INT,
    month INT,
    month_name VARCHAR(10),
    quarter INT,
    year INT
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_key VARCHAR(50) PRIMARY KEY, -- Using product_id as key for simplicity
    product_name VARCHAR(255),
    category VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_key VARCHAR(50) PRIMARY KEY, -- Using customer_id as key
    customer_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_key VARCHAR(100) PRIMARY KEY, -- Using region name as key
    region_name VARCHAR(100)
);

-- Fact Table
CREATE TABLE IF NOT EXISTS fact_sales (
    sale_key SERIAL PRIMARY KEY,
    date_key INT REFERENCES dim_date(date_key),
    product_key VARCHAR(50) REFERENCES dim_product(product_key),
    customer_key VARCHAR(50) REFERENCES dim_customer(customer_key),
    region_key VARCHAR(100) REFERENCES dim_region(region_key),
    sale_id VARCHAR(50) UNIQUE, -- To link back to raw if needed
    quantity_sold INT,
    unit_price DECIMAL(10, 2),
    total_sales DECIMAL(10, 2)
);
