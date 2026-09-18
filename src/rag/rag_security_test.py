from src.rag.retriever import retrieve_documents
from src.rag.security import RAGSecurity


if __name__ == "__main__":

    query = "What is machine learning?"

    retrieved = retrieve_documents(
        query,
        top_k=3
    )

    documents = [
        item["document"]
        for item in retrieved
    ]


    security = RAGSecurity()

    results = security.scan_documents(
        documents
    )


    print("\nRAG Security Analysis:\n")


    for i, result in enumerate(results, start=1):

        print(f"Document {i}")
        print(f"File: {result['file']}")
        print(f"Risk Score: {result['risk_score']}")
        print(f"Decision: {result['decision']}")
        print(f"Matched Patterns: {result['matched_patterns']}")
        print("-" * 50)
