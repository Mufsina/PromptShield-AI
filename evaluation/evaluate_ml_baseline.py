"""
PromptShield-AI

ML Baseline Evaluation

Model:
TF-IDF + LinearSVC

Metrics:
- Accuracy
- Precision
- Recall
- F1-score
"""


import os
import pickle
import pandas as pd


from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)



MODEL_PATH = (
    "models_saved/"
    "best_prompt_model.pkl"
)


VECTORIZER_PATH = (
    "models_saved/"
    "tfidf_vectorizer.pkl"
)


DATASET_PATH = (
    "data/evaluation/"
    "rag_security_test_cases.csv"
)


RESULT_PATH = (
    "evaluation/results/"
    "ml_baseline_results.csv"
)



def main():

    print("\nLoading dataset...")


    df = pd.read_csv(
        DATASET_PATH
    )


    print(
        "Loading ML model..."
    )


    with open(
        MODEL_PATH,
        "rb"
    ) as f:

        model = pickle.load(f)



    with open(
        VECTORIZER_PATH,
        "rb"
    ) as f:

        vectorizer = pickle.load(f)



    predictions = []


    print(
        "\nRunning ML baseline...\n"
    )


    for _, row in df.iterrows():


        text = row["text"]


        X = vectorizer.transform(
            [text]
        )


        score = float(
            model.decision_function(X)[0]
        )


        prediction = int(
            score >= 0.0
        )


        predictions.append(
            prediction
        )


        print(
            "Text:",
            text
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
            "Decision Score:",
            round(score,4)
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
        "ML Baseline Evaluation Results"
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