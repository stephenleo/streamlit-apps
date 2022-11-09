import json

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from stqdm import stqdm

url = "https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3"

st.set_page_config(
    page_title="Singapore Housing Price Trends",
    page_icon="🇸🇬",
)

# Title of the page
st.title("🇸🇬 Singapore Housing Trends")
st.header("Check Trends in Singapore Housing Prices")

with open("descriptions/03_🇸🇬_SG_Housing_Price_Trends.md", "r") as f:
    content = f.read()

with st.sidebar:
    st.header("🇸🇬 Singapore Housing Trends")
    st.markdown(content)

# Load unique categories
with open("data/unique_categories.json", "r") as f:
    unique_categories = json.load(f)


# Get user inputs
filters = {}

sold_year = st.selectbox(
    "Sold Year", options=[""] + sorted(unique_categories["sold_year"])
)
if sold_year:
    filters["month"] = [f"{sold_year}-{month:02}" for month in range(1, 13)]

town = st.selectbox("Town", options=[""] + sorted(unique_categories["town"]))
if town:
    filters["town"] = town

address = st.selectbox("Address", options=[""] + sorted(unique_categories["address"]))
if address:
    filters["block"] = address.split()[0]
    filters["street_name"] = " ".join(address.split()[1:])


flat_type = st.selectbox(
    "Flat Type", options=[""] + sorted(unique_categories["flat_type"])
)
if flat_type:
    filters["flat_type"] = flat_type


storey_range = st.selectbox(
    "Storey Range", options=[""] + sorted(unique_categories["storey_range"])
)
if storey_range:
    filters["storey_range"] = storey_range


lease_commence_date = st.selectbox(
    "Lease Commence Year",
    options=[""] + sorted(unique_categories["lease_commence_year"]),
)
if lease_commence_date:
    filters["lease_commence_date"] = lease_commence_date

st.write("API Payload:")
st.write(filters)

# Add a submit button
if st.button("Submit"):
    # Code to post the user inputs to the API and get the data

    filtered_url = f"{url}&filters={json.dumps(filters)}"

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

        df = pd.DataFrame(records)
        st.write(df)


#     # TODO
#     api_route = "/predict"

#     with st.spinner("🥁 Drumroll..."):
#         response = requests.post(f"{api_url}{api_route}", json=[names])

#     predictions_df = pd.DataFrame(response.json()["response"])
#     predictions_df.columns = ["Name", "Boy or Girl?", "Probability"]
#     predictions_df = predictions_df.apply(
#         lambda x: x.str.title() if x.dtype == "object" else x
#     )

#     fig = px.bar(
#         predictions_df,
#         x="Probability",
#         y="Name",
#         color="Boy or Girl?",
#         orientation="h",
#         color_discrete_map={"Boy": "dodgerblue", "Girl": "lightcoral"},
#     )

#     fig.update_layout(
#         title={"text": "Confidence in Prediction", "x": 0.5},
#         yaxis={
#             "categoryorder": "array",
#             "categoryarray": predictions_df["Name"].values.tolist(),
#             "autorange": "reversed",
#         },
#         xaxis={"range": [0, 1]},
#         font={"size": 14},
#         # width=700
#     )

#     st.write("Predictions")
#     st.dataframe(predictions_df)
#     st.plotly_chart(fig, use_container_width=True)
