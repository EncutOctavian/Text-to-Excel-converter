import pandas as pd
import sys


def dataFrameCreator(lineList):
    dataFrame = {}
    header = {0: 'Signal', 1: 'Value', 2: 'Resolution', 3: 'Unit', 4: 'Information'}
    for element in range(len(lineList[1])):
        for line in lineList:
            if header[element] not in dataFrame:
                dataFrame[header[element]] = list()
            dataFrame[header[element]].append(line[element])
    return dataFrame


def excelWriter(file, lineList):
    dataFrame = dataFrameCreator(lineList)
    output = pd.DataFrame(dataFrame)
    output.index += 1
    output.to_excel(file, index_label='ID')


def getAndProcessData(file):
    lineList = []
    with open(file) as f:
        lines = f.readlines()
    for line in lines:
        lineList.append(line.split(';'))
        lineList[-1].remove(lineList[-1][-1])
    return lineList


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
    linesList = getAndProcessData(inputFile)
    excelWriter(outputFile, linesList)
