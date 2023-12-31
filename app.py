"""
Script for running the flask app
author: George Christodoulou
Date: 07/07/23
"""

import json
from flask import Flask, request
from diagnostics import (
    model_predictions,
    dataframe_summary,
    calculate_na_percentage,
)
from scoring import score_model


# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = "1652d576-484a-49fd-913a-6879acfa6ba4"

with open("config.json", "r") as f:
    config = json.load(f)

dataset_csv_path = config["output_folder_path"]

prediction_model_path = config["output_model_path"]


# Prediction Endpoint
@app.route("/prediction", methods=["GET", "POST", "OPTIONS"])
def predict():
    """call the prediction function you created in Step 3

    Returns:
        str: the predictions
    """
    if request.method == "GET":
        data_path = request.args.get("datapath")
    elif request.method == "POST":
        data_path = request.form.get("datapath")
    else:
        return "Method not allowed", 405
    predictions, _ = model_predictions(data_path)
    return str(predictions), 200


# Scoring Endpoint
@app.route("/scoring", methods=["GET", "OPTIONS"])
def stats_1():
    """check the score of the deployed model

    Returns:
        str: score of model
    """

    f1 = score_model()
    return str(f1), 200


# Summary Statistics Endpoint
@app.route("/summarystats", methods=["GET", "OPTIONS"])
def stats_2():
    """check means, medians, and modes for each column

    Returns:
        str: summary_stats
    """
    summary_stats = dataframe_summary()
    return str(summary_stats), 200


# Diagnostics Endpoint
@app.route("/diagnostics", methods=["GET", "OPTIONS"])
def stats_3():
    """check timing and percent NA values

    Returns:
        _type_: _description_
    """

    na_percentages = calculate_na_percentage()
    return na_percentages, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True, threaded=True)
