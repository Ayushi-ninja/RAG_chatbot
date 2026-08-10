from pathlib import Path


def create_vector_store(path: str = "./chroma_db"):
    return {
        "path": str(Path(path).resolve()),
        "status": "ready"
    }
