from airflow.sdk import dag, task, asset
from pendulum import datetime
import os
from assets_12 import asset_fetch_data

@asset(
    schedule=asset_fetch_data,
    #This is optional but good to include for clarity about the asset's destination
    uri="/opt/airflow/logs/data/data_process.txt",
    name="asset_process_data"
)

def process_data(self):

    #Ensure the directory exists
    os.makedirs(os.path.dirname(self.uri), exist_ok=True)

    #Simulate data fetching by writing to a file
    with open(self.uri, 'w') as f:
        f.write(f"Data processed successfully")

    print(f"Data processed to {self.uri}")