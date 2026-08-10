def create_chunks(
    pages,
    source,
    document_id,
    chunk_size=500,
    chunk_overlap=50
):

    chunks = []

    for page in pages:

        words = page["text"].split()

        start = 0

        while start < len(words):

            end = start + chunk_size

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            if chunk_text.strip():

                chunks.append({

                    "text": chunk_text,

                    "page": page["page"],

                    "source": source,

                    "document_id": document_id

                })

            start += (
                chunk_size - chunk_overlap
            )

    return chunks