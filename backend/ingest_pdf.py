import os

from services.pdf_loader import (
    extract_text_from_pdf
)

from services.chunker import (
    create_chunks
)

from services.vector_store import (
    store_chunks
)


PDF_PATH = "uploads/test.pdf"


file_name = os.path.basename(
    PDF_PATH
)


print("Reading PDF...")


pages = extract_text_from_pdf(
    PDF_PATH
)


print(
    f"Extracted {len(pages)} pages."
)


print("Creating chunks...")


chunks = create_chunks(
    pages,
    source=file_name
)


print(
    f"Created {len(chunks)} chunks."
)


print("Creating embeddings and storing...")


count = store_chunks(
    chunks
)


print(
    f"Successfully stored {count} chunks."
)