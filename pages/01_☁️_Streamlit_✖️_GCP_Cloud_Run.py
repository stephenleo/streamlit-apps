import json

import requests
import streamlit as st

st.set_page_config(
    page_title="Streamlit X GCP Cloud Run",
    page_icon="☁️",
)

# Title of the page
st.title("🎓 Graduate School Admissions")

with open("descriptions/01_☁️_Streamlit_✖️_GCP_Cloud_Run.md", "r") as f:
    content = f.read()

with st.sidebar:
    st.header("🎓 Graduate School Admissions")
    st.markdown(content)

# Get user inputs
gre = st.number_input(
    "📚 GRE Score:", min_value=0, max_value=800, help="GRE score in the range 0 to 800"
)  # int max value to allow only int inputs
gpa = st.number_input(
    "✍️ GPA Score:", min_value=0.0, max_value=5.0, help="GPA in the range 0 to 5"
)  # float max value to allow decimal inputs

# Display the inputs
user_input = {"gre": gre, "gpa": gpa}
st.write("User input:")
st.write(user_input)

# Add a submit button
if st.button("Submit"):
    # Code to post the user inputs to the API and get the predictions
    # Paste the URL to your GCP Cloud Run API here!
    api_url = "https://grad-school-admission-a4rmk57awq-as.a.run.app"
    api_route = "/predict"

    response = requests.post(
        f"{api_url}{api_route}", json=json.dumps(user_input)
    )  # json.dumps() converts dict to JSON
    predictions = response.json()

    st.write(f"Prediction: {predictions['predictions'][0]}")
