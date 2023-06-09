## imports
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

xCoords = np.linspace(0, 10, 1000)

dataSelection = {
        "totalMagenticField": False,
        "quadratic": False,
        "negative cubic": False
    }

window = tk.Tk()

checkboxVar_totalB = tk.BooleanVar()
cbB = tk.BooleanVar()
cbC = tk.BooleanVar()

def main():

    window.title("JUPT")

    plotButton = tk.Button(window, text="PLOT", command=PlotData)
    plotButton.pack() 

    dataSelectionFrame = tk.LabelFrame(window, text="Data Selection")

    checkBoxA = tk.Checkbutton(dataSelectionFrame, text="Total Magnetic Field Strength |B|", variable=checkboxVar_totalB, onvalue=True, offvalue=False, command=ChangeSelection)
    checkBoxA.pack()

    checkBoxB = tk.Checkbutton(dataSelectionFrame, text="Quadratic", variable=cbB, onvalue=True, offvalue=False, command=ChangeSelection)
    checkBoxB.pack()

    checkBoxC = tk.Checkbutton(dataSelectionFrame, text="Negative Cubic", variable=cbC, onvalue=True, offvalue=False, command=ChangeSelection)
    checkBoxC.pack()

    dataSelectionFrame.pack()

    window.mainloop()

def ChangeSelection():

    if checkboxVar_totalB.get() == True:
        dataSelection["totalMagenticField"] = True
    else:
        dataSelection["totalMagenticField"] = False

    if cbB.get() == True:
        dataSelection["quadratic"] = True
    else:
        dataSelection["quadratic"] = False

    if cbC.get() == True:
        dataSelection["negative cubic"] = True
    else:
        dataSelection["negative cubic"] = False

def FetchData(dataSelection, xCoords):
    
    dataOutput = []
    if dataSelection["linear"] == True:
        dataA = PlotA(xCoords)
        dataOutput.append(dataA)

    if dataSelection["quadratic"] == True:
        dataB = PlotB(xCoords)
        dataOutput.append(dataB)

    if dataSelection["negative cubic"] == True:
        dataC = PlotC(xCoords)
        dataOutput.append(dataC)

    return dataOutput

def PlotData():
    dataList = FetchData(dataSelection, xCoords)

    fig = plt.figure()

    numSubPlots = len(dataList)
    positionIndex = range(1, numSubPlots + 1)

    for i, data in zip(range(numSubPlots), dataList):

        ax = fig.add_subplot(numSubPlots, 1, positionIndex[i])
        ax.plot(xCoords, data)

    plt.show()

def PlotA(xCoords):
    # Line y = x 
    y = []
    for x in xCoords:
        y.append(x)
    return y

def PlotB(xCoords):
    # line y = x**2
    y = []
    for x in xCoords:
        y.append(x**2)
    return y

def PlotC(xCoords):
    # line y = x**3
    y = []
    for x in xCoords:
        y.append(-x**3)
    return y


if __name__ == "__main__":
    main()
