"""
PromptShield-AI

Final Experimental Comparison

Compares:
1. Rule-based
2. TF-IDF + LinearSVC
3. HybridDefenseV2
"""


import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)



DATASETS = {

    "Rule-based PromptFilter":
    "evaluation/results/rule_based_evaluation_results.csv",

    "TF-IDF + LinearSVC":
    "evaluation/results/ml_baseline_results.csv",

    "HybridDefenseV2":
    "evaluation/results/hybrid_evaluation_results.csv"

}



OUTPUT_PATH = (
    "evaluation/results/"
    "final_comparison.csv"
)



def calculate_metrics(path):

    df = pd.read_csv(path)


    y_true = df["label"]

    y_pred = df["prediction"]


    return {

        "Accuracy":
            round(
                accuracy_score(
                    y_true,
                    y_pred
                ),
                4
            ),

        "Precision":
            round(
                precision_score(
                    y_true,
                    y_pred
                ),
                4
            ),

        "Recall":
            round(
                recall_score(
                    y_true,
                    y_pred
                ),
                4
            ),

        "F1-score":
            round(
                f1_score(
                    y_true,
                    y_pred
                ),
                4
            )
    }



def main():


    results = []


    for name, path in DATASETS.items():

        metrics = calculate_metrics(path)

        metrics["Method"] = name

        results.append(metrics)



    result_df = pd.DataFrame(results)


    result_df = result_df[
        [
            "Method",
            "Accuracy",
            "Precision",
            "Recall",
            "F1-score"
        ]
    ]


    print(
        "\nFinal Experimental Comparison\n"
    )


    print(
        result_df.to_string(
            index=False
        )
    )


    result_df.to_csv(
        OUTPUT_PATH,
        index=False
    )


    print(
        "\nSaved:",
        OUTPUT_PATH
    )



if __name__ == "__main__":

    main()