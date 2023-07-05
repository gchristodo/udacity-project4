from flask import Flask, session, jsonify, request
import pandas as pd
import numpy as np
import pickle
import os
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from ingestion import create_output_folder
import json
import shutil



# Load config.json and correct path variable
with open('config.json', 'r') as f:
    config = json.load(f) 

dataset_csv_path = config['output_folder_path'] 
prod_deployment_path = config['prod_deployment_path']
model_path = config["output_model_path"]


# function that copies latestscore.txt to deployment directory
def copy_ingestedfiles():
    source_folder = dataset_csv_path
    destination_folder = prod_deployment_path
    file_name = "ingestedfiles.txt"
    source_file_path = os.path.join(source_folder, file_name)
    destination_file_path = os.path.join(destination_folder, file_name)
    shutil.copy(source_file_path, destination_file_path)


def copy_latestscorefile():
    source_folder = os.getcwd()
    destination_folder = prod_deployment_path
    file_name = "latestscore.txt"
    source_file_path = os.path.join(source_folder, file_name)
    destination_file_path = os.path.join(destination_folder, file_name)
    shutil.copy(source_file_path, destination_file_path)    


# function for deployment
def store_model_into_pickle(model_name):
    # copy the latest pickle file, the latestscore.txt value,
    # and the ingestfiles.txt file into the deployment directory
    create_output_folder(prod_deployment_path)
    destination_folder = prod_deployment_path
    source_folder = model_path
    source_file_path = os.path.join(source_folder, model_name)
    destination_file_path = os.path.join(destination_folder, model_name)
    shutil.copy(source_file_path, destination_file_path)    
    copy_ingestedfiles()
    copy_latestscorefile()


if __name__ == "__main__":
    store_model_into_pickle("trainedmodel.pkl")
