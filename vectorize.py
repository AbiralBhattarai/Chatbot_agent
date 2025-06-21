import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader,PyPDFLoader

#loading the env variables
load_dotenv()

#path initialization for vectorstore and documents
current_dir = os.path.dirname(os.path.abspath(__file__))
books_dir = os.path.join(current_dir,"docs")
db_dir = os.path.join(current_dir,"db")
persistent_directory = os.path.join(db_dir,"chroma_db")


if not os.path.exists(persistent_directory):
    #check if vectorstore directory exists
    print("\nCreating Vector Store\n")

    if not os.path.exists(books_dir):
        #check if file path for document exists
        raise FileNotFoundError(f"Books directory not found at {books_dir}")
    
    book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt") or f.endswith(".pdf")] #load the txt and pdf file paths into a list.

    documents = []

    for book_file in book_files:
        #loop to open and load the documents and store them in the document list.
        file_path = os.path.join(books_dir,book_file)
        if book_file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif book_file.endswith(".txt"):
            loader = TextLoader(file_path,encoding='utf-8')
        
        book_docs = loader.load()
        for doc in book_docs:
            doc.metadata = {"source":book_file} #adding metadata about the document.
            documents.append(doc)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=50) #doc splitter
    docs = text_splitter.split_documents(documents) #splitting the document into chunks with 50 characters overlap between chunks
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embeddings-001")#generate vectors
    db = Chroma.from_documents(docs,embeddings,persist_directory=persistent_directory)#store the vectors in the chroma vectorstore
    print("\nVectores created and stored in DB")

else:
    print("\nVector store already exists\n")