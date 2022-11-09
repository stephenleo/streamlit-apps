import json

import pandas as pd
import requests
from loguru import logger
from tqdm import tqdm

url = "https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3"


def download_all_data(step: int = 100) -> pd.DataFrame:

    logger.info("Get Total Rows")
    total_rows = requests.get(f"{url}&limit=1").json()["result"]["total"]
    logger.info(f"{total_rows = }")

    logger.info("Begin Downloading")
    records = []
    for start_row in tqdm(range(0, total_rows, step)):
        offset_url = f"{url}&limit={step}&offset={start_row}"
        records.extend(requests.get(offset_url).json()["result"]["records"])

    logger.info("Convert to Dataframe")

    return pd.DataFrame(records)


def calc_unique_categories(df: pd.DataFrame) -> dict:
    logger.info("Calc custom fields")
    df["sold_year"] = df["month"].str.split("-").str[0].astype(int)
    df["address"] = df["block"] + " " + df["street_name"]

    logger.info("Calc unique categories")
    return {
        "sold_year": df["sold_year"].unique().tolist(),
        "town": df["town"].unique().tolist(),
        "flat_type": df["flat_type"].unique().tolist(),
        "address": df["address"].unique().tolist(),
        "storey_range": df["storey_range"].unique().tolist(),
        "lease_commence_year": df["lease_commence_date"].unique().tolist(),
    }


if __name__ == "__main__":
    logger.info("Begin Execution")
    df = download_all_data(step=100)
    unique_categories = calc_unique_categories(df)

    logger.info("Write to JSON")
    with open("data/unique_categories.json", "w") as f:
        json.dump(unique_categories, f)

    logger.info("Done")

# python -m src.03_SG_Housing_Price_Trends
