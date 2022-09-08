import streamlit as st

st.set_page_config(
    page_title="Stephen Leo's Streamlit Apps",
    page_icon="favicon.png",
)

st.title("🚀 Streamlit Apps")

st.sidebar.success("Select a demo above.")

with open("about.md", "r") as f:
    content = f.read()
st.markdown(content)
