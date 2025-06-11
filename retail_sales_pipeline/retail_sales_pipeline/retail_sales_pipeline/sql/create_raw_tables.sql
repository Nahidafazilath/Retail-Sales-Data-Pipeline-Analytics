-- raw_sales table: stores raw ingested data
CREATE TABLE IF NOT EXISTS raw_sales (
    sale_id VARCHAR(50) PRIMARY KEY,
    transaction_date DATE,
    product_id VARCHAR(50),
    product_name VARCHAR(255),
    category VARCHAR(100),
    price DECIMAL(10, 2),
    quantity INT,
    customer_id VARCHAR(50),
    customer_name VARCHAR(255),
    region VARCHAR(100)
);
