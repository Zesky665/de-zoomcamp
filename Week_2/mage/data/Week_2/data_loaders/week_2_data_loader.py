from mage_ai.io.file import FileIO
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd


@data_loader
def load_data_from_file(*args, **kwargs):
    """
    Template for loading data from filesystem.
    Load data from 1 file or multiple file directories.

    For multiple directories, use the following:
        FileIO().load(file_directories=['dir_1', 'dir_2'])

    Docs: https://docs.mage.ai/design/data-loading#fileio
    """
    month = kwargs.get("month")
    year = kwargs.get("year")

    date = f'{year}-{month}'
    print(date)

    url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_{date}.csv.gz'

    taxi_dtypes = {
        'VendorID': float,
        'store_and_fwd_flag': str,
        'RatecodeID': float,
        'PULocationID': float,
        'DOLocationID': float,
        'passenger_count': float,
        'trip_distance': float,
        'fare_amount': float,
        'extra': float,
        'mta_tax': float,
        'tip_amount': float,
        'tolls_amount': float,
        'ehail_fee': float,
        'improvement_surcharge': float,
        'total_amount': float,
        'payment_type': float,
        'trip_type': float,
        'congestion_surcharge': float
    }

    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    df = pd.read_csv(url, sep=',', compression='gzip', parse_dates=parse_dates)
    df = df.astype(taxi_dtypes)

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
