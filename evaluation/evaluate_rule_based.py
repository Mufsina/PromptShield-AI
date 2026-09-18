"""
PromptShield-AI

Rule-Based Baseline Evaluation

Uses:
PromptFilter only

Metrics:
- Accuracy
- Precision
- Recall
- F1-score
"""


import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)


from src.defense.prompt_filter import PromptFilter



DATASET_PATH = (
    "data/evaluation/"
    "rag_security_test_cases.csv"
)


RESULT_PATH = (
    "evaluation/results/"
    "rule_based_evaluation_results.csv"
)



def main():

    print("\nLoading dataset...")


    df = pd.read_csv(
        DATASET_PATH
    )


    detector = PromptFilter()


    predictions = []


    print(
        "\nRunning Rule-Based Detector...\n"
    )


    for _, row in df.iterrows():


        result = detector.analyze(
            row["text"]
        )


        # Rule decision mapping
        #
        # BLOCK / REVIEW = Attack
        # ALLOW = Safe

        prediction = (
            1
            if result["decision"]
            in [
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
            result["decision"]
        )

        print(
            "Patterns:",
            result["matched_patterns"]
        )

        print("-" * 60)



    df["prediction"] = predictions



    df.to_csv(
        RESULT_PATH,
        index=False
    )



    y_true = df["label"]

    y_pred = df["prediction"]



    print(
        "\n=============================="
    )

    print(
        "Rule-Based Evaluation Results"
    )

    print(
        "==============================\n"
    )



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



    print(
        "\nConfusion Matrix:"
    )

    print(
        confusion_matrix(
            y_true,
            y_pred
        )
    )



    print(
        "\nClassification Report:"
    )

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