import streamlit as st # type: ignore
import requests # type: ignore

st.title("My App Connected to My Private API")
topic = st.text_input("Enter Topic:")

if st.button("Generate"):
    if not topic:
        st.error("Please enter a topic.")
    else:
        api_url = "http://127.0.0.1:8000/generate-content"
        payload = {"topic": topic, "tone": "Professional"}

        response = requests.post(api_url, json=payload)

        if response.status_code == 200:
            st.write(response.json()["ai_response"])
        else:
            st.error("Failed to connect to internal API.")

