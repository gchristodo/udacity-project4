"""
Script for running the scoring during fullprocess
author: George Christodoulou
Date: 07/07/23
"""

import pickle
import os
import json
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score


# Load config.json and get path variables
with open("config.json", "r") as f:
    config = json.load(f)

output_model_path = config["output_model_path"]
output_folder_path = config["output_folder_path"]


# Function for model scoring
def score_model():
    """This function should take a trained model, load test data,
    and calculate an F1 score for the model relative to the test data
    it should write the result to the latestscore.txt file

    Returns:
    float   : f1 score
    """

    modelname = "trainedmodel.pkl"
    with open(os.path.join(output_model_path, modelname), "rb") as f:
        model = pickle.load(f)

    test_data = pd.read_csv(output_folder_path + "/" + "finaldata.csv")
    X = np.array(
        test_data[["lastmonth_activity",
                   "lastyear_activity",
                   "number_of_employees"]]
    ).reshape(-1, 3)
    y = np.array(test_data["exited"])
    predictions = model.predict(X)
    f1 = f1_score(predictions, y)
    print(f1)
    with open("latestscore.txt", "w") as f:
        f.write(str(f1))
    return float(f1)


if __name__ == "__main__":
    score_model()
