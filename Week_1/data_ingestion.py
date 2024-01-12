import os
from time import time
import urllib.request
import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import psycopg2

#################################################
### SECTION 1: Setup and Download the Dataset ###
#################################################

# Create the directory if it doesn't exist
os.makedirs("ny_taxi", exist_ok=True)

# URL of the dataset
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

# Download the dataset
urllib.request.urlretrieve(url, "ny_taxi/yellow_tripdata_2023-01.parquet")

print("Dataset downloaded successfully!")


###################################
### SECTION 2: Load the dataset ###
###################################

# Columns
needed_columns = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "tip_amount",
    "tolls_amount",
    "total_amount"
]

# Read the parquet file
parquet_file = pq.ParquetFile("ny_taxi/yellow_tripdata_2023-01.parquet")
df = pd.read_parquet("ny_taxi/yellow_tripdata_2023-01.parquet")


################################################
### SECTION 3: Setup the database connection ###
################################################

# Connect to database
conn = psycopg2.connect(
    host="pgdatabase",
    port="5432",
    database="db-name",
    user="db-user",
    password="db-password"
)

# Set autocommit to true
conn.autocommit = True

# Use existing psycopg2 connection to create engine
engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)


####################################################
### SECTION 4: Ingest the dataset into postgres ###
####################################################

# Start total ingestion time timer
t_start = time()

# Ingest the data to the database a chunk at a time
for batch in parquet_file.iter_batches(batch_size=100000, columns=needed_columns):
    # Start batch timer
    b_start = time()

    batch_df = batch.to_pandas()

    # Rename columns
    new_column_names = {
        "VendorID": "vendor_id",
        "tpep_pickup_datetime": "pickup_datetime",
        "tpep_dropoff_datetime": "dropoff_datetime",
        "RatecodeID": "rate_code",
        "PULocationID": "pickup_location",
        "DOLocationID": "dropoff_location",
    }

    batch_df = batch_df.rename(columns=new_column_names)

    # Drop rows with missing values
    df = batch_df.dropna()

    # Drop rows with invalid values
    df = df[df['pickup_datetime'].dt.year == 2023]
    df = df[df['dropoff_datetime'].dt.year == 2023]

    df = df[df['pickup_datetime'].dt.month == 1]
    df = df[df['dropoff_datetime'].dt.month == 1]

    with engine.begin() as conn:
        # Ingest the data to the database
        df.to_sql(name='ny_yellow_taxi', schema="de_zoom_camp", con=conn, if_exists='append', index=False)

    # End batch timer
    b_end = time()
    print('inserted another chunk, took %.3f second' % (b_end - b_start))

    print('inserted another chunk, took %.3f second' % (b_end - b_start))

# End total ingestion time timer
t_end = time()
print("Finished ingesting data into the postgres database, it took %.3f seconds" % (t_end - t_start))


##########################
### SECTION 5: Cleanup ###
##########################

# Close the connection
conn.close()

# Delete the dataset
os.remove("ny_taxi/yellow_tripdata_2023-01.parquet")