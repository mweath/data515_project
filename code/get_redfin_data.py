import pandas as pd
import requests
import io
import os

def get_data():
    try:
        return get_data_from_Redfin()
    except ValueError:
        return get_data_from_file()

def get_data_from_file():
    current_path = os.getcwd()
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
    data_path = os.path.join(parent_path, "data")
    redfin_path = os.path.join(data_path,"redfin")
    file_path = os.path.join(redfin_path, "All_King_Redfin.csv")
    df = pd.read_csv(file_path)
    return df

def get_data_from_Redfin():
    all_king_url = "https://www.redfin.com/stingray/api/gis-csv?al=1&cluster_bounds=-123.04941%2046.84777%2C-121.01694%2046.84777%2C-121.01694%2047.92442%2C-123.04941%2047.92442%2C-123.04941%2046.84777&market=seattle&min_stories=1&num_homes=5000&ord=redfin-recommended-asc&page_number=1&region_id=118&region_type=5&sf=1,2,3,5,6,7&status=1&uipt=1,2,3,4,5,6&v=8"
    urlData = requests.get(all_king_url).content
    if "spam bot" in str(urlData):
        raise ValueError("Redfin api error")
    else:
        return pd.read_csv(io.StringIO(urlData.decode('utf-8')))
