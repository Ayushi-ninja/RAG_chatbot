import os

import chromadb

from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()


openrouter_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)

#embedding model to use for creating embeddings
EMBEDDING_MODEL = (
    "nvidia/nemotron-3-embed-1b:free"
)

# create client embedding
def create_embeddings(texts):

    print(
        f"Creating embeddings for {len(texts)} chunks..."
    )

    response = (
        openrouter_client.embeddings.create(

            model=EMBEDDING_MODEL,

            input=texts,

            encoding_format="float"
        )
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    print(
        f"Created {len(embeddings)} embeddings."
    )

    return embeddings



def store_chunks(chunks):

    if not chunks:

        raise ValueError(
            "No chunks were provided."
        )


    texts = [
        chunk["text"]
        for chunk in chunks
    ]


    embeddings = create_embeddings(
        texts
    )


    ids = []

    documents = []

    metadatas = []


    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"{chunk['source']}"
            f"-{chunk['page']}"
            f"-{index}"
        )


        ids.append(
            chunk_id
        )


        documents.append(
            chunk["text"]
        )


        metadatas.append({

            "source":
                chunk["source"],

            "page":
                chunk["page"]

        })


    collection.upsert(

        ids=ids,

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas
    )


    print(
        f"Stored {len(chunks)} chunks in ChromaDB."
    )


    return len(chunks)