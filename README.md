# Retail Sales Data Pipeline & Analytics

## Project Overview

This project demonstrates an end-to-end data engineering pipeline for processing retail sales data. It covers data ingestion, transformation, storage in a data warehouse, and preparation for analytical queries. The goal is to provide insights into sales trends, product performance, and customer behavior.

## Problem Statement

A hypothetical retail company needs to analyze its daily sales transactions to understand key metrics such as total sales, sales by product category, sales by region, and customer purchasing patterns. The current process is manual and inefficient, leading to delayed insights. We aim to automate this process to enable timely and effective business decisions.

## Key Features

* **Automated Data Ingestion:** Simulate ingesting daily sales data.
* **Data Transformation:** Clean, normalize, and enrich raw sales data.
* **Data Warehousing:** Store transformed data in a structured manner for analytical queries.
* **Data Modeling:** Implement a star schema for efficient reporting.
* **Workflow Orchestration:** Automate the entire pipeline using Apache Airflow.
* **Containerization:** Package the pipeline components for easy deployment and reproducibility using Docker.

## Technology Stack

* **Programming Language:** Python 3.9+
* **Data Ingestion (Simulation):** Python (`Faker`, `random`)
* **Raw Data Storage:** Local CSV files (simulated by `data/raw/` directory)
* **Data Processing/Transformation:** Pandas
* **Data Warehouse:** PostgreSQL (running in Docker)
* **Workflow Orchestration:** Apache Airflow (running in Docker)
* **Containerization:** Docker, Docker Compose
* **Version Control:** Git, GitHub

## Project Architecture

```mermaid
graph TD
    A[Simulated Sales Data Generation] --> B(Raw Sales CSVs);
    B --> C{Airflow DAG: Ingest Raw Data};
    C --> D[PostgreSQL: Raw Layer];
    D --> E{Airflow DAG: Transform & Load};
    E --> F[PostgreSQL: Data Warehouse Layer];
    F --> G[BI Tool (Conceptual/Future Step)];

    subgraph Orchestration
        C
        E
    end

    subgraph Data Stores
        B
        D
        F
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#bbf,stroke:#333,stroke-width:2px
    style D fill:#bbf,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f9f,stroke:#333,stroke-width:2px
