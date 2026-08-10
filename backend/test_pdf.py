from services.pdf_loader import extract_text_from_pdf
from services.chunker import create_chunks


pages = extract_text_from_pdf(
    "uploads/test.pdf"
)


chunks = create_chunks(
    pages,
    source="test.pdf"
    )


print("Number of chunks:", len(chunks))


for index, chunk in enumerate(chunks):

    print("\n====================")

    print("CHUNK:", index)

    print("PAGE:", chunk["page"])

    print(chunk["text"][:500])