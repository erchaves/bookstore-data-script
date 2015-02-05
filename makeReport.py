#!/usr/bin/env python 
import re
import os

# variable settings
shouldFilterZeroValues = True
datdDirectoryPath = 'process_home'
reportFilePath = 'report.csv'
reportFields = ['date','locationName','discountType','quantity','amount']
reportHeaders = ['Date,Location,Discount Type,Quantity,Amount']
dateRegex = '\d\d_\d\d_\d\d'
dateSearchRegex = '^.*('+dateRegex+').*$'
# only process files that will be in the expected format
fileNameValidator = '^disc.*'+dateRegex+'$'
# add validation regex for data rows if desired.
dataRowValidator = None
# The specfic character ranges occupied by each field in a data row
dataFieldCharRanges = {
    'discountType': [0,20],
    'quantity': [21,27],
    'amount': [28,37],
}

def getfileMetaDataArr(directoryName):
    fileMetaDataArr = []

    for subdir, dirs, files in os.walk(directoryName):
        validFiles = [filename for filename in files if re.match(fileNameValidator, filename)]
        folderName = subdir.split('/')[-1]
        locationName = folderName
        
        for validfile in validFiles:
            filePath = os.path.join(subdir, validfile)
            dateSearch = re.search(dateSearchRegex, validfile)
            dateMatch = dateSearch.group(1)
            fileMetaDataArr.append({
                'date': dateMatch.replace('_','/'),
                'filePath': filePath,
                'locationName': locationName,
            })

    return fileMetaDataArr

def formatDataRow (line, fileMetaData):
    if dataRowValidator and not re.match(dataRowValidator, line):
        return ''

    fileRowData = parseDataRow(line)
    dataDict = dict(fileRowData.items() + fileMetaData.items())

    if shouldFilterZeroValues:
        hasZeros = not (float(dataDict['quantity']) and float(dataDict['amount']))
        if hasZeros:
            return ''

    fields = [dataDict[field] for field in reportFields]
    formattedLine = ','.join(map(str, fields))
    return formattedLine

# parses a line of raw data in a specific format where each field holds a set number of chars
# Example of a row 'A Field..........10% 000014  000003421'
def parseDataRow (line):
    dataFields = {}
    for key in dataFieldCharRanges:
        range = dataFieldCharRanges[key]
        field = line[range[0]:range[1]]
        dataFields[key] = field
    return dataFields

def writeLinesToReport (lines):
    reportFile = open(reportFilePath, 'a')
    with reportFile as out:
        for line in lines:
            if line:
                out.writelines(line + '\n')
    reportFile.close()

def makeCsvReport (fileMetaDataArr):
    # first clear the file
    reportFile = open(reportFilePath, 'w').close()

    # write a header line
    headerLine = ','.join(map(str, reportHeaders))
    writeLinesToReport([headerLine])

    # write the rest of the lines
    for fileMetaData in fileMetaDataArr:
        filePath = fileMetaData['filePath']
        readFile = open(filePath, 'r')
        formattedLines = [formatDataRow(line, fileMetaData) for line in readFile]
        writeLinesToReport(formattedLines)
        readFile.close()

if __name__ == "__main__":
    fileMetaDataArr = getfileMetaDataArr(datdDirectoryPath)
    makeCsvReport(fileMetaDataArr)
