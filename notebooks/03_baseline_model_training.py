#!/usr/bin/env python
# coding: utf-8

# # PromptShield-AI
# 
# ## Baseline Model Training
# 
# Research Topic:
# Explainable Hybrid AI Framework for Detecting Prompt Injection Attacks in LLM Agents
# 
# Objective:
# Train and evaluate baseline machine learning models for prompt injection detection.

# In[2]:


import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

import pickle
import os

print("Libraries imported successfully!")


# In[3]:


dataset_path = "../data/processed/clean_prompt_dataset.csv"

df = pd.read_csv(dataset_path)

print("Dataset loaded successfully!")

df.head()


# In[4]:


print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nLabels:")
print(df["label"].value_counts())


# In[5]:


X = df["prompt"]

y = df["label"]


print("Input samples:", len(X))
print("Labels:", y.unique())


# In[6]:


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# In[7]:


tfidf = TfidfVectorizer(
    max_features=5000,
    lowercase=True,
    ngram_range=(1,2)
)


X_train_tfidf = tfidf.fit_transform(X_train)

X_test_tfidf = tfidf.transform(X_test)


print("TF-IDF completed!")

print(
    "Feature size:",
    X_train_tfidf.shape
)


# In[8]:


models = {

    "Logistic Regression":
    LogisticRegression(
        max_iter=1000
    ),


    "Naive Bayes":
    MultinomialNB(),


    "Random Forest":
    RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ),


    "SVM":
    LinearSVC()

}


print("Models created!")


# In[9]:


results = []


for name, model in models.items():

    print("\nTraining:", name)

    model.fit(
        X_train_tfidf,
        y_train
    )


    prediction = model.predict(
        X_test_tfidf
    )


    results.append({

        "Model": name,

        "Accuracy":
        accuracy_score(
            y_test,
            prediction
        ),

        "Precision":
        precision_score(
            y_test,
            prediction
        ),

        "Recall":
        recall_score(
            y_test,
            prediction
        ),

        "F1 Score":
        f1_score(
            y_test,
            prediction
        )

    })


print("\nTraining Completed!")


# In[10]:


results_df = pd.DataFrame(results)

results_df


# In[11]:


os.makedirs(
    "../experiments",
    exist_ok=True
)

results_path = "../experiments/baseline_model_results.csv"

results_df.to_csv(
    results_path,
    index=False
)

print("Baseline model results saved!")
print("Saved to:", results_path)


# In[12]:


plt.figure(figsize=(8,5))

plt.bar(
    results_df["Model"],
    results_df["F1 Score"]
)

plt.xticks(rotation=45)

plt.title(
    "Baseline Model F1 Score Comparison"
)

plt.ylabel(
    "F1 Score"
)

plt.show()


# In[13]:


best_model_name = (
    results_df
    .sort_values(
        "F1 Score",
        ascending=False
    )
    .iloc[0]["Model"]
)


print(
    "Best Model:",
    best_model_name
)


# In[14]:


best_model = models[best_model_name]


os.makedirs(
    "../models_saved",
    exist_ok=True
)


with open(
    "../models_saved/best_prompt_model.pkl",
    "wb"
) as file:

    pickle.dump(
        best_model,
        file
    )


with open(
    "../models_saved/tfidf_vectorizer.pkl",
    "wb"
) as file:

    pickle.dump(
        tfidf,
        file
    )


print("Model saved successfully!")


# In[15]:


print("========== Training Summary ==========")

print(
    "Best Model:",
    best_model_name
)

print(
    "Dataset Size:",
    len(df)
)

print(
    "Models Tested:",
    len(models)
)

print(
    "Training Pipeline Completed!"
)

