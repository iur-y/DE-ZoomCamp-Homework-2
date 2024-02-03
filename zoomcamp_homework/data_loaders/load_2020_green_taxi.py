import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    base_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/"\
    "download/green/green_tripdata_2020-PLACEHOLDER.csv.gz"

    # The PLACEHOLDER requires leading zeros for months
    months = [f"{month:02}" for month in range(10, 13)]

    # Initialize empty DataFrame for concatenation
    df = pd.DataFrame()

    for month in months:
        url = base_url.replace("PLACEHOLDER", month)
        response = requests.get(url)
        
        temp_df = pd.read_csv(io.BytesIO(response.content), sep=',', compression="gzip")
        df = pd.concat([df, temp_df], axis=0, ignore_index=True)

    return df


@test
def test_output(df, *args) -> None:
    assert df is not None, 'The output is undefined'

@test
def test_shape(df) -> None:
    assert df.shape != (0, 0), 'The dataframe has no rows'
