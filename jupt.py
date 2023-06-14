# import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting modules
import junoMAG
import junoEphemeris
import junoWAVES

timeFrame = ["2021-09-09T00:00:00", "2021-09-12T05:05:00"]

plotMag = True
plotWaves = True

numSubPlots = 2

fig = plt.figure()

positionIndex = 1

if plotMag:
    ax = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoMAG.PlotData(ax, timeFrame, plotEphemeris=False, polarCoordinates=True, linewidth=0.5)
    positionIndex += 1

if plotWaves:
    ax = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoWAVES.PlotData(fig, ax, timeFrame, dataDirectory = r"/home/daraghhollman/Main/data/", plotEphemeris=True)
    positionIndex += 1

plt.show()
