🌟 View code on [Github](https://github.com/stephenleo/streamlit-apps/blob/main/pages/01_%F0%9F%8E%93_Graduate_School_Admissions.py)

This is a minimal working example for a Streamlit app running with a remote ML model deployed on GCP Cloud Run. The architecture is as follows:
1. ML model deployed on GCP Cloud Run using 🐳 Docker: [Link](https://grad-school-admission-a4rmk57awq-as.a.run.app)
1. Streamlit UI calls the API under the hood

👉 **Why Cloud Run?**
- Practically free for moderate usage: [Link](https://cloud.google.com/products/calculator/#id=32ea150c-67b7-4ebc-9143-789f703ee574)
- Easy to deploy with just one line: `gcloud run deploy`
- Frees up resources on the Streamlit app by offloading the ML computations to a remote server with a microservice architecture!