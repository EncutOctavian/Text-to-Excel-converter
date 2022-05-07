import pandas as pd


def dataFrameCreator(linesList):
    dataFrame = {}
    header = {0: 'Signal', 1: 'Value', 2: 'Resolution', 3: 'Unit', 4: 'Information'}
    for element in range(len(linesList[1])):
        for line in linesList:
            if header[element] not in dataFrame:
                dataFrame[header[element]] = list()
            dataFrame[header[element]].append(line[element])
    return dataFrame


def excelWriter(outputFile, linesList):
    dataFrame = dataFrameCreator(linesList)
    output = pd.DataFrame(dataFrame)
    output.index += 1
    output.to_excel(outputFile, index_label='ID')


if __name__ == '__main__':
    with open('sample.txt') as f:
        lines = f.readlines()
    linesList = []
    for line in lines:
        linesList.append(line.split(';'))
        linesList[-1].remove(linesList[-1][-1])
    path = 'output.xlsx'
    excelWriter(path, linesList)
