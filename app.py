import streamlit as st
import requests

st.title("📄 Ask My Document")

# --- Upload a PDF file ---
st.header("📤 Upload a PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Send the uploaded file directly to the backend /upload/ endpoint
    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
    response = requests.post("http://127.0.0.1:8000/upload/", files=files)

    if response.status_code == 200:
        st.success(f"📄 '{uploaded_file.name}' uploaded and processed successfully!")
    else:
        st.error(f"⚠️ Error processing document: {response.text}")

# --- Ask a Question ---
st.header("❓ Ask a Question")
user_input = st.text_input("Enter your question:")

if st.button("Get Answer") and user_input:
    response = requests.get(f"http://127.0.0.1:8000/ask/?query={user_input}")

    if response.status_code == 200:
        answer = response.json().get("answer", "⚠️ No relevant answer found.")
        st.success(f"**Answer:** {answer}")
    else:
        st.error(f"❌ API Request Failed: {response.text}")
