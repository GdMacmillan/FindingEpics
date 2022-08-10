import os
import zipfile
import pandas as pd
from urllib import request

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

URL = "https://simplemaps.com/static/data/us-cities/1.75/basic/simplemaps_uscities_basicv1.75.zip"
DATA_DIR = "city_data"
DATABASE_PATH = os.path.join(ROOT, DATA_DIR)


def download_and_extract():
    os.makedirs(DATABASE_PATH, exist_ok=True)

    data_store_raw = os.path.join(DATABASE_PATH, "uscities.zip")
    if not os.path.exists(data_store_raw):
        request.urlretrieve(URL, data_store_raw)

    with zipfile.ZipFile(data_store_raw, 'r') as zf:
        zf.extractall(DATABASE_PATH)

def load():
    data_store = os.path.join(DATABASE_PATH, "uscities.csv")
    if os.path.exists(data_store):
        df = pd.read_csv(data_store)
        return df
    else:
        raise Exception('city data not loaded. Did you try download_and_extract()?')

if __name__ == "__main__":
    download_and_extract()