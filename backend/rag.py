import os

import chromadb

from openai import OpenAI

from dotenv import load_dotenv

from services.vector_store import (
    collection,
    create_embeddings
)


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
    n_results=3,
    document_id=None
):

    question_embedding = create_embeddings(
        [question]
    )[0]

    if document_id:

        results = collection.query(

            query_embeddings=[
                question_embedding
            ],

            n_results=n_results,

            where={
                "document_id": document_id
            }
        )

    else:

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


    response = openrouter_client.chat.completions.create(

        model="openrouter/free",

        messages=[

            {
                "role": "system",
                "content": (
                    "You are a helpful document "
                    "assistant. Answer only using "
                    "the provided document context."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ]

    )


    return response.choices[0].message.content

def ask_question(
    question,
    document_id=None
):

    documents = retrieve_documents(
        question,
        document_id=document_id
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