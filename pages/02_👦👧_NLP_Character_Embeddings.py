import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Character Embeddings",
    page_icon="🧑",
)

# Title of the page
st.title("👦👧 Boy or Girl?")
st.header("Check if your names are Boy's names or Girl's names")

with open("descriptions/02_👦👧_NLP_Character_Embeddings.md", "r") as f:
    content = f.read()

with st.sidebar:
    st.header("👦👧 Boy or Girl?")
    st.markdown(content)

# Get user inputs
names = st.text_input(
    "Names", help="Input the names you'd like to check separated with spaces or commas"
)

# Add a submit button
if st.button("Submit"):
    # Code to post the user inputs to the API and get the predictions
    # Paste the URL to your GCP Cloud Run API here!
    api_url = "https://name-gender1.p.rapidapi.com/predict"

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": st.secrets["RAPID_API_KEY"],
        "X-RapidAPI-Host": "name-gender1.p.rapidapi.com",
    }

    with st.spinner("🥁 Drumroll..."):
        response = requests.post(api_url, json=[names], headers=headers)

    predictions_df = pd.DataFrame(response.json()["response"])
    predictions_df.columns = ["Name", "Boy or Girl?", "Probability"]
    predictions_df = predictions_df.apply(
        lambda x: x.str.title() if x.dtype == "object" else x
    )

    fig = px.bar(
        predictions_df,
        x="Probability",
        y="Name",
        color="Boy or Girl?",
        orientation="h",
        color_discrete_map={"Boy": "dodgerblue", "Girl": "lightcoral"},
    )

    fig.update_layout(
        title={"text": "Confidence in Prediction", "x": 0.5},
        yaxis={
            "categoryorder": "array",
            "categoryarray": predictions_df["Name"].values.tolist(),
            "autorange": "reversed",
        },
        xaxis={"range": [0, 1]},
        font={"size": 14},
        # width=700
    )

    st.write("Predictions")
    st.dataframe(predictions_df)
    st.plotly_chart(fig, use_container_width=True)
