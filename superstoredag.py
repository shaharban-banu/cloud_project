import datetime  
import pandas as pd  
from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor 
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator 
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator  
from airflow.operators.python import PythonOperator
from google.cloud import storage  



BUCKET='sales-bucket-super'
RAW_FILE='raw/Sample - Superstore.csv'
CLEANED_FILE='cleaned/Superstore_clean.csv'
BQ_DATASET='superstore_dw'

def clean_sales_data():
    client=storage.Client()
    bucket=client.bucket(BUCKET)

    blob=bucket.blob(RAW_FILE)
    blob.download_to_filename('/tmp/superstore.csv')

    df=pd.read_csv('/tmp/superstore.csv',encoding='cp1252')

    df.columns=df.columns.str.strip().str.lower().str.replace(' ','_')
    df.drop_duplicates(subset=['order_id'],inplace=True)
    df['order_date']=pd.to_datetime(df['order_date'])
    df['ship_date']=pd.to_datetime(df['ship_date'])
    df['postal_code'].fillna('Unknown',inplace=True)
    df.dropna(subset=['order_id','sales','profit'],inplace=True)
    

    df.to_csv('/tmp/superstore_clean.csv',index=False)

    clean_blob=bucket.blob(CLEANED_FILE)
    clean_blob.upload_from_filename('/tmp/superstore_clean.csv')

default_args={
    'start_date':datetime.datetime(2025,11,1),
    'retries':1,
}

with DAG(
    dag_id='superstore-etl-dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    description='ETL pipeline for superstore data in GCP',
) as dag:
    
    check_file=GCSObjectExistenceSensor(
        task_id='check_file',
        bucket=BUCKET,
        object=RAW_FILE,
        poke_interval=30,
        timeout=300,
        )
    
    clean_data = PythonOperator(
        task_id="clean_data",
        python_callable=clean_sales_data
    )

    load_file= GCSToBigQueryOperator(
        task_id='load_file',
        bucket=BUCKET,
        source_objects=[CLEANED_FILE],
        destination_project_dataset_table='final-project-etl.superstore_dw.sales_data',
        source_format='CSV',
        skip_leading_rows=1,
        write_disposition='WRITE_TRUNCATE',
        autodetect=True
       
        )
    validate_bq=BigQueryCheckOperator(
        task_id='validate_bq',
        sql="select count(*)>0 from `final-project-etl.superstore_dw.sales_data`",
        use_legacy_sql=False,
        
        )
    
    check_file>>clean_data>>load_file>>validate_bq

