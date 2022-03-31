# -*- coding: utf-8 -*-

# Import packages
import arcpy
import os
import sys
import traceback
import shutil

# Import config variables
from config import PATHS as paths
historicFolder = paths['HISTORIC_FOLDER']
resultsFolder = paths['RESULTS_FOLDER']
toConvertFolder = paths['TO_CONVERT_FOLDER']


# Define util functions
def getFormattedException():
    excType, excValue, excTb = sys.exc_info()
    formattedException = traceback.format_exception(excType, excValue, excTb)

    return '\n'.join(formattedException)


def arcpyPrint(type, message):
    if type == 'ERROR':
        arcpy.AddError(message)

    elif type == 'WARNING':
        arcpy.AddWarning(message)

    elif type == 'MESSAGE':
        arcpy.AddMessage(message)

    else:
        raise Exception('There are only 3 options for type argument:\n "ERROR", "WARNING" and "MESSAGE"\n')

    return True


def listGDBs():
    filesNames = os.listdir(toConvertFolder)

    GDBs = []
    for fileName in filesNames:
        extension = os.path.splitext(fileName)[1]

        if extension == '.gdb':
            file = os.path.join(toConvertFolder, fileName)
            GDBs.append(file)

    message = 'All file geodatabases were successfully listed!\n'

    return [message, GDBs]


def createFolder(dir, folderName):
    folderToCreate = os.path.join(dir, folderName)

    if os.path.exists(folderToCreate):
        shutil.rmtree(folderToCreate)

    os.makedirs(folderToCreate)

    return folderToCreate


def listFeatureDatasets(gdb):
    featuresDatasetsExists = False

    try:
        arcpy.env.workspace = gdb

        gdbName = os.path.splitext(os.path.basename(gdb))[0]

        featureDatasetsNames = arcpy.ListDatasets('*', 'Feature')

        if len(featureDatasetsNames) == 0:
            message = 'There is no dataset in the file geodatabase {}\n'.format(gdbName)

            return [False, featuresDatasetsExists, message, featureDatasetsNames]

        featuresDatasetsExists = True

        featuresDatasetsNames = []
        for featureDatasetName in featureDatasetsNames:
            dataset = os.path.join(gdb, featureDatasetName)

            datasetType = arcpy.Describe(dataset).datasetType

            if datasetType == 'FeatureDataset':
                featuresDatasetsNames.append(featureDatasetName)

        message = 'The datasets from file geodatabase {} were successfully listed\n'.format(gdbName)

        return [True, featuresDatasetsExists, message, featuresDatasetsNames]

    except:
        formattedException = getFormattedException()

        message = 'There was a problem while listing datasets.\nError:\n{}\n'.format(formattedException)

        return [False, featuresDatasetsExists, message, '']




