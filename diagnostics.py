
import pandas as pd
import numpy as np
import time
import subprocess
import os
import json
import pickle

# Load config.json and get environment variables
with open('config.json', 'r') as f:
    config = json.load(f)

dataset_csv_path = config['output_folder_path']
test_data_path = config['test_data_path']
prod_deployment_path = config['prod_deployment_path']
output_folder_path = config['output_folder_path']


# Function to get model predictions
def model_predictions():
    # read the deployed model and a test dataset, calculate predictions
    model_pkl_file = "trainedmodel.pkl"
    with open(os.path.join(prod_deployment_path, model_pkl_file), "rb") as f:
        deployed_model = pickle.load(f)
    test_data = test_data = pd.read_csv(test_data_path + "/" + "testdata.csv")
    X = np.array(test_data[["lastmonth_activity",
                            "lastyear_activity",
                            "number_of_employees"]]).reshape(-1, 3)
    y = np.array(test_data["exited"])
    predictions = deployed_model.predict(X)
    print("Predictions: ", predictions)
    return predictions, y


# Function to get summary statistics
def dataframe_summary():
    final_data_file = "finaldata.csv"
    # calculate summary statistics here
    final_data_path = os.path.join(output_folder_path, final_data_file)
    mydata = pd.read_csv(final_data_path)
    summary_stats = []
    for col in mydata.columns:
        if np.issubdtype(mydata[col].dtype, np.number):
            mean_value = mydata[col].mean()
            median_value = mydata[col].median()
            std_value = mydata[col].std()
            summary_stats.append((mean_value, median_value, std_value))
    print("summary_stats: ", summary_stats)
    return summary_stats


# Function to check the missing data
def calculate_na_percentage():
    final_data_file = "finaldata.csv"
    #calculate summary statistics here
    final_data_path = os.path.join(output_folder_path, final_data_file)
    mydata = pd.read_csv(final_data_path)
    na_percentages = []
    for col in mydata.columns:
        na_percentage = mydata[col].isna().mean() * 100
        na_percentages.append((col, na_percentage))
    print("na_percentages: ", na_percentages)            
    return na_percentages   


# Function to get timings
def execution_time():
    # calculate timing of training.py and ingestion.py
    scripts = ["ingestion.py", "training.py"]
    execution_times = []
    for script in scripts:
        start_time = time.time()
        subprocess.call(["python", script])
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append((script, execution_time))
    print("execution_times: ", execution_times)
    return execution_times


# Function to check dependencies
def outdated_packages_list():
    # Read requirements.txt file and extract module names
    with open("requirements.txt", 'r') as f:
        modules = [line.strip().split("==")[0] for line in f]
    
    # Get the currently installed versions:
    installed_versions = []
    for module in modules:
        result = subprocess.run(["pip", "show", module], capture_output=True, text=True)
        output = result.stdout.strip()
        version = next((line.split(":")[1].strip() for line in output.split('\n') if line.startswith('Version:')), None)
        installed_versions.append(version)

    # Get the list of outdated modules
    result = subprocess.run(['pip', 'list', '--outdated', '--format=columns'], capture_output=True, text=True)
    output = result.stdout.strip().split('\n')[2:]
    outdated_modules = {}
    for line in output:
        module_info = line.split()
        module = module_info[0]
        current_version = module_info[1]
        latest_version = module_info[2]
        outdated_modules[module] = {
            "current_version": current_version,
            "latest_version": latest_version
            }
    latest_version_list = []
    for mod, ver in zip(modules, installed_versions):
        if mod in outdated_modules.keys():
            latest_version_list.append(outdated_modules[mod]["latest_version"])
        else:
            latest_version_list.append(ver)

    dependencies_dict = {
        'Module': modules,
        'Installed_Version': installed_versions,
        'Latest_Version': latest_version_list
        }
    dependencies_df = pd.DataFrame(dependencies_dict)
    print(dependencies_df)
    return dependencies_df


if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    calculate_na_percentage()
    execution_time()
    outdated_packages_list()

