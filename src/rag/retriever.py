import faiss
import pickle

from src.rag.embeddings import create_embeddings


INDEX_PATH = "models_saved/rag/faiss.index"
DOCUMENTS_PATH = "models_saved/rag/documents.pkl"


def load_vector_store():
    index = faiss.read_index(INDEX_PATH)

    with open(DOCUMENTS_PATH, "rb") as f:
        documents = pickle.load(f)

    return index, documents


def retrieve_documents(query, top_k=3):
    index, documents = load_vector_store()

    query_embedding = create_embeddings([query])

    distances, indices = index.search(query_embedding, top_k)

    results = []

    for distance, index_id in zip(distances[0], indices[0]):

        if index_id == -1:
            continue

        results.append({
            "document": documents[index_id],
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    query = "What is machine learning?"

    results = retrieve_documents(query, top_k=3)

    print("\nRetrieved Documents:\n")

    for i, result in enumerate(results, start=1):

        print(f"Result {i}")
        print(f"Distance: {result['distance']}")
        print(f"Document: {result['document']}")
        print("-" * 50)