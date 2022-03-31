# -*- coding: utf-8 -*-

# Import packages
import os

# Define config variables
absFolder = os.path.dirname(os.path.abspath(__file__))

PATHS = {
    "HISTORIC_FOLDER": os.path.join(absFolder, "GDBs-Historic"),
    "RESULTS_FOLDER": os.path.join(absFolder, "Results"),
    "TO_CONVERT_FOLDER": os.path.join(absFolder, "To-Convert")
}




