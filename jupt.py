# import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting modules
import junoMAG
import junoEphemeris
import junoWAVES

timeFrame = ["2016-12-18T00:00:00", "2016-12-19T12:01:00"]

majorTickLength=10
majorTickWidth=0.8

minorTickLength=7
minorTickWidth=majorTickWidth

plotWaves = True
plotMag = True

numSubPlots = 2

fig = plt.figure()

plt.rcParams.update({'font.size': 11})

positionIndex = 1

if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = r"/home/daraghhollman/Main/data/", yLim=[9, 139], vmin=10e-16, vmax=10e-12, plotEphemeris=True, ephemerisLabels=False)
    positionIndex += 1

if plotMag:
    if plotWaves:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axWaves)
    else:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoMAG.PlotData(axMag, timeFrame, plotEphemeris=True, ephemerisLabels=True, polarCoordinates=True, linewidth=0.5)
    positionIndex += 1


plt.setp(axWaves.get_xticklabels(), visible=False)

for axis in fig.axes:
    axis.tick_params("x", which="major", direction="inout", length=majorTickLength, width=majorTickWidth)
    axis.tick_params("x", which="minor", direction="inout", length=minorTickLength, width=minorTickWidth)

plt.subplots_adjust(hspace=0, bottom=0.2)


print("Showing figure")
plt.show()
