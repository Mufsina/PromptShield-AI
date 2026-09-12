from fastapi import FastAPI
from pydantic import BaseModel

from src.defense.hybrid_defense_v2 import HybridDefenseV2


app = FastAPI(
    title="PromptShield-AI",
    description="Hybrid AI framework for detecting prompt injection attacks",
    version="1.0.0"
)


detector = HybridDefenseV2()


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    return {
        "project": "PromptShield-AI",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "Hybrid Defense V2"
    }


@app.post("/predict")
def predict(request: PromptRequest):
    result = detector.analyze(request.prompt)

    return {
        "prompt": result["prompt"],
        "decision": result["final_decision"],
        "rule_risk_score": result["rule_risk_score"],
        "rule_decision": result["rule_decision"],
        "ml_prediction": result["ml_prediction"],
        "ml_label": result["ml_label"],
        "ml_decision_score": result["ml_decision_score"],
        "ml_borderline": result["ml_borderline"],
        "matched_block_patterns": result["block_patterns"],
        "matched_review_patterns": result["review_patterns"]
    }