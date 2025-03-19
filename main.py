import os
import fitz  # PyMuPDF for PDFs
import faiss
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
from fastapi import FastAPI, File, UploadFile
from sentence_transformers import SentenceTransformer, CrossEncoder

# Download NLTK tokenizer
nltk.download('punkt')
nltk.data.path.append("/Users/stutipandey/nltk_data")
nltk.download('punkt')


# Initialize FastAPI app
app = FastAPI()

# Load embedding and re-ranking models
model = SentenceTransformer("all-MiniLM-L6-v2")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# FAISS index setup
dimension = 384  # Matches Sentence Transformer output
index = faiss.IndexFlatL2(dimension)
documents = []  # Store document text

@app.get("/")
async def root():
    return {"message": "Welcome to the Document Q&A API! Use /docs to test."}

def get_embedding(text):
    return np.array(model.encode(text), dtype=np.float32)

# Function to extract text from PDF
def extract_text(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text

@app.post("/upload/")
async def upload_file(file: UploadFile):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = extract_text(file_path)

    # Debugging print
    print(f"✅ Extracted {len(text)} characters from {file.filename}")

    # Split into meaningful chunks
    sentences = sent_tokenize(text)
    chunk_size = 5  
    chunks = [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]

    for chunk in chunks:
        emb = get_embedding(chunk)
        index.add(np.array([emb]))  # Add to FAISS index
        documents.append(chunk)

    print(f"✅ Stored {len(chunks)} document chunks in FAISS index.")

    return {"filename": file.filename, "message": "Document processed successfully!"}

# Process an existing document
@app.post("/process_existing/")
async def process_existing_file(filename: str):
    file_path = f"uploads/{filename}"
    
    if not os.path.exists(file_path):
        return {"error": "File not found!"}

    # Extract text
    text = extract_text(file_path)

    # Split into meaningful sentences instead of fixed character chunks
    sentences = sent_tokenize(text)

    # Combine small sentences to form coherent paragraphs
    chunk_size = 8  # Increase context range
    chunks = [" ".join(sentences[i:i+chunk_size]) for i in range(0, len(sentences), chunk_size)]

    for chunk in chunks:
        emb = get_embedding(chunk)
        index.add(np.array([emb]))  # Add to FAISS index
        documents.append(chunk)  # Store text

    return {"filename": filename, "message": "Existing document processed with improved chunking!"}


# Ask a question
@app.get("/ask/")
async def ask_question(query: str):
    if index.ntotal == 0:
        return {"error": "No document embeddings found! Process a document first."}

    print(f"🔎 Query received: {query}")
    print(f"📄 FAISS Index contains {index.ntotal} embeddings.")

    query_emb = get_embedding(query)

    # Retrieve top 5 matches
    D, I = index.search(np.array([query_emb]), k=5)

    if len(D) == 0 or len(I) == 0:
        return {"error": "No relevant matches found in the document."}

    best_match = documents[I[0][0]]
    
    return {"query": query, "answer": best_match}


# Test embedding functionality
test_text = "Hello, test embedding!"
try:
    emb = get_embedding(test_text)
    print("✅ Embeddings are working correctly!")
except Exception as e:
    print(f"❌ Embedding Error: {e}")
