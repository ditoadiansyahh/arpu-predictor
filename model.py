import pandas as pd
import numpy as np
import pickle
from sklearn.externals import joblib


def read_without_column(csv):
    df = pd.read_csv(csv)
    return df


def read_with_column(csv, cols):
    df = pd.read_csv(csv, names=cols)
    return df


def cleaning(lst):
    cleaned = [float(i) for i in lst]
    cleaned = np.array(lst).reshape(1, -1)
    return cleaned


# Classifier
def rf_prediction():
    rf = pickle.load(open('static/pickle/rf.pkl', 'rb'))
    return rf
