# -*- coding: utf-8 -*-

# Import packages
import arcpy
import os
import shutil

# Import functions from util
from util import getFormattedException, listGDBs, listFeatureDatasets, arcpyPrint, createFolder

# Import  config variables
from config import PATHS as paths

historicFolder = paths['HISTORIC_FOLDER']
resultsFolder = paths['RESULTS_FOLDER']
toConvertFolder = paths['TO_CONVERT_FOLDER']


# Define functions
def convertGDBsToShapefile():
    convertedGDBs = []
    notConvertedGDBs = []

    try:
        arcpyPrint('MESSAGE', 'Listing only file geodatabases from folder {}...\n'.format(toConvertFolder))

        message, GDBs = listGDBs()

        arcpyPrint('MESSAGE', message)

        for GDB in GDBs:
            GDBName = os.path.splitext(os.path.basename(GDB))[0]

            arcpyPrint('MESSAGE', '--- Working on file geodatabase {} ---\n'.format(GDBName))

            GDBFolder = createFolder(resultsFolder, GDBName)

            arcpyPrint('MESSAGE', 'Listing only feature datasets from file geodatabase {}...\n'.format(GDBName))

            runSuccessfully, featuresDatasetsExists, message, featuresDatasetsNames = listFeatureDatasets(GDB)

            if not runSuccessfully:
                arcpyPrint('ERROR', message)

                continue

            arcpyPrint('MESSAGE', message)

            arcpy.env.overwriteOutput = GDB
            try:
                if featuresDatasetsExists:
                    for featureDatasetName in featuresDatasetsNames:
                        arcpyPrint('MESSAGE', '-- Working on feature dataset {} from file geodatabase {} --\n'.format(
                            featureDatasetName, GDBName))

                        datasetFolder = createFolder(GDBFolder, featureDatasetName)

                        featuresClassesNames = arcpy.ListFeatureClasses(feature_dataset=featureDatasetName)

                        for featureClassName in featuresClassesNames:
                            arcpyPrint('MESSAGE',
                                       '- Working on feature class {} from feature dataset {} in the file geodatabase {} -\n'.format(
                                           featureClassName, featureDatasetName, GDBName))

                            featureClass = os.path.join(GDB, featureDatasetName, featureClassName)

                            shapefile = os.path.join(datasetFolder, featureClassName + '.shp')

                            arcpy.CopyFeatures_management(featureClass, shapefile)

                            arcpyPrint('MESSAGE',
                                       '- Feature classe {} from dataset {} in file geodatabase {} was successfully converted -\n'.format(
                                           featureClassName, featureDatasetName, GDBName))

                        arcpyPrint('MESSAGE',
                                   '-- All feature classes from dataset {} in file geodatabase {} was successfully converted --\n'.format(
                                       featureDatasetName, GDBName))

                else:
                    featuresClassesNames = arcpy.ListFeatureClasses()

                    for featureClassName in featuresClassesNames:
                        arcpyPrint('MESSAGE',
                                   '-- Working on feature class {} in the file geodatabase {} --\n'.format(
                                       featureClassName, GDBName))

                        featureClass = os.path.join(GDB, featureClassName)

                        shapefile = os.path.join(GDBFolder, featureClassName + '.shp')

                        arcpy.CopyFeatures_management(featureClass, shapefile)

                        arcpyPrint('MESSAGE',
                                   '-- Feature classe {} in file geodatabase {} was successfully converted --\n'.format(
                                       featureClassName, GDBName))
                convertedGDBs.append(GDB)

            except:
                formattedException = getFormattedException()
                arcpy.AddError(
                    'There was a problem while converting feature classes from file geodatabase {}\nError:\n{}\n'.format(
                        GDBName, formattedException))
                notConvertedGDBs.append(GDB)

                continue

        message = 'All the features classes from file geodatabases were successfully converted!\n'

        return [True, message, convertedGDBs, notConvertedGDBs]

    except:
        formattedException = getFormattedException()

        message = "There was a problem while converting feature classes to shapefiles.\nError:\n{}\n".format(
            formattedException)

        return [False, message, convertedGDBs, notConvertedGDBs]


def moveGDBsFromCovertFolderToHistoric(convertedGDBs):
    try:
        for convertedGDB in convertedGDBs:
            GDBNameWithExtension = os.path.basename(convertedGDB)
            GDBDest = os.path.join(historicFolder, GDBNameWithExtension)

            shutil.move(convertedGDB, GDBDest)

        message = 'All GDBs which were converted were successfully moved to Historic folder\n'

        return [True, message]

    except:
        formattedException = getFormattedException()

        message = 'There was a problem while moving GDBs from To-Check folder to GDBs-Historic folder.\nError:\n{}\n'.format(
            formattedException)

        return [False, message]


def deleteNotConvertedFolder(notConvertedGDBs):
    try:
        for notConvertedGDB in notConvertedGDBs:
            GDBName = os.path.splitext(os.path.basename(notConvertedGDB))

            foldersNames = os.listdir(resultsFolder)

            for folderName in foldersNames:
                if GDBName == folderName:
                    folder = os.path.join(resultsFolder, folderName)
                    shutil.rmtree(folder)

                    continue

        message = "All folder created for file geodatabases which weren't converted were successfully deleted\n"

        return [True, message]

    except:
        formattedException = getFormattedException()

        message = 'There was a problem while deleting folders from Results folder from not converted GDBs.\nError:\n{}\n'.format(formattedException)

        return [False, message]
