import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting modules
import junoMAG
import junoEphemeris

timeFrame = ["2018-01-01T00:00:00", "2018-01-01T00:50:00"]

plotMag = True

numSubPlots = 2

fig = plt.figure()

positionIndex = 1

if plotMag:
    ax = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoMAG.PlotData(ax, timeFrame, plotEphemeris=True)
    positionIndex += 1

plt.show()
