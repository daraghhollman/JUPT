# import tkinter as tk
import matplotlib.pyplot as plt

# Importing plotting scripts
import junoMAG
import junoEphemeris
import junoWAVES

# Selected timeframe to display between
timeFrame = ["2021-09-12T00:00:00", "2021-09-18T00:00:00"]

# Set path to place data
dataDirectory = r"/home/daraghhollman/Main/data/"

# Set parameters for the shape of ticks
majorTickLength=12
majorTickWidth=0.8
minorTickLength=8
minorTickWidth=majorTickWidth

# Select which panels to plot
plotWaves = True
plotMag = True

panelsBooleanList = [plotWaves, plotMag]
numSubPlots = sum(panelsBooleanList)

# Set font parameters
fontsize = 11

# Space between the panels
panelSpacing = 0.0


fig = plt.figure()
plt.rcParams.update({'font.size': fontsize}) # Changes the default fontsize

positionIndex = 1 # Define a position index to tell each subplot what position it should be in

# Section controlling Waves plotting
if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, positionIndex)

    # Plot the Waves data from the junoWAVES script
    junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=[9, 139], vmin=10e-16, vmax=10e-12, plotEphemeris=True, ephemerisLabels=False)
    positionIndex += 1

    if numSubPlots != 1:
        # Make the ephemerisLabels invisible if in a multipanel plot
        plt.setp(axWaves.get_xticklabels(), visible=False)


# Section controlling MAG plotting
if plotMag:
    # Test if this subplot needs to share axes
    if plotWaves:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axWaves)
    else:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex)

    # Plot the MAG data from the junoMAG script
    junoMAG.PlotData(axMag, timeFrame, plotMeasurements={
        "total": True,
        "cartesians": False,
        "polars": True,
        "lobe": True,
        "lobeUncertainty": True
    }, plotEphemeris=True, ephemerisLabels=True, linewidth=0.5)
    positionIndex += 1


# Set tick formatting
for i, axis in enumerate(fig.axes):
    axis.format_coord = lambda x, y: '' # Disables the cursor coordinate display. This feature causes major slowdowns when resizing the window.
    if i == 0:
        axis.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axis.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)
    else:
        axis.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axis.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

# Move the subplots together and add room below for ephemeris labels
plt.subplots_adjust(hspace=panelSpacing, bottom=0.2)


print("Showing figure")
plt.show()
