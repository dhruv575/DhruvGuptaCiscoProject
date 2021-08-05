from PIL import Image, ImageTk

import tkinter as tk
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename

from matplotlib import pyplot as plt

from dateutil.parser import parse

import os

def open_file():
    browseText.set("Loading...")
    #logFileName= askopenfilename(parent=window, mode='rb', title="Choose a file", filetype=[("Log file", "*")])
    logFileName = askopenfilename()
    logFile=open(logFileName, "r")
    if logFile:
        global dir_path
        dir_path = os.path.dirname(logFileName)
        global logFileLines
        logFileLines=logFile.read().splitlines()
        logFile.close()
        browseText.set("Browse")
        canvas = tk.Canvas(window, width=800, height=300)
        canvas.grid(columnspan=3, rowspan=7)
        add_functions()

def add_functions():
    stringSearchButton = tk.Button(window, text="String Search", command=lambda: string_search_open(), font="Raleway", bg="#81bc5a",fg="white", height=2, width=20)
    stringSearchButton.grid(column=0, row=4)

    stringCountButton = tk.Button(window, text="String Count", command=lambda: string_search_open(), font="Raleway",bg="#81bc5a", fg="white", height=2, width=20)
    stringCountButton.grid(column=0, row=5)

    aggregationOperationsButton = tk.Button(window, text="Module Search", command=lambda: string_search_open(), font="Raleway", bg="#81bc5a", fg="white", height=2, width=25)
    aggregationOperationsButton.grid(column=1, row=4)

    deviceSearchButton = tk.Button(window, text="Create Bar Graph", font="Raleway", command=lambda: make_histogram(), bg="#81bc5a", fg="white", height=2, width=25)
    deviceSearchButton.grid(column=1, row=5)

    timestampSearchesButton = tk.Button(window, text="Timestamp Search", command=lambda: time_search_open(), font="Raleway", bg="#81bc5a", fg="white", height=2, width=20)
    timestampSearchesButton.grid(column=2, row=4)

    deviceSearchButton = tk.Button(window, text="Timestamp Count", font="Raleway", command=lambda: time_count_open(),bg="#81bc5a", fg="white", height=2, width=20)
    deviceSearchButton.grid(column=2, row=5)

def string_search_open():

    stringTextLabel = tk.Label(window, text="Enter search request")
    stringTextLabel.grid(column=0, row=6)
    stringSearchEntry = tk.Entry(window)
    stringSearchEntry.grid(column=0, row=7)

    outputTextLabel = tk.Label(window, text="Enter Output File Name")
    outputTextLabel.grid(column=1, row=6)
    outputFileName = tk.Entry(window)
    outputFileName.grid(column=1, row=7)

    stringSearchSubmitButton = tk.Button(window, text="Submit", font="Raleway", command=lambda: string_search(stringSearchEntry.get(), outputFileName.get()), bg="#81bc5a", fg="white", height=2, width=15)
    stringSearchSubmitButton.grid(column=2, row=7)

def time_search_open():
    lowerBoundLabel = tk.Label(window, text="Lower Bound (Hour:Min:Sec.MilliSec)")
    lowerBoundLabel.grid(column=0, row=6)
    lowerBoundInput = tk.Entry(window)
    lowerBoundInput.grid(column=0, row=7)

    upperBoundLabel = tk.Label(window, text="Upper Bound (Hour:Min:Sec.MilliSec)")
    upperBoundLabel.grid(column=0, row=8)
    upperBoundInput = tk.Entry(window)
    upperBoundInput.grid(column=0, row=9)

    outputTextLabel = tk.Label(window, text="Enter Output File Name")
    outputTextLabel.grid(column=1, row=6)
    outputFileName = tk.Entry(window)
    outputFileName.grid(column=1, row=7)

    tokenEnterLabel = tk.Label(window, text="Enter a String to Search for (Optional)")
    tokenEnterLabel.grid(column=1, row=8)
    tokenEnterInput = tk.Entry(window)
    tokenEnterInput.grid(column=1, row=9)

    stringSearchSubmitButton = tk.Button(window, text="Submit", font="Raleway", command=lambda: time_search(lowerBoundInput.get(), upperBoundInput.get(), tokenEnterInput.get(), outputFileName.get()), bg="#81bc5a", fg="white", height=2, width=15)
    stringSearchSubmitButton.grid(column=2, row=7)

def time_count_open():
    lowerBoundLabel = tk.Label(window, text="Enter Lower Bound (Hour:Min:Sec.MilliSec)")
    lowerBoundLabel.grid(column=0, row=6)
    lowerBoundInput = tk.Entry(window)
    lowerBoundInput.grid(column=0, row=7)

    upperBoundLabel = tk.Label(window, text="Enter Upper Bound (Hour:Min:Sec.MilliSec)")
    upperBoundLabel.grid(column=0, row=8)
    upperBoundInput = tk.Entry(window)
    upperBoundInput.grid(column=0, row=9)

    tokenEnterLabel = tk.Label(window, text="Enter a String to Search for (Optional)")
    tokenEnterLabel.grid(column=1, row=8)
    tokenEnterInput = tk.Entry(window)
    tokenEnterInput.grid(column=1, row=9)

    stringSearchSubmitButton = tk.Button(window, text="Submit", font="Raleway", command=lambda: time_count(lowerBoundInput.get(), upperBoundInput.get(), tokenEnterInput.get()), bg="#81bc5a", fg="white", height=2, width=15)
    stringSearchSubmitButton.grid(column=2, row=7)

def string_search(token, outputFileName):
    output_file_name = os.path.join(dir_path, outputFileName + ".txt")
    output_file=open(output_file_name, "w")

    occurrences=0
    for line in logFileLines:
        if token in str(line):
            output_file.write(line + "\n")
            occurrences=occurrences+1

    occurenceLabelText=tk.StringVar()
    occurrenceLabel = tk.Label(window, textvariable=occurenceLabelText)

    occurenceLabelText.set("There were " + str(occurrences) + " occurrences of the string " + token)

    occurrenceLabel.grid(column=1, row=8)

    output_file.close()


def time_search(lowerBoundInput, upperBoundInput, tokenInput, outputFileName):
    output_file_name = os.path.join(dir_path, outputFileName + ".txt")
    output_file = open(output_file_name, "w")
    occurrences = 0
    lowerBound = lowerBoundInput.split(":")
    upperBound = upperBoundInput.split(":")

    for i in range(0,3):
        lowerBound[i] = float(lowerBound[i])
        upperBound[i] = float(upperBound[i])

    for line in logFileLines:
        parse_line(line)
        if lineTime:
            if (upperBound[1] == lowerBound[1] == lineTime[1] and lowerBound[2] <= lineTime[2] <= upperBound[2]) or (
                    upperBound[1] != lowerBound[1] and (
                    (lineTime[1] == upperBound[1] and lineTime[2] < upperBound[2]) or (
                    lineTime[1] == lowerBound[1] and lineTime[2] > lowerBound[2]))):
                if tokenInput:
                    if tokenInput in str(line):
                        output_file.write(line + "\n")
                        occurrences = occurrences + 1
                else:
                    output_file.write(line + "\n")
                    occurrences = occurrences + 1

def time_count(lowerBoundInput, upperBoundInput, tokenInput):

    occurrences = 0
    lowerBound = lowerBoundInput.split(":")
    upperBound = upperBoundInput.split(":")

    for i in range(0,3):
        lowerBound[i] = float(lowerBound[i])
        upperBound[i] = float(upperBound[i])

    for line in logFileLines:
        parse_line(line)
        if lineTime:
            if (upperBound[1] == lowerBound[1] == lineTime[1] and lowerBound[2] <= lineTime[2] <= upperBound[2]) or (
                    upperBound[1] != lowerBound[1] and (
                    (lineTime[1] == upperBound[1] and lineTime[2] < upperBound[2]) or (
                    lineTime[1] == lowerBound[1] and lineTime[2] > lowerBound[2]))):
                if tokenInput:
                    if tokenInput in str(line):
                        occurrences = occurrences + 1
                else:
                    occurrences = occurrences + 1

    occurenceLabelText.set("There were " + str(occurrences) + " occurrences in that time period")
    occurrenceLabel.grid(column=1, row=8)

def parse_line(line):
    global lineTime
    lineTime = []
    if line != "\n":
        if "*" in line or "[" in line or "2021" in line:
            strip1 = ""
            for i in range(1, len(line)):
                if "{" in line[i] or "[" in line[i] or "]" in line[i] or "}" in line[i]:
                    break
                else:
                    strip1 = strip1 + line[i]
            strip2 = ""
            if line[0] == "*":
                parsedLine = strip1.split(maxsplit=3)
                strip2 = parsedLine[0] + " " + parsedLine[1] + " " + parsedLine[2]
                if strip2[len(strip2) - 1] == ":":
                    strip2 = strip2[:-1]
            elif line[0] == "[":
                zeroCount = 0
                for i in range(0, len(strip1)):
                    if zeroCount == 3:
                        break
                    else:
                        if strip1[i] == "0":
                            zeroCount = zeroCount + 1
                        else:
                            zeroCount = 0
                        strip2 = strip2 + strip1[i]
            else:
                strip2 = line[0] + strip1

            midWayContainer = parse(strip2)
            lineTime.append(float(midWayContainer.hour))
            lineTime.append(float(midWayContainer.minute))
            lineTime.append(float(str(midWayContainer.second)+"."+str(midWayContainer.microsecond)))
        else:
            lineTime=None
    else:
        lineTime = None

def find_next_point(lowerBound):
    upperBound = [0.0]*3
    upperBound[0] = lowerBound[0]

    if lowerBound[1] >= 59 and lowerBound[2] >= 30:
        upperBound[0] = lowerBound[0]+1
        upperBound[1] = 0.0
        upperBound[2] = round((lowerBound[2] + 30.0) % 60, 3)

    elif lowerBound[2] > 30:
        upperBound[1] = lowerBound[1] + 1
        upperBound[2] = round((lowerBound[2] + 30.0) % 60, 3)

    else:
        upperBound[1] = lowerBound[1]
        upperBound[2] = round(lowerBound[2] + 30.0, 3)

    return upperBound

def to_string(lowerBound, upperBound):
    #return str(lowerBound[0]) + ":" + str(lowerBound[1]) + ":" + str(lowerBound[2]) + "to " + str(upperBound[0]) + ":" + str(upperBound[1]) + ":" + str(upperBound[2])
    return str(int(lowerBound[0])) + ":" + str(int(lowerBound[1])) + ":" + str(lowerBound[2])

def batch_stripper(batch):
    newBatch=[]
    if len(batch) > 10:
        count=0
        for i in batch:
            if count % 4 == 0:
                newBatch.append(i)
                print(i)
            if count % 4 == 3:
                newBatch.append(i+batch[count-2])
                print(i+batch[count-2])
            count=count+1

        if len(batch) % 4 == 2:
            newBatch.append(batch[len(batch)-2])
            newBatch.append(batch[len(batch)-1])
            print(batch[len(batch)-2])
            print(batch[len(batch)-1])

    return newBatch

def make_histogram():
    count=0
    batch = []
    for line in logFileLines:
        parse_line(line)
        if lineTime is not None:
            time1 = lineTime
            lowerBound=lineTime
            break

    upperBound = find_next_point(lowerBound)

    for line in logFileLines:
        parse_line(line)
        if lineTime:
            if lineTime[0] > lowerBound[0]:
                count=count+1
            elif (upperBound[1] == lowerBound[1] == lineTime[1] and lowerBound[2] <= lineTime[2] <= upperBound[2]) or (upperBound[1] != lowerBound[1] and ((lineTime[1] == upperBound[1] and lineTime[2] < upperBound[2]) or (lineTime[1] == lowerBound[1] and lineTime[2] > lowerBound[2]))):
                count=count+1
            else:
                print(upperBound)
                print(count)
                batch.append(to_string(lowerBound, upperBound))
                batch.append(count)
                count = 0
                lowerBound=upperBound
                upperBound = find_next_point(lowerBound)

    x = []
    y = []
    count=0

    #while len(batch) > 11:
    #   batch = batch_stripper(batch)

    for i in batch:
        if count % 2 == 0:
            x.append(i)
        else:
            y.append(i)

        count=count+1

    plt.bar(x, y)
    plt.title("Log Counting Over Time")
    plt.xlabel("Start time for Log counting Period")
    plt.ylabel("Number of Logs")
    plt.show()


#Window initialization
window = tk.Tk()
window.title("Log Analyzer Engine")

canvas = tk.Canvas(window, width=600, height=400)
canvas.grid(columnspan=3, rowspan=4)

#Logo
logo = Image.open("C:\\Users\\gupta\\Downloads\\logAnalyzerEngineLogo.png")
logo = ImageTk.PhotoImage(logo)
logoLabel=tk.Label(image=logo)
logoLabel.image = logo
logoLabel.grid(column=1, row=0)

#Add first level of instructions
instructions = tk.Label(window, text="Select a Log file on your computer to analyze", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

#Browse button
browseText = tk.StringVar()
browseButton = tk.Button(window, textvariable=browseText, command=lambda:open_file() ,font="Raleway", bg="#81bc5a", fg="white", height=2, width=15)
browseText.set("Browse")
browseButton.grid(column=1, row=2)



window.mainloop()