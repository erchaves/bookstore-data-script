#!/usr/bin/env python 

import os
import re

fileMustStartWith = 'disc'
fileDirectoryName = 'sample_data'
reportFileName = 'report.txt'

files = [filename for filename in os.listdir(fileDirectoryName) if filename.startswith(fileMustStartWith)]

for fileName in files:
    
    readFile = open(fileDirectoryName + '/' + fileName, 'r')
    reportFile = open(reportFileName, 'w')

    # print readFile.name
    formattedLines = []

    for line in readFile:
        if re.match('(.*)', line):
            formatedLine = re.sub('\s+', ',', line)
            formattedLines.append(formatedLine)

    with reportFile as out:
        out.writelines(formattedLines)

    readFile.close()
    reportFile.close()