# Retail-Sales-Data-Pipeline-Analytics
retail_sales_pipeline
retail_sales_pipeline/
├── data/
│   └── raw/             # To store generated raw sales data (CSV)
├── dags/
│   └── retail_sales_dag.py # Airflow DAG definition
├── scripts/
│   ├── generate_sales_data.py # Script to generate dummy sales data
│   ├── ingest_data_to_postgres.py # Script to load CSV to raw DB
│   └── transform_load_dwh.py  # Script for transformations and loading DWH
├── sql/
│   ├── create_raw_tables.sql # SQL for creating raw tables
│   ├── create_dwh_tables.sql # SQL for creating DWH tables (dimension/fact)
│   └── dwh_queries.sql     # Example analytical queries
├── docker-compose.yml       # Docker Compose file for Airflow & Postgres
├── Dockerfile.airflow       # Custom Dockerfile for Airflow
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation (this file)
