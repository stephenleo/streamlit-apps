import json

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from stqdm import stqdm

url = "https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3"


def user_inputs(unique_categories: dict) -> dict:
    filters = {}
    st.subheader("User Inputs")
    st.caption("Select the filters you want to apply to the data.")
    st.caption(
        "Leave the dropdown selection empty to select All in that respective dropdown."
    )

    if sold_year := st.selectbox(
        "Sold Year", options=[""] + sorted(unique_categories["sold_year"])
    ):
        filters["month"] = [f"{sold_year}-{month:02}" for month in range(1, 13)]

    if town := st.selectbox("Town", options=[""] + sorted(unique_categories["town"])):
        filters["town"] = town

    if addresses := st.multiselect(
        "Address", options=[""] + sorted(unique_categories["address"])
    ):
        split_addresses = [address.split() for address in addresses]
        filters["block"] = [address[0] for address in split_addresses]
        filters["street_name"] = [" ".join(address[1:]) for address in split_addresses]

    if flat_type := st.selectbox(
        "Flat Type", options=[""] + sorted(unique_categories["flat_type"])
    ):
        filters["flat_type"] = flat_type

    if storey_range := st.selectbox(
        "Storey Range", options=[""] + sorted(unique_categories["storey_range"])
    ):
        filters["storey_range"] = storey_range

    if lease_commence_date := st.selectbox(
        "Lease Commence Year",
        options=[""] + sorted(unique_categories["lease_commence_year"]),
    ):
        filters["lease_commence_date"] = lease_commence_date

    st.write("API Payload:")
    st.write(filters)

    return filters


def plot_violin(
    df: pd.DataFrame, x: str, y: str, xaxis_title: str, yaxis_title: str, title: str
) -> None:
    fig = px.violin(df.sort_values(x), y=y, x=x, box=True)
    fig.update_layout(xaxis_title=xaxis_title, yaxis_title=yaxis_title, title=title)
    st.plotly_chart(fig, use_container_width=True)


def dashboard(df: pd.DataFrame) -> None:
    # Price vs Floor
    plot_violin(
        df,
        x="storey_range",
        y="psf",
        xaxis_title="Storey Range",
        yaxis_title="PSF ($)",
        title="Price vs Floor",
    )

    # Price vs Purchase month
    plot_violin(
        df,
        x="month",
        y="psf",
        xaxis_title="Purchase Month",
        yaxis_title="PSF ($)",
        title="Price vs Purchase Month",
    )


##### Main #####
st.set_page_config(
    page_title="Singapore Housing Price Trends",
    page_icon="🇸🇬",
)

# Title of the page
st.title("🇸🇬 Singapore Housing Trends")
st.header("Check Trends in Singapore Housing Prices")

# Sidebar
with open("descriptions/03_🇸🇬_SG_Housing_Price_Trends.md", "r") as f:
    content = f.read()

with st.sidebar:
    st.header("🇸🇬 Singapore Housing Trends")
    st.markdown(content)

# Load unique categories
with open("data/unique_categories.json", "r") as f:
    unique_categories = json.load(f)

# Get user inputs
filters = user_inputs(unique_categories)

# Submit button
if st.button("Submit"):
    # Code to post the user inputs to the API and get the data

    filtered_url = f"{url}&filters={json.dumps(filters)}"

    try:
        total_rows = requests.get(f"{filtered_url}&limit=1").json()["result"]["total"]
        st.write(f"Total rows: {total_rows}")

        if total_rows > 1000:
            st.warning("Too many rows to query (max 1000). Please refine your filters.")
        else:
            records = []
            step = 100
            for start_row in stqdm(range(0, total_rows, step)):
                offset_url = f"{filtered_url}&limit={step}&offset={start_row}"
                records.extend(requests.get(offset_url).json()["result"]["records"])

            # API results to Dataframe
            df = pd.DataFrame(records)
            df = df.apply(pd.to_numeric, errors="ignore")
            df["floor_area_sqft"] = df["floor_area_sqm"] * 10.764
            df["psm"] = df["resale_price"] / df["floor_area_sqm"]
            df["psf"] = df["resale_price"] / df["floor_area_sqft"]
            df = df.sort_values(by="month", ascending=False)
            # df.to_pickle("data/sg_housing_price_trends.pkl")
            st.write(df)

            # Plots
            dashboard(df)

    except Exception as e:
        st.write(e)  # "No flats meet the filter criteria. Please adjust your filters")
