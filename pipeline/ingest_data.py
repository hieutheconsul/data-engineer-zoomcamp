#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm


# =========================
# Configuration
# =========================

YEAR = 2021
MONTH = 1

DATA_PREFIX = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/"
FILE_URL = f"{DATA_PREFIX}yellow_tripdata_{YEAR}-{MONTH:02d}.csv.gz"

# PostgreSQL connection
PG_USER = "root"
PG_PASS = "root"
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "ny_taxi"

TABLE_NAME = "yellow_taxi_data"

CHUNK_SIZE = 100000


# =========================
# Data schema
# =========================

DTYPE = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
}

PARSE_DATES = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# =========================
# Database connection
# =========================

def get_engine():
    connection_str = (
        f"postgresql+psycopg://{PG_USER}:{PG_PASS}"
        f"@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )
    engine = create_engine(connection_str)
    return engine


# =========================
# Load data in chunks
# =========================

def load_data(engine):

    df_iter = pd.read_csv(
        FILE_URL,
        dtype=DTYPE,
        parse_dates=PARSE_DATES,
        iterator=True,
        chunksize=CHUNK_SIZE
    )

    for df_chunk in tqdm(df_iter, desc="Loading chunks"):

        df_chunk.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists="append",
            index=False
        )


# =========================
# Main pipeline
# =========================

def main():

    print("Starting pipeline...")

    engine = get_engine()

    print("Connected to PostgreSQL")

    load_data(engine)

    print("Pipeline completed")


# =========================
# Script entrypoint
# =========================

if __name__ == "__main__":
    main()