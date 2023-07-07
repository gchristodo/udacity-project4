"""
Script for running the reporting
author: George Christodoulou
Date: 07/07/23
"""
import json
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from diagnostics import model_predictions


# Load config.json and get path variables
with open("config.json", "r") as f:
    config = json.load(f)

model_path = config["output_model_path"]
confusion_matrix_plot = config["confusion_matrix_plot"]


def model_report(filename):
    """Function for reporting

    Args:
        filename (str): the file name
    """
    # calculate a confusion matrix using the test data and the deployed model
    # write the confusion matrix to the workspace
    predictions, y = model_predictions()
    cm = confusion_matrix(y, predictions)

    # CM Plot
    class_labels = ["0", "1"]

    fig, ax = plt.subplots()
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        cbar=False,
        xticklabels=class_labels,
        yticklabels=class_labels,
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("True")

    ax.set_title("Confusion Matrix")
    plt.savefig(model_path + "/" + filename)


if __name__ == "__main__":
    model_report(confusion_matrix_plot)
