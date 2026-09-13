"""
PromptShield-AI
Baseline Machine Learning Models

Contains reusable baseline classifiers
for prompt injection detection experiments.
"""


from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC



def get_baseline_models(random_state=42):

    """
    Return baseline ML models.

    Models:
    - Logistic Regression
    - Multinomial Naive Bayes
    - Random Forest
    - Linear SVM
    """


    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=2000,
                random_state=random_state
            ),


        "Naive Bayes":
            MultinomialNB(),


        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,
                random_state=random_state,
                n_jobs=-1
            ),


        "SVM":
            LinearSVC(
                random_state=random_state
            )
    }


    return models