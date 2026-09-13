"""
PromptShield-AI
Explainability Module

Provides human-readable explanations
for hybrid defense decisions.
"""


def generate_explanation(result):

    """
    Generate explanation from hybrid defense output.

    Expected keys:
    - prompt
    - block_patterns
    - review_patterns
    - ml_prediction
    - ml_decision_score
    - final_decision
    """


    explanation = {}


    explanation["prompt"] = result.get(
        "prompt",
        ""
    )


    explanation["decision"] = result.get(
        "final_decision",
        "UNKNOWN"
    )


    evidence = []


    # Rule evidence

    block_patterns = result.get(
        "block_patterns",
        []
    )

    review_patterns = result.get(
        "review_patterns",
        []
    )


    if block_patterns:

        evidence.append(
            "Strong rule patterns detected: "
            + ", ".join(block_patterns)
        )


    if review_patterns:

        evidence.append(
            "Contextual/review patterns detected: "
            + ", ".join(review_patterns)
        )


        # ML evidence

    if "ml_decision_score" in result:

        score = result["ml_decision_score"]

        evidence.append(
            f"SVM decision score: {score}"
        )


    explanation["evidence"] = evidence


    # ML Confidence

    if "ml_decision_score" in result:

        score = result["ml_decision_score"]

        if abs(score) > 0.5:
            confidence = "High"

        elif abs(score) > 0.1:
            confidence = "Medium"

        else:
            confidence = "Low"

        explanation["ml_confidence"] = confidence
    # Human readable reason

    decision = explanation["decision"]


    if decision == "BLOCK":

        explanation["reason"] = (
            "Multiple suspicious indicators "
            "suggest a prompt injection attempt."
        )


    elif decision == "REVIEW":

        explanation["reason"] = (
            "Suspicious patterns detected. "
            "Additional review is recommended."
        )


    elif decision == "ALLOW":

        explanation["reason"] = (
            "No significant prompt injection "
            "indicators detected."
        )


    else:

        explanation["reason"] = (
            "Decision explanation unavailable."
        )


    return explanation