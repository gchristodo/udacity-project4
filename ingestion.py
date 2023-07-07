"""
Script for running the ingestion
author: George Christodoulou
Date: 07/07/23
"""
import os
import json
import pandas as pd


# Load config.json and get input and output paths
with open("config.json", "r") as f:
    config = json.load(f)

input_folder_path = config["input_folder_path"]
output_folder_path = config["output_folder_path"]


def view_folder_content(folder_path):
    """view_folder_content

    Args:
        folder_path (str): The folder path

    Returns:
        list: list of file paths
    """
    cwd = os.getcwd()
    entries = os.listdir(cwd + "/" + folder_path)
    my_entries = []
    for entry in entries:
        if entry.split(".")[-1] == "csv":
            my_entries.append(cwd + "/" + folder_path + "/" + entry)
    return my_entries


def extract_csv_from_path_list(path_entries):
    """extract_csv_from_path_list

    Args:
        path_entries (list): list of file paths

    Returns:
        list: list of csv
    """
    extracted_csv = []
    for path in path_entries:
        extracted_csv.append(path.split("/")[-1])
    return extracted_csv


def create_output_folder(folder_path):
    """create_output_folder if needed

    Args:
        folder_path (str): folder_path
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
        print(f"Folder {folder_path} created successfully.")
    else:
        print(f"Folder {folder_path} already exists.")


def merge_multiple_dataframe():
    """Function for data ingestion"""
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


if __name__ == "__main__":
    merge_multiple_dataframe()
