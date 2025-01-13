import chromadb
from uuid import uuid4
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import multiprocessing as mp

def producer(queue, id,docs):
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

    for i in range(0, len(serializable_data), 100):  # Adjust batch size as needed
        batch_data = serializable_data[i:i+100]
        batch_ids = serialize_ids[i:i+100]
        queue.put((batch_data, batch_ids))

    queue.put(None)  # Signal the consumer to stop

def consumer(queue, id):
    print("Creating collection...")
    
    chroma_client = chromadb.HttpClient(
        host="34.131.189.237",
        port=8000
    )
    
    chroma_client.heartbeat()

    collection = chroma_client.create_collection(f"{id}")

    while True:
        batch = queue.get()
        if batch is None:
            break

        print("Adding data to collection...")
        collection.add(
            documents=batch[0],
            ids=batch[1],
        )

def getContext(query, id, docs):
    queue = mp.Queue()

    producer_process = mp.Process(target=producer, args=(queue, id,docs))
    consumer_process = mp.Process(target=consumer, args=(queue, id))

    producer_process.start()
    consumer_process.start()

    producer_process.join()
    consumer_process.join()

    print("Querying the collection...")
    chroma_client = chromadb.HttpClient(
        host="chromadb",
        port=8001
    )
    collection = chroma_client.get_collection(f"{id}")
    result = collection.query(
        query_texts=[query],
        n_results=2
    )

    print("Result documents:")
    print(result["documents"])
    return result["documents"][0][0]
