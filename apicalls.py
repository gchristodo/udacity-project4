import requests
import subprocess
import json

# Specify a URL that resolves to your workspace
URL = "http://127.0.0.1"
with open('config.json', 'r') as f:
    config = json.load(f)

output_model_path = config['output_model_path']
apireturns_txt = config["apireturns_txt"]

# Call each API endpoint and store the responses
response1 = subprocess.run(['curl', URL + ':8000/scoring'], capture_output=True).stdout
response2 = subprocess.run(['curl', URL + ':8000/summarystats'], capture_output=True).stdout
response3 = subprocess.run(['curl', URL + ':8000/diagnostics'], capture_output=True).stdout
response4 = requests.get(URL + ':8000/prediction?datapath=testdata/testdata.csv').content

# combine all API responses
responses = str(response1) + "\n" + str(response2) + "\n" + str(response3) + "\n" + str(response4)

# write the responses to your workspace
with open(output_model_path + "/" + apireturns_txt, "w") as f:
    f.write(responses)

