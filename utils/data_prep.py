from sklearn.preprocessing import LabelEncoder
import sqlite3
import pandas as pd


def get_dataset():
    conn = sqlite3.connect('paragraphs.db')

    data_set = pd.read_sql("Select p.*,pc.section from paragraph as p join page_classes pc "
                           "on p.page = pc.page and "
                           "p.company = pc.company and "
                           "p.year = pc.year", conn)

    le = LabelEncoder()
    data_set['class'] = le.fit_transform(data_set.loc[:, 'section'])

    return data_set
