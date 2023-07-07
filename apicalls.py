"""
Script for making apicalss
author: George Christodoulou
Date: 07/07/23
"""
import subprocess
import json
import requests


# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1"
with open("config.json", "r") as f:
    config = json.load(f)

output_model_path = config["output_model_path"]
apireturns_txt = config["apireturns_txt"]

# Call each API endpoint and store the responses
RESPONSE1 = subprocess.run(["curl", URL + ":8000/scoring"], capture_output=True).stdout
RESPONSE2 = subprocess.run(
    ["curl", URL + ":8000/summarystats"], capture_output=True
).stdout
RESPONSE3 = subprocess.run(
    ["curl", URL + ":8000/diagnostics"], capture_output=True
).stdout
RESPONSE4 = requests.get(
    URL + ":8000/prediction?datapath=testdata/testdata.csv"
).content

# combine all API responses
RESPONSES = (
    str(RESPONSE1)
    + "\n"
    + str(RESPONSE2)
    + "\n"
    + str(RESPONSE3)
    + "\n"
    + str(RESPONSE4)
)

# write the responses to your workspace
with open(output_model_path + "/" + apireturns_txt, "w") as f:
    f.write(RESPONSES)
