
# 📄 Document-QA  

A **FastAPI-powered** Document Q&A system that utilizes **FAISS** for efficient retrieval and **SentenceTransformers** for embedding-based search. It enables users to upload PDF documents and ask questions, retrieving contextually relevant answers from the documents.

---

## 🚀 Features  
✅ **Upload PDFs** and extract meaningful content  
✅ **FAISS-based Retrieval** for efficient search  
✅ **Sentence Embeddings** for improved answer relevance  
✅ **FastAPI Backend** for handling queries  
✅ **Streamlit UI** for easy interaction  

---

## 🛠️ Tech Stack  
- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)  
- **Vector Search:** FAISS  
- **PDF Processing:** PyMuPDF (fitz)  
- **Re-ranking:** CrossEncoder (MS MARCO)  

---

## 📂 Project Structure  
```
document-qa/ 
│── uploads/ # Folder to store uploaded PDFs
│── venv/ # Virtual environment (not tracked)
│── main.py # FastAPI Backend
│── app.py # Streamlit Frontend
│── requirements.txt # Dependencies
│── .gitignore # Ignored files (venv, cache, large files)
│── README.md # Project Documentation
```

---

## 🛠️ Setup Instructions  

### 1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/stutipandey20/Document-QA.git
cd Document-QA
```

### 2️⃣ Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux  
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Backend (FastAPI)
```bash
uvicorn main:app --reload
```
FastAPI will be available at: http://127.0.0.1:8000/docs

### 5️⃣ Run the Frontend (Streamlit)
```bash
streamlit run app.py
```

### 📌 How It Works
1️⃣ **Upload a PDF document** using the frontend.  
2️⃣ **The document is processed and stored in FAISS.**  
3️⃣ **Ask a question**, and the system retrieves the most relevant passage.  
4️⃣ **Re-ranks results for improved answer accuracy.**  

### 🎯 Learnings & Takeaways
How to build a document-based Q&A system.
Efficient use of FAISS for fast vector retrieval.
Combining NLP models for better information retrieval.
Deploying a FastAPI-based backend with a user-friendly UI.

### 📌 TODO (Next Improvements)
 Add support for multi-document queries
 Improve answer extraction using a fine-tuned model
 Deploy on AWS/GCP for public access

### 🏆 Acknowledgments
Special thanks to FastAPI, FAISS, and Hugging Face Transformers for providing amazing open-source tools that made this project possible.
