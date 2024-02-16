from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action
from pandas import DataFrame, to_datetime

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def execute_transformer_action(df: DataFrame, *args, **kwargs) -> DataFrame:
    """
    Execute Transformer Action: ActionType.REMOVE

    Docs: https://docs.mage.ai/guides/transformer-blocks#remove-columns
    """
    action_one = build_transformer_action(
        df,
        action_type=ActionType.REMOVE,
        arguments=['extra', 'mat_tax', 'ehail_fee', 'improvement_surcharge', 'congestion_surcharge'],
        axis=Axis.COLUMN,
    )

    df = BaseAction(action_one).execute(df)

    # Rename columns
    new_column_names = {
        "VendorID": "vendor_id",
        "lpep_pickup_datetime": "pickup_datetime",
        "lpep_dropoff_datetime": "dropoff_datetime",
        "RatecodeID": "rate_code_id",
        "PULocationID": "pickup_location",
        "DOLocationID": "dropoff_location",
    }

    df = df.rename(columns=new_column_names)

    month = kwargs.get("month")
    year = kwargs.get("year")

    # Drop rows with invalid values
    df = df[df['pickup_datetime'].dt.year == year]
    df = df[df['dropoff_datetime'].dt.year == year]

    df = df[df['pickup_datetime'].dt.month == month]
    df = df[df['dropoff_datetime'].dt.month == month]

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
