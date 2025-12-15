# Superstore Cloud ETL Pipeline using Airflow & BigQuery

## 📌 Project Overview
This project demonstrates an end-to-end cloud-based ETL pipeline built on Google Cloud Platform.
The pipeline ingests raw sales data, cleans and transforms it using Apache Airflow, stores it in
BigQuery using a star schema, and visualizes insights using Power BI.


### Flow:
Raw CSV → Google Cloud Storage → Airflow ETL → BigQuery Data Warehouse → Power BI Dashboard

## ⚙️ Technologies Used
- Google Cloud Storage (GCS)
- Apache Airflow
- Google BigQuery
- SQL (Data Warehousing)
- Power BI
- Python (Pandas)

## 🔄 ETL Pipeline (Airflow DAG)
The Airflow DAG performs the following steps:

1. **File Detection**
   - Uses `GCSObjectExistenceSensor` to check for new files in GCS.

2. **Data Cleaning**
   - Uses `PythonOperator` to:
     - Remove duplicates
     - Handle missing values
     - Standardize column names
     - Fix date formats

3. **Load to BigQuery**
   - Uses `GCSToBigQueryOperator` to load cleaned data.

4. **Data Validation**
   - Uses `BigQueryCheckOperator` to validate successful load.

5. **Data Modeling**
   - Splits data into fact and dimension tables using SQL.

## 🗄️ Data Warehouse Design
Star schema implemented in BigQuery:

- Fact Table:
  - `fact_sales`
- Dimension Tables:
  - `dim_customer`
  - `dim_product`
  - `dim_region`
  - `dim_date`


## 📊 Power BI Dashboard
The Power BI dashboard provides insights such as:
- Sales by region
- Sales trends over time
- Top customers
- Profit by product category

Dashboard screenshots are available in `/powerbi`.

## 🚀 Automation
The entire pipeline is automated using Airflow.
Optionally, the Power BI dataset can be refreshed automatically using Power BI REST APIs
after successful DAG completion.


## 🧠 Learnings
- Cloud-native ETL design
- Workflow orchestration with Airflow
- Star schema data modeling
- Analytics-ready data pipelines

## 🔮 Future Enhancements
- Incremental loading
- Real-time ingestion using Pub/Sub
- Monitoring and alerting

