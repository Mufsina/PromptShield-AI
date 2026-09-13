import os
import pickle
import pandas as pd

from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split

from src.features.tfidf_features import (
    create_tfidf_vectorizer,
    transform_text
)


DATA_PATH = "data/processed/prompt_dataset_dev.csv"

MODEL_PATH = "models_saved/best_prompt_model.pkl"
VECTORIZER_PATH = "models_saved/tfidf_vectorizer.pkl"


RANDOM_STATE = 42


def train_svm():

    print("=" * 60)
    print("PromptShield-AI SVM Training Pipeline")
    print("=" * 60)


    # Load dataset

    df = pd.read_csv(DATA_PATH)

    X = df["text"]
    y = df["label"]


    print("\nDataset:")
    print(df.shape)

    print("\nLabels:")
    print(y.value_counts())


    # Train-test split

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y
    )


    # TF-IDF

    vectorizer = create_tfidf_vectorizer()

    X_train_tfidf, X_test_tfidf = transform_text(
        vectorizer,
        X_train,
        X_test
    )


    print("\nTF-IDF:")
    print(X_train_tfidf.shape)


    # SVM

    model = LinearSVC(
        random_state=RANDOM_STATE
    )


    model.fit(
        X_train_tfidf,
        y_train
    )


    print("\nTraining completed!")


    # Save model

    os.makedirs(
        "models_saved",
        exist_ok=True
    )


    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)


    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)


    print("\nSaved:")
    print(MODEL_PATH)
    print(VECTORIZER_PATH)


if __name__ == "__main__":

    train_svm()