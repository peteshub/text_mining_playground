import sqlite3
import pandas as pd
import nltk
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split

from textblob import Word
from textblob import TextBlob

import re

def ml_pipeline(df):
    '''
    Creates Pipeline:
    1) Vectorizer -> TFIDF
    2) TruncatedSVD from the TFIDF
    3) SVC Support Vector Machine with linear kernel
    '''

    X = df['paragraph']
    y = df['class']
    X_train, X_test, y_train, y_test = train_test_split( \
        X, y, test_size=0.3)

    ''' TFIDF + SVC Pipeline '''
    # Principal components (SVD) set to 230 (based on GridSearchCV)
    # features 1500
    # ncomponents 500
    clf = Pipeline([ \
        ("vect", TfidfVectorizer(max_features=1500, stop_words="english", binary=True, sublinear_tf=True)), \
        ("svd", TruncatedSVD(n_components=500, n_iter=10)), \
        ("svc", SVC(C=1, kernel="linear", probability=True)) \
        ])

    clf_fit = clf.fit(X_train, y_train)

    # grid_search_tuning(clf, X_train, y_train)

    return clf_fit, clf, X_train, y_train, X_test, y_test


def txt_preprocessing(df):
    ''' some text preprocessing '''

    def to_token(text):
        return [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]

    def join_to_string(token):
        return " ".join(token)

    def letters_only(tokens):
        return [token for token in tokens if re.search('[a-zA-Z]', token)]

    def lemmatize(tokens):
        return [Word(token).lemmatize() for token in tokens]

    def spelling_correction(tokens):
        return [Word(token).correct() for token in tokens]

    def remove_punctuation(text):
        return

    df["paragraph"] = df.paragraph.apply(to_token)  # Tokenizes everything for text processing
    df["paragraph"] = df.paragraph.apply(letters_only) # NOT WORKING SO WELL
    df["paragraph"] = df.paragraph.apply(lemmatize)  # Seems to improve classifier
    df["length"] = df.paragraph.apply(len)
    # df["paragraph"] = df.paragraph.apply(spelling_correction) # Takes tremendous amount of time to run
    df["paragraph"] = df.paragraph.apply(join_to_string)  # Rejoin tokens to string

    return df


conn = sqlite3.connect('paragraphs.db')

data_set = pd.read_sql("Select p.*,pc.section from paragraph as p join page_classes pc "
                 "on p.page = pc.page and "
                 "p.company = pc.company and "
                 "p.year = pc.year",conn)

le = LabelEncoder()
data_set['class'] = le.fit_transform(data_set.loc[:,'section'])

data_set = txt_preprocessing(data_set)

data_set2 = data_set.loc[data_set.length>10,:]


clf_fit, clf, X_train, y_train, X_test, y_test  = ml_pipeline(data_set2.loc[:10000,:])

clf_fit.score(X_test,y_test)