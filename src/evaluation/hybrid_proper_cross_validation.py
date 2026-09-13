import os
import re
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


DATA_PATH = "data/processed/prompt_dataset_dev.csv"
OUTPUT_PATH = "experiments/hybrid_proper_cross_validation_results.csv"

RANDOM_STATE = 42
N_SPLITS = 5


# =========================
# Rule Engine
# =========================

class RuleDetector:

    def __init__(self):

        self.patterns = {

            "forget_previous":
                r"(forget|vergiss|vergessen)\s+(all|alles|everything|previous|davor|vorher)",


            "override_instruction":
                r"(override|bypass|disregard|ignore)\s+(instructions|rules|guidelines|previous)",


            "system_extraction":
                r"(hidden|secret|internal)\s+(prompt|instruction|rules)",


            "role_play":
                r"(act\s+as|acting\s+as|role[-\s]?play|fungieren\s+als|stay\s+fully\s+in\s+their\s+roles)",


            "jailbreak_context":
                r"(unrestricted|no\s+rules|without\s+limitations|exploit\s+ai|pwned)",

            "ignore_previous":
                r"ignore\s+(all\s+)?previous\s+instructions",

            "system_prompt":
                r"(show|reveal|print|give)"
                r"\s+(me\s+)?(the\s+)?system\s+prompt",

            "developer_message":
                r"ignore\s+developer\s+message",

            "jailbreak":
                r"(jailbreak|DAN\s+mode|do\s+anything\s+now)",

            "role_override":
                r"you\s+are\s+now\s+",

            "secret_request":
                r"(password|api key|secret|token)"
        }


    def analyze(self, text):

        text = text.lower()

        matches = []

        for name, pattern in self.patterns.items():

            if re.search(pattern, text):

                matches.append(name)


        return {
            "matches": matches,
            "risk": len(matches)
        }



# =========================
# Load Dataset
# =========================

df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["label"]


# =========================
# Hybrid Model
# =========================

skf = StratifiedKFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_STATE
)


results = []


for fold, (train_idx, val_idx) in enumerate(
        skf.split(X, y),
        start=1):


    print("\n" + "="*60)
    print("Fold", fold)
    print("="*60)


    X_train = X.iloc[train_idx]
    X_val = X.iloc[val_idx]

    y_train = y.iloc[train_idx]
    y_val = y.iloc[val_idx]


    # Train SVM inside fold

    svm_model = Pipeline([

        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1,2),
                max_features=10000
            )
        ),

        (
            "classifier",
            SVC(
                kernel="linear",
                probability=False,
                random_state=RANDOM_STATE
            )
        )
    ])


    svm_model.fit(
        X_train,
        y_train
    )


    detector = RuleDetector()


    predictions = []


    for text in X_val:


        rule_result = detector.analyze(text)

        ml_score = svm_model.decision_function(
            [text]
        )[0]


        ml_prediction = 1 if ml_score >= 0 else 0


        # Hybrid Decision Policy
        # Hybrid Decision Policy

        if rule_result["risk"] >= 1:

            final_prediction = 1

        elif ml_score >= 0:

            final_prediction = 1

        else:

            final_prediction = 0


        predictions.append(final_prediction)



    accuracy = accuracy_score(
        y_val,
        predictions
    )

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


    print(
        f"Accuracy={accuracy:.4f}, "
        f"Precision={precision:.4f}, "
        f"Recall={recall:.4f}, "
        f"F1={f1:.4f}"
    )


    results.append({

        "fold": fold,
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1

    })



# =========================
# Save Results
# =========================

results_df = pd.DataFrame(results)


os.makedirs(
    "experiments",
    exist_ok=True
)


results_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\n" + "="*60)
print("HYBRID PROPER CV SUMMARY")
print("="*60)


for metric in [
    "accuracy",
    "precision",
    "recall",
    "f1"
]:

    print(
        f"{metric}: "
        f"{results_df[metric].mean():.4f} ± "
        f"{results_df[metric].std():.4f}"
    )


print("\nSaved:")
print(OUTPUT_PATH)