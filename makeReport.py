#!/usr/bin/env python 

import re
import os

fileMustStartWith = 'disc'
dataDirectoryName = 'sample_data'
reportFileName = 'report.txt'
# validate if needed
dataLineValidator = '.*'

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

def formatDataLine (line):
    # todo update to correct formatting
    if not re.match(dataLineValidator, line):
        return ''

    formatedLine = re.sub('\s+', ',', line)
    return formatedLine + '\n'

def makeReport (filePathsByLocation, reportFileName):
    # clear the file
    reportFile = open(reportFileName, 'w').close()

    # todo: break into smaller functions
    for location in filePathsByLocation:
        filePaths = filePathsByLocation[location]

        for filePath in filePaths:
            # open the file to append new lines
            readFile = open(filePath, 'r')
            for line in readFile:
                reportFile = open(reportFileName, 'a')
                with reportFile as out:
                    formattedLine = formatDataLine(line)
                    out.writelines(formattedLine)
                reportFile.close()

            readFile.close()

filePathsByLocation = getFilePathsByLocation(dataDirectoryName)
makeReport(filePathsByLocation, reportFileName)