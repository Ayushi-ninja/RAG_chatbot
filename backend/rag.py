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


collection = chroma_client.get_collection(
    name="knowledge_base"
)


def retrieve_documents(
    question,
    n_results=3
):

    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = (
        response.data[0].embedding
    )


    results = collection.query(
        query_embeddings=[
            question_embedding
        ],
        n_results=n_results
    )


    documents = results["documents"][0]

    metadatas = results["metadatas"][0]


    retrieved = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        retrieved.append({
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"]
        })


    return retrieved


def generate_answer(
    question,
    documents
):

    context_parts = []


    for document in documents:

        context_parts.append(
            f"""
Source: {document['source']}
Page: {document['page']}

Content:
{document['text']}
"""
        )


    context = "\n\n".join(
        context_parts
    )


    prompt = f"""
You are a helpful document assistant.

Answer the user's question using ONLY
the information contained in the provided
document context.

If the answer cannot be found in the
provided context, say:

"I don't know based on the provided documents."


DOCUMENT CONTEXT:

{context}


USER QUESTION:

{question}


Answer clearly and concisely.
"""


    response = openai_client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )


    return response.output_text


def ask_question(question):

    documents = retrieve_documents(
        question
    )


    answer = generate_answer(
        question,
        documents
    )


    sources = []


    for document in documents:

        sources.append({
            "source": document["source"],
            "page": document["page"]
        })


    return {
        "answer": answer,
        "sources": sources
    }