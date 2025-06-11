-- Total sales by product category
SELECT
    dp.category,
    SUM(fs.total_sales) AS total_revenue
FROM fact_sales fs
JOIN dim_product dp ON fs.product_key = dp.product_key
GROUP BY dp.category
ORDER BY total_revenue DESC;

-- Daily sales trend
SELECT
    dd.full_date,
    SUM(fs.total_sales) AS daily_revenue
FROM fact_sales fs
JOIN dim_date dd ON fs.date_key = dd.date_key
GROUP BY dd.full_date
ORDER BY dd.full_date;

-- Top 5 customers by sales
SELECT
    dc.customer_name,
    SUM(fs.total_sales) AS total_spent
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_key = dc.customer_key
GROUP BY dc.customer_name
ORDER BY total_spent DESC
LIMIT 5;
