import os
import urllib.request

# Create the directory if it doesn't exist
os.makedirs("ny_taxi", exist_ok=True)

# URL of the dataset
url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"

# Download the dataset
urllib.request.urlretrieve(url, "ny_taxi/yellow_tripdata_2019-01.parquet")

print("Dataset downloaded successfully!")
