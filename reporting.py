import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from diagnostics import model_predictions


# Load config.json and get path variables
with open('config.json', 'r') as f:
    config = json.load(f)

model_path = config["output_model_path"]
confusion_matrix_plot = config["confusion_matrix_plot"]


# Function for reporting
def model_report(filename):
    # calculate a confusion matrix using the test data and the deployed model
    # write the confusion matrix to the workspace
    predictions, y = model_predictions()
    cm = confusion_matrix(y, predictions)

    # CM Plot
    class_labels = ["0", "1"]

    fig, ax = plt.subplots()
    sns.heatmap(cm,
                annot=True,
                fmt='d',
                cmap='Blues',
                cbar=False,
                xticklabels=class_labels,
                yticklabels=class_labels,
                ax=ax
                )
    ax.set_xlabel('Predicted')
    ax.set_ylabel('True')

    ax.set_title("Confusion Matrix")
    plt.savefig(model_path +
                "/" + filename)


if __name__ == '__main__':
    model_report(confusion_matrix_plot)
