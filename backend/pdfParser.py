import pymupdf4llm
from langchain.text_splitter import MarkdownTextSplitter
from langchain_ollama.embeddings import OllamaEmbeddings
import chromadb
import uuid
import json
#semantic chunker 

chroma_client = chromadb.Client()

collection = chroma_client.create_collection("docsCollection")

def getContext(query):
    md_text = pymupdf4llm.to_markdown("backend/Samples/test.pdf")

    splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=30)
    
    data = splitter.create_documents(
        texts= [md_text]
    )
    

    serializable_data = [doc.page_content for doc in data]

   
    serialize_ids = [str(uuid.uuid4()) for _ in serializable_data]
    collection.add(
        documents= serializable_data[:50],
        ids= serialize_ids[:50],
    )

    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result["documents"]

getContext("Mahatma Gandhi")