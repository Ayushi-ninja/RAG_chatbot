import os

from openai import OpenAI

from dotenv import load_dotenv


load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)


print("Testing OpenRouter embeddings...")


response = client.embeddings.create(

    model="nvidia/nemotron-3-embed-1b:free",

    input=[
        "This is a test document."
    ],

    encoding_format="float"
)


embedding = response.data[0].embedding


print("Embedding successfully created!")

print(
    "Embedding dimensions:",
    len(embedding)
)

print(
    "First 5 values:",
    embedding[:5]
)