import os
import pandas as pd

from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier


# =========================
# Configuration
# =========================

DATA_PATH = "data/processed/prompt_dataset_dev.csv"
OUTPUT_PATH = "experiments/cross_validation_results.csv"

RANDOM_STATE = 42
N_SPLITS = 5


# =========================
# Load Dataset
# =========================

df = pd.read_csv(DATA_PATH)

X = df["text"]
y = df["label"]


# =========================
# Models
# =========================

models = {
    "SVM": Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )),
        ("classifier", SVC(kernel="linear", random_state=RANDOM_STATE))
    ]),

    "Logistic Regression": Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )),
        ("classifier", LogisticRegression(
            max_iter=2000,
            random_state=RANDOM_STATE
        ))
    ]),

    "Naive Bayes": Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )),
        ("classifier", MultinomialNB())
    ]),

    "Random Forest": Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            max_features=10000
        )),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=RANDOM_STATE,
            n_jobs=-1
        ))
    ])
}


# =========================
# Stratified 5-Fold CV
# =========================

skf = StratifiedKFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_STATE
)

results = []


for model_name, model in models.items():

    print("\n" + "=" * 60)
    print(model_name)
    print("=" * 60)

    fold_scores = []

    for fold, (train_idx, val_idx) in enumerate(
        skf.split(X, y), start=1
    ):

        X_train = X.iloc[train_idx]
        X_val = X.iloc[val_idx]

        y_train = y.iloc[train_idx]
        y_val = y.iloc[val_idx]

        # Train
        model.fit(X_train, y_train)

        # Predict
        y_pred = model.predict(X_val)

        # Metrics
        accuracy = accuracy_score(y_val, y_pred)

        precision = precision_score(
            y_val,
            y_pred,
            zero_division=0
        )

        recall = recall_score(
            y_val,
            y_pred,
            zero_division=0
        )

        f1 = f1_score(
            y_val,
            y_pred,
            zero_division=0
        )

        fold_scores.append({
            "model": model_name,
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

    # Add fold results
    results.extend(fold_scores)


# =========================
# Save Fold Results
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

summary = (
    results_df
    .groupby("model")[["accuracy", "precision", "recall", "f1"]]
    .agg(["mean", "std"])
    .round(4)
)

print("\n" + "=" * 60)
print("5-FOLD CROSS-VALIDATION SUMMARY")
print("=" * 60)

print(summary)

print("\nResults saved to:")
print(OUTPUT_PATH)