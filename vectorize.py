import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader,PyPDFLoader

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
books_dir = os.path.join(current_dir,"docs")
db_dir = os.path.join(current_dir,"db")
persistent_directory = os.path.join(db_dir,"chroma_db")

if not os.path.exists(persistent_directory):
    print("\nCreating Vector Store\n")

    if not os.path.exists(books_dir):
        raise FileNotFoundError(f"Books directory not found at {books_dir}")
    
    book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt") or f.endswith(".pdf")]

    documents = []

    for book_file in book_files:
        file_path = os.path.join(books_dir,book_file)
        if book_file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif book_file.endswith(".txt"):
            loader = TextLoader(file_path,encoding='utf-8')
        
        book_docs = loader.load()
        for doc in book_docs:
            doc.metadata = {"source":book_file}
            documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50)
    docs = text_splitter.split_documents(documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embeddings-001")
    db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_directory)
    print("\nVectores created and stored in DB")

else:
    print("\nVector store already exists\n")