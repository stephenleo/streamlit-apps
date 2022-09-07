import streamlit as st
import requests
import json

# Title of the page
st.title("🎓 Graduate School Admissions")

# Get user inputs
gre = st.number_input("📚 GRE Score:", step=1, max_value=800)
gpa = st.number_input("✍️ GPA Score:", max_value=5.0)

# Display the inputs
user_input = {"gre":gre,"gpa":gpa}
st.write("User input:")
st.write(user_input)

# Code to post the user inputs to the API and get the predictions
api_url = 'https://grad-school-admission-a4rmk57awq-as.a.run.app'
api_route = '/predict'

response = requests.post(f'{api_url}{api_route}', json=json.dumps(user_input)) # json.dumps() converts dict to JSON
predictions = response.json()

# Add a submit button
if st.button("Submit"): 
    st.write(f"Prediction: {predictions['predictions'][0]}")
