# import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting modules
import junoMAG
import junoEphemeris
import junoWAVES

timeFrame = ["2016-12-17T00:00:00", "2016-12-20T00:02:00"]

plotMag = True
plotWaves = False

numSubPlots = 2

fig = plt.figure()

positionIndex = 1

if plotMag:
    ax = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoMAG.PlotData(ax, timeFrame, plotEphemeris=True, polarCoordinates=True)
    positionIndex += 1

if plotWaves:
    ax = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoWAVES.PlotData(fig, ax, timeFrame, plotEphemeris=False)
    positionIndex += 1

plt.show()
