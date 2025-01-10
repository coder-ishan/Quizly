import chromadb
from uuid import uuid4
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def getContext(query, id):
    print("Creating collection...")
    
    chroma_client  = chromadb.HttpClient(
        host="chromadb",
        port=8001
    )
    
    chroma_client.heartbeat()

    collection = chroma_client.create_collection(f"{id}")

    print("Loading and parsing document...")
    loader = PyMuPDFLoader("Samples/test.pdf")
    docs = loader.load()

    print("Splitting text semantically...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    data = splitter.split_documents(docs)

    print("Preparing data for collection...")
    serializable_data = [doc.page_content for doc in data]
    serialize_ids = [str(uuid4()) for _ in serializable_data]

    print("Adding data to collection...")
    collection.add(
        documents=serializable_data,
        ids=serialize_ids,
    )

    print("Querying the collection...")
    result = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("Result documents:")
    print(result["documents"])
    return result["documents"]


