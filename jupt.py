# import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting modules
import junoMAG
import junoEphemeris
import junoWAVES

timeFrame = ["2016-12-17T00:00:00", "2016-12-24T05:00:00"]

majorTickLength=10
majorTickWidth=0.8

minorTickLength=7
minorTickWidth=majorTickWidth

plotMag = True
plotWaves = True

numSubPlots = 2

fig = plt.figure()

positionIndex = 1

if plotMag:
    axMag = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoMAG.PlotData(axMag, timeFrame, plotEphemeris=True, polarCoordinates=True, linewidth=0.5)
    positionIndex += 1

if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axMag)
    junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = r"/home/daraghhollman/Main/data/", plotEphemeris=True)
    # axWaves.get_shared_x_axes().join(axMag, axWaves)
    positionIndex += 1

plt.setp(axMag.get_xticklabels(), visible=False)

for axis in fig.axes:
    axis.tick_params("x", which="major", direction="inout", length=majorTickLength, width=majorTickWidth)
    axis.tick_params("x", which="minor", direction="inout", length=minorTickLength, width=minorTickWidth)

plt.subplots_adjust(hspace=0)

plt.show()
