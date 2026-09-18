"""
PromptShield-AI

Hybrid RAG Security Test

Flow:

User Query
    ↓
FAISS Retriever
    ↓
Retrieved Documents
    ↓
HybridDefenseV2
    ↓
ALLOW / REVIEW / BLOCK
"""


from src.rag.retriever import retrieve_documents
from src.defense.hybrid_defense_v2 import HybridDefenseV2



def main():

    query = "What is machine learning?"


    print("\nUSER QUERY:")
    print(query)


    # Retrieve documents from FAISS

    retrieved_documents = retrieve_documents(
        query,
        top_k=3
    )


    documents = [
        item["document"]
        for item in retrieved_documents
    ]


    print("\nRetrieved Documents:")
    print("=" * 70)


    for i, doc in enumerate(documents, start=1):

        print(f"\nDocument {i}")
        print("File:", doc.get("file"))
        print("Content:")
        print(doc.get("content"))
        print("-" * 70)



    # Hybrid Security Layer

    detector = HybridDefenseV2()


    print("\n\nHYBRID SECURITY ANALYSIS")
    print("=" * 70)



    for i, document in enumerate(documents, start=1):

        result = detector.analyze(
            document
        )


        print(f"\nDocument {i}")

        print(
            "File:",
            result["file"]
        )

        print(
            "Rule Risk:",
            result["rule_risk_score"]
        )

        print(
            "Block Patterns:",
            result["block_patterns"]
        )

        print(
            "Review Patterns:",
            result["review_patterns"]
        )

        print(
            "ML Prediction:",
            result["ml_prediction"]
        )

        print(
            "ML Score:",
            result["ml_decision_score"]
        )

        print(
            "Final Decision:",
            result["final_decision"]
        )

        print("-" * 70)



if __name__ == "__main__":

    main()