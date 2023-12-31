"""
Script for training the model
author: George Christodoulou
Date: 07/07/23
"""
import json
import pickle
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from ingestion import create_output_folder


# Load config.json and get path variables
with open("config.json", "r") as f:
    config = json.load(f)

dataset_csv_path = os.path.join(config["output_folder_path"])
model_path = config["output_model_path"]


# Function for training the model
def train_model():
    """A function that trains the model
    """
    cwd = os.getcwd()
    trainingdata = pd.read_csv(cwd + "\\" + dataset_csv_path + "\\" + "finaldata.csv")
    X = trainingdata.loc[
        :, ["lastmonth_activity", "lastyear_activity", "number_of_employees"]
    ].values.reshape(-1, 3)
    y = trainingdata["exited"].values.reshape(-1, 1)
    # use this logistic regression for training
    logit = LogisticRegression(
        C=1.0,
        class_weight=None,
        dual=False,
        fit_intercept=True,
        intercept_scaling=1,
        l1_ratio=None,
        max_iter=100,
        n_jobs=None,
        penalty="l2",
        random_state=0,
        solver="liblinear",
        tol=0.0001,
        verbose=0,
        warm_start=False,
    )

    # fit the logistic regression to your data
    model = logit.fit(X, y)
    # write the trained model to your workspace
    # in a file called trainedmodel.pkl
    create_output_folder(model_path)
    file_path = cwd + "/" + model_path + "/" + "trainedmodel.pkl"
    with open(file_path, "wb") as f:
        pickle.dump(model, f)


if __name__ == "__main__":
    train_model()
