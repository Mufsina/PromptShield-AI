"""
PromptShield-AI
HybridDefenseV2 Evaluation

Metrics:
- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix
"""


import os
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


from src.defense.hybrid_defense_v2 import HybridDefenseV2



DATASET_PATH = (
    "data/evaluation/"
    "rag_security_test_cases.csv"
)


RESULT_PATH = (
    "evaluation/results/"
    "hybrid_evaluation_results.csv"
)



def main():

    print("\nLoading dataset...")

    df = pd.read_csv(DATASET_PATH)


    detector = HybridDefenseV2()


    predictions = []


    print("\nRunning HybridDefenseV2...\n")


    for _, row in df.iterrows():

        result = detector.analyze(
            row["text"]
        )


        prediction = (
            1
            if result["final_decision"] in [
                "BLOCK",
                "REVIEW"
            ]
            else 0
        )


        predictions.append(
            prediction
        )


        print(
            "Text:",
            row["text"]
        )

        print(
            "Expected:",
            row["label"]
        )

        print(
            "Prediction:",
            prediction
        )

        print(
            "Decision:",
            result["final_decision"]
        )

        print("-" * 60)



    df["prediction"] = predictions



    # Save detailed results

    df.to_csv(
        RESULT_PATH,
        index=False
    )


    y_true = df["label"]

    y_pred = df["prediction"]



    print("\n==============================")
    print("Evaluation Results")
    print("==============================\n")


    print(
        "Accuracy:",
        round(
            accuracy_score(
                y_true,
                y_pred
            ),
            4
        )
    )


    print(
        "Precision:",
        round(
            precision_score(
                y_true,
                y_pred
            ),
            4
        )
    )


    print(
        "Recall:",
        round(
            recall_score(
                y_true,
                y_pred
            ),
            4
        )
    )


    print(
        "F1 Score:",
        round(
            f1_score(
                y_true,
                y_pred
            ),
            4
        )
    )


    print("\nConfusion Matrix:")
    print(
        confusion_matrix(
            y_true,
            y_pred
        )
    )


    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            y_pred
        )
    )


    print(
        "\nSaved:",
        RESULT_PATH
    )



if __name__ == "__main__":

    main()