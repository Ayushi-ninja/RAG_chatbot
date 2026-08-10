import os

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from services.pdf_loader import (
    extract_text_from_pdf
)

from services.chunker import (
    create_chunks
)

from services.vector_store import (
    store_chunks
)

from rag import ask_question




app = FastAPI(
    title="RAG Chatbot API",
    description="A document-based RAG chatbot using OpenRouter and ChromaDB",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



UPLOAD_DIRECTORY = "uploads"

os.makedirs(
    UPLOAD_DIRECTORY,
    exist_ok=True
)



class ChatRequest(BaseModel):

    question: str



@app.get("/")
def home():

    return {
        "message": "RAG Chatbot API is running",
        "status": "success"
    }



@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }



@app.post("/chat")
def chat(
    request: ChatRequest
):

    try:

        result = ask_question(
            request.question
        )

        return result

    except Exception as error:

        print(
            "Chat error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process the question."
        )




@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

 

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )


    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are currently supported."
        )



    file_path = os.path.join(
        UPLOAD_DIRECTORY,
        file.filename
    )


    try:

       

        contents = await file.read()


       
        with open(
            file_path,
            "wb"
        ) as output_file:

            output_file.write(
                contents
            )


        

        pages = extract_text_from_pdf(
            file_path
        )


        if not pages:

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the PDF."
            )


      

        chunks = create_chunks(
            pages,
            source=file.filename
        )


        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="No text chunks were created from the PDF."
            )


  

        chunk_count = store_chunks(
            chunks
        )


        

        return {

            "message":
                "Document uploaded successfully.",

            "filename":
                file.filename,

            "pages":
                len(pages),

            "chunks":
                chunk_count
        }


    except HTTPException:

        raise


    except Exception as error:

        print(
            "Upload error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to process the PDF."
        )