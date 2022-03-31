# -*- coding: utf-8 -*-

# Import packages
import arcpy
import os

# Import util functions
from util import getFormattedException

# Import functions from functions
from functions import convertGDBsToShapefile, moveGDBsFromCovertFolderToHistoric, deleteNotConvertedFolder

# Define main function
def main():
    try:
        runSuccessfully, message, convertedGDBs, notConvertedGDBs = convertGDBsToShapefile()

        if not runSuccessfully:
            raise Exception(message)

        runSuccessfully, message = moveGDBsFromCovertFolderToHistoric(convertedGDBs)

        if not runSuccessfully:
            raise Exception(message)

        runSuccessfully, message = deleteNotConvertedFolder(notConvertedGDBs)

        if not runSuccessfully:
            raise Exception(message)

        return [True, message]

    except:
        formattedException = getFormattedException()

        return [False, 'There was a problem while running function main.\nError:\n{}'.format(formattedException)]


if __name__ == '__main__':
    runSuccessfully, message = main()

    arcpy.AddWarning(message)
