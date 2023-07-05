from flask import Flask, session, jsonify, request
from diagnostics import (model_predictions,
                         dataframe_summary,
                         execution_time,
                         calculate_na_percentage,
                         outdated_packages_list)
from scoring import score_model
import json



# Set up variables for use in our script
app = Flask(__name__)
app.secret_key = '1652d576-484a-49fd-913a-6879acfa6ba4'

with open('config.json', 'r') as f:
    config = json.load(f) 

dataset_csv_path = config['output_folder_path']

prediction_model_path = config["output_model_path"]


# Prediction Endpoint
@app.route("/prediction", methods=['POST', 'OPTIONS'])
def predict(data_path):
    # call the prediction function you created in Step 3

    predictions, _ = model_predictions(data_path)
    return str(predictions)


# Scoring Endpoint
@app.route("/scoring", methods=['GET', 'OPTIONS'])
def stats_1():
    # check the score of the deployed model

    f1 = score_model()
    return str(f1)


# Summary Statistics Endpoint
@app.route("/summarystats", methods=['GET', 'OPTIONS'])
def stats_2():
    # check means, medians, and modes for each column
    summary_stats = dataframe_summary()
    return str(summary_stats)


# Diagnostics Endpoint
@app.route("/diagnostics", methods=['GET', 'OPTIONS'])
def stats_3():
    # check timing and percent NA values

    na_percentages = calculate_na_percentage()
    return na_percentages


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True, threaded=True)
