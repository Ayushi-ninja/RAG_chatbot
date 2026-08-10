import os

import chromadb
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)


collection = chroma_client.get_collection(
    name="knowledge_base"
)


def retrieve_documents(question, n_results=3):

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )

    documents = results["documents"][0]

    return documents


def generate_answer(question, documents):

    context = "\n\n".join(documents)

    prompt = f"""
You are a helpful assistant.

Answer the user's question using ONLY the information
provided in the context below.

If the answer cannot be found in the context,
say: "I don't know based on the provided documents."

Context:
{context}

User question:
{question}

Answer:
"""

    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output_text


def ask_question(question):

    documents = retrieve_documents(question)

    answer = generate_answer(
        question,
        documents
    )

    return {
        "answer": answer,
        "sources": documents
    }