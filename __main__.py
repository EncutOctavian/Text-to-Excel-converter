import pandas as pd
import sys
import json
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

outputFile = ""
inputFile = ""


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


def readFromConfigFile():
    data = {}
    with open("config.json", "r") as f:
        data = json.load(f)
    inputFile = data["inputFile"]
    outputFile = data["outputFile"]
    return inputFile, outputFile


def useGui():
    global outputFile
    global inputFile
    root = tk.Tk()
    root.title("Text to Excel converter")
    canvas = tk.Canvas(root, height=450, width=900, bg="lightblue")
    canvas.grid(columnspan=3, rowspan=4)

    logo = Image.open('Styling/logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo, bg="lightblue")
    logo_label.image = logo
    logo_label.place(x=340, y=50)

    arrow = Image.open('Styling/arrow.png')
    arrow = ImageTk.PhotoImage(arrow)
    arrow_label = tk.Label(image=arrow, bg="lightblue")
    arrow_label.image = arrow
    arrow_label.place(x=425, y=170)

    instructions = tk.Label(root, text="Choose Input File..", bg="lightblue")
    instructions.place(x=150, y=150)

    browse_text1 = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text1, command=lambda: getInputFile(browse_text1),
                           fg="black", height=3, width=15, bd=0)
    browse_text1.set("Browse")
    browse_btn.place(x=125, y=180)

    instructions = tk.Label(root, text="Choose Output File..", bg="lightblue")
    instructions.place(x=625, y=150)

    browse_text2 = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text2, command=lambda: getOutputFile(browse_text2),
                           fg="black", height=3, width=15, bd=0)
    browse_text2.set("Browse")
    browse_btn.place(x=600, y=175)

    browse_text = tk.StringVar()
    browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: guiConverter(root),
                           fg="black", height=3, width=15, bd=0)

    browse_text.set("Convert!")
    browse_btn.place(x=375, y=300)
    root.mainloop()


def getOutputFile(browse):
    global outputFile
    outputFile = filedialog.askopenfilename(title="Choose the output file", initialdir='/',
                                            filetypes=[('Excel files', '*.xlsx')])

    if outputFile != "":
        text = outputFile.split('/')
        text = text[-1]
        browse.set(text)


def getInputFile(browse):
    global inputFile
    inputFile = filedialog.askopenfilename(title="Choose the input file", initialdir='/',
                                           filetypes=[('Text files', '*.txt')])
    if inputFile != "":
        text = inputFile.split('/')
        text = text[-1]
        browse.set(text)


def guiConverter(root):
    if inputFile == "" or outputFile == "":
        root = tk.Tk()
        root.title("Warning!")
        canvas = tk.Canvas(root, height=250, width=500)
        canvas.grid(columnspan=3)
        if inputFile == "" and outputFile != "":
            instructions = tk.Label(root, text="Please select the input file!")
            instructions.place(x=150, y=100)
        elif inputFile != "" and outputFile == "":
            instructions = tk.Label(root, text="Please select the output file!")
            instructions.place(x=150, y=100)
        elif inputFile == "" and outputFile == "":
            instructions = tk.Label(root, text="Please select the files!")
            instructions.place(x=175, y=100)
        root.mainloop()
    else:
        excelWriter(outputFile, getAndProcessData(inputFile))
        root.destroy()
        root = tk.Tk()
        root.title("Text to Excel converter")
        canvas = tk.Canvas(root, height=250, width=500)
        canvas.grid(columnspan=3)
        instructions = tk.Label(root, text="Conversion complete!")
        instructions.place(x=175, y=100)
        root.mainloop()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        inputFile = sys.argv[1]
        outputFile = sys.argv[2]
        linesList = getAndProcessData(inputFile)
        excelWriter(outputFile, linesList)
    else:
        inputFile, outputFile = readFromConfigFile()
        if inputFile == "" or outputFile == "":
            inputFile = ""
            outputFile = ""
            useGui()
        else:
            linesList = getAndProcessData(inputFile)
            excelWriter(outputFile, linesList)
