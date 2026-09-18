"""
PromptShield-AI
RAG Security API

Combines:
1. FAISS Retriever
2. RAG Security Scanner
3. HybridDefenseV2

Provides:
- Prompt injection detection
- Retrieved document security analysis
"""


from fastapi import FastAPI
from pydantic import BaseModel


from src.rag.retriever import retrieve_documents
from src.rag.security import RAGSecurity
from src.defense.hybrid_defense_v2 import HybridDefenseV2



app = FastAPI(
    title="PromptShield-AI RAG Security API",
    description=(
        "Hybrid AI framework for detecting "
        "prompt injection attacks in RAG systems"
    ),
    version="2.0.0"
)



# Load models once

detector = HybridDefenseV2()

security = RAGSecurity()



class QueryRequest(BaseModel):

    query: str



@app.get("/")
def root():

    return {
        "project": "PromptShield-AI",
        "status": "running",
        "version": "2.0.0"
    }



@app.get("/health")
def health():

    return {
        "status": "healthy",
        "components": {
            "retriever": "active",
            "rag_security": "active",
            "hybrid_defense": "active"
        }
    }



@app.post("/analyze")
def analyze(request: QueryRequest):


    query = request.query



    # -------------------------
    # Step 1: Retrieve documents
    # -------------------------

    retrieved = retrieve_documents(
        query,
        top_k=3
    )


    documents = [
        item["document"]
        for item in retrieved
    ]



    # -------------------------
    # Step 2: Scan RAG context
    # -------------------------

    security_results = (
        security.scan_documents(
            documents
        )
    )



    # -------------------------
    # Step 3: Analyze query
    # -------------------------

    prompt_result = detector.analyze(
        query
    )



    # -------------------------
    # Final response
    # -------------------------

    return {

        "query": query,


        "prompt_analysis": {

            "decision":
            prompt_result["final_decision"],

            "ml_prediction":
            prompt_result["ml_prediction"],

            "ml_score":
            prompt_result["ml_decision_score"],

            "block_patterns":
            prompt_result["block_patterns"],

            "review_patterns":
            prompt_result["review_patterns"]

        },


        "retrieved_documents":
        security_results

    }