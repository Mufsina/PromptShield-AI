import faiss
import os
import pickle

from src.rag.document_loader import load_documents
from src.rag.embeddings import create_embeddings


def build_vector_store():

    documents = load_documents(
        "data/rag_documents"
    )

    texts = [
        doc["content"]
        for doc in documents
    ]

    embeddings = create_embeddings(texts)


    dimension = embeddings.shape[1]


    index = faiss.IndexFlatL2(
        dimension
    )


    index.add(
        embeddings
    )


    os.makedirs(
        "models_saved/rag",
        exist_ok=True
    )


    faiss.write_index(
        index,
        "models_saved/rag/faiss.index"
    )


    with open(
        "models_saved/rag/documents.pkl",
        "wb"
    ) as f:

        pickle.dump(
            documents,
            f
        )


    print(
        "FAISS vector store created successfully"
    )


if __name__ == "__main__":

    build_vector_store()