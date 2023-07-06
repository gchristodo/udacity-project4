import pandas as pd
import numpy as np
import os
import json
from datetime import datetime


# Load config.json and get input and output paths
with open('config.json', 'r') as f:
    config = json.load(f) 

input_folder_path = config['input_folder_path']
output_folder_path = config['output_folder_path']


def view_folder_content(folder_path):
    cwd = os.getcwd()
    entries = os.listdir(cwd + "/" + folder_path)
    my_entries = []
    for entry in entries:
        my_entries.append(cwd + "/" + folder_path + "/" + entry)
    return my_entries


def create_output_folder(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder {folder_path} created successfully.")
    else:
        print(f"Folder {folder_path} already exists.")


# Function for data ingestion
def merge_multiple_dataframe():
    # check for datasets, compile them together, and write to an output file
    file_paths = view_folder_content(input_folder_path)
    print(file_paths)
    dataframe = pd.DataFrame()
    csv_files = []
    for entry in file_paths:
        if entry.split(".")[-1] == "csv":
            tmp_df = pd.read_csv(entry)
            csv_files.append(entry.split("/")[-1])
            
        else:
            pass
        dataframe = dataframe.append(tmp_df)
    with open(output_folder_path + "/" + "ingestedfiles.txt", "w") as f:
        f.write("\n".join(csv_files))
    print("ingestedfiles.txt created successfully")
    dataframe = dataframe.drop_duplicates()
    dataframe = dataframe.reset_index(drop=True)
    create_output_folder(output_folder_path)
    dataframe.to_csv(output_folder_path + "/" + "finaldata.csv")   


if __name__ == '__main__':
    merge_multiple_dataframe()
