def create_chunks(
    pages,
    source,
    document_id,
    chunk_size=400,
    chunk_overlap=80
):

    chunks = []


    for page in pages:

        text = page["text"].strip()


        if not text:
            continue


        words = text.split()


        start = 0


        while start < len(words):

            end = start + chunk_size


            chunk_words = words[start:end]


            chunk_text = " ".join(
                chunk_words
            ).strip()


            if chunk_text:

                chunks.append({

                    "text":
                        chunk_text,

                    "page":
                        page["page"],

                    "source":
                        source,

                    "document_id":
                        document_id

                })


            start += (
                chunk_size -
                chunk_overlap
            )


    return chunks