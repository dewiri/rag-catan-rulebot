import streamlit as st
import requests

st.title("Catan-Rules-Chatbot")
question = st.text_input("Ask Question")
if st.button("Send"):
    response = requests.post("http://localhost:8000/ask", json={"question": question})
    st.write(response.json().get("answer", "No Result"))
