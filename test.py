#!/usr/bin/env python 

import re
import os

fileMustStartWith = 'disc'
dataDirectoryName = 'sample_data'
reportFileName = 'report.txt'

def getFilePathsByLocation(directoryName):
    validFilesByLocation = {}

    for subdir, dirs, files in os.walk(directoryName):
        validFiles = [filename for filename in files if filename.startswith(fileMustStartWith)]
        folderName = subdir.split('/')[-1]
        locationName = folderName

        for validfile in validFiles:
            filePath = os.path.join(subdir, validfile)
            # todo: use a differnt key because locationname might not be a valid key
            locationFiles = validFilesByLocation.setdefault(locationName,[])
            locationFiles.append(filePath)

    return validFilesByLocation

def makeReport (filePathsByLocation, reportFileName):
    # clear the file
    reportFile = open(reportFileName, 'w')

    for location in filePathsByLocation:
        filePaths = filePathsByLocation[location]

        for filePath in filePaths:
            # open the file to append new lines
            reportFile = open(reportFileName, 'a')
        
            # todo: do something with this
            readFile = open(filePath, 'r')
            readFile.close()

            with reportFile as out:
                out.writelines('test')
                out.writelines('\n')

    reportFile.close()

filePathsByLocation = getFilePathsByLocation(dataDirectoryName)
makeReport(filePathsByLocation, reportFileName)