import streamlit as st
import requests
import os

st.title("📄 Ask My Document")

# Upload a PDF file
st.header("📤 Upload a PDF Document")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    # Ensure 'uploads/' directory exists
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file to the 'uploads/' folder
    file_path = f"uploads/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")

    # Send API request to process the uploaded PDF
    response = requests.post(f"http://127.0.0.1:8000/process_existing/?filename={uploaded_file.name}")

    if response.status_code == 200:
        st.success(f"📄 '{uploaded_file.name}' processed successfully!")
    else:
        st.error(f"⚠️ Error processing document: {response.text}")

# Question Input
st.header("❓ Ask a Question")
user_input = st.text_input("Enter your question:")

if st.button("Get Answer"):
    response = requests.get(f"http://127.0.0.1:8000/ask/?query={user_input}")

    if response.status_code == 200:
        answer = response.json().get("answer", "⚠️ No relevant answer found.")
        st.success(f"**Answer:** {answer}")
    else:
        st.error(f"❌ API Request Failed: {response.text}")
