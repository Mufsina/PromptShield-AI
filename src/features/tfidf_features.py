from sklearn.feature_extraction.text import TfidfVectorizer


def create_tfidf_vectorizer():
    """
    Create TF-IDF feature extractor.
    """

    return TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        max_features=10000
    )


def transform_text(vectorizer, train_text, test_text=None):

    X_train = vectorizer.fit_transform(train_text)

    if test_text is not None:
        X_test = vectorizer.transform(test_text)
        return X_train, X_test

    return X_train