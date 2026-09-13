import os
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)

from src.defense.prompt_filter import PromptFilter


DATA_PATH = "data/processed/prompt_dataset_dev.csv"
OUTPUT_PATH = "experiments/rule_based_cross_validation_results.csv"

N_SPLITS = 5
RANDOM_STATE = 42


# =========================
# Load Dataset
# =========================

df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["label"]
detector = PromptFilter()



# =========================
# Stratified 5-Fold CV
# =========================

skf = StratifiedKFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_STATE
)

results = []


for fold, (_, val_idx) in enumerate(skf.split(X, y), start=1):

    X_val = X.iloc[val_idx]
    y_val = y.iloc[val_idx]

    predictions = []

    for prompt in X_val:

        detector = PromptFilter()

        result = detector.analyze(prompt)
        

    

        # Existing rule-based detector
        # risk_score > 0 means suspicious/injection
        prediction = 1 if result["risk_score"] > 0 else 0

        predictions.append(prediction)

    accuracy = accuracy_score(y_val, predictions)

    precision = precision_score(
        y_val,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_val,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_val,
        predictions,
        zero_division=0
    )

    results.append({
        "fold": fold,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    })

    print(
        f"Fold {fold}: "
        f"Accuracy={accuracy:.4f}, "
        f"Precision={precision:.4f}, "
        f"Recall={recall:.4f}, "
        f"F1={f1:.4f}"
    )


# =========================
# Save Results
# =========================

results_df = pd.DataFrame(results)

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)

results_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# =========================
# Summary
# =========================

metrics = ["accuracy", "precision", "recall", "f1"]

print("\n" + "=" * 60)
print("RULE-BASED 5-FOLD CROSS-VALIDATION SUMMARY")
print("=" * 60)

for metric in metrics:

    mean = results_df[metric].mean()
    std = results_df[metric].std()

    print(
        f"{metric.capitalize():10s}: "
        f"{mean:.4f} ± {std:.4f}"
    )


print("\nResults saved to:")
print(OUTPUT_PATH)