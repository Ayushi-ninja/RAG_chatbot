import os
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)


def create_chunks(text, chunk_size=500):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


with open("data/knowledge.txt", "r", encoding="utf-8") as file:
    document = file.read()


chunks = create_chunks(document)

print(f"Created {len(chunks)} chunks.")


response = client.embeddings.create(
    model="text-embedding-3-small",
    input=chunks
)

embeddings = [
    item.embedding
    for item in response.data
]


ids = [
    f"chunk-{i}"
    for i in range(len(chunks))
]


collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)

print("Documents successfully stored in ChromaDB.")
