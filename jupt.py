import matplotlib.pyplot as plt
from datetime import datetime
import configparser
import ast

config = configparser.ConfigParser()

# Importing plotting scripts
import junoMAG
import junoEphemeris
import junoWAVES

config.read("./config.ini")

# Selected timeframe to display between
timeFrame = [config["plotting"]["start time"], config["plotting"]["end time"]]

# Set path to place data
dataDirectory = config["data"]["data directory"]

# Set parameters for the shape of ticks
majorTickLength = config["plotting"].getfloat("major tick length")
majorTickWidth = config["plotting"].getfloat("major tick width")
minorTickLength = config["plotting"].getfloat("minor tick length")
minorTickWidth = config["plotting"].getfloat("minor tick width")

# Select which panels to plot
plotWaves = config["plotting"].getboolean("plot Waves")
plotMag = config["plotting"].getboolean("plot MAG")

# Set font parameters
fontsize = config["plotting"].getfloat("font size")

# Space between the panels
panelSpacing = config["plotting"].getfloat("panel spacing")

# Parameters for vertical lines
vLineLabels = ast.literal_eval(config["vertical lines"]["labels"])
vLinePositions = ast.literal_eval(config["vertical lines"]["positions"])
vLineLabelSpacing = 1/32 # In units of axis length

# Colour Parameters
vLineColours = ast.literal_eval(config["vertical lines"]["colours"])
componentColours = ast.literal_eval(config["colours"]["component colours"])
magnitudeColour = config["colours"]["magnitude colour"]
lobeColour = config["colours"]["lobe colour"]

panelsBooleanList = [plotWaves, plotMag]
numSubPlots = sum(panelsBooleanList)


fig = plt.figure()
plt.rcParams.update({'font.size': fontsize}) # Changes the default fontsize

positionIndex = 1 # Define a position index to tell each subplot what position it should be in

# Section controlling Waves plotting
if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, positionIndex)

    # Plot the Waves data from the junoWAVES script
    junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=ast.literal_eval(config["Waves"]["frequency limit"]), plotEphemeris=True, ephemerisLabels=False, colourmap=config["Waves"]["colour map"])
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
        "total": config["MAG"].getboolean("plot magnitude"),
        "cartesians": config["MAG"].getboolean("plot cartesians"),
        "polars": config["MAG"].getboolean("plot polars"),
        "lobe": config["MAG"].getboolean("plot lobe"),
        "lobeUncertainty": config["MAG"].getboolean("plot lobe uncertainty")
    }, plotEphemeris=True, ephemerisLabels=True, linewidth=config["MAG"].getfloat("line width"), componentColours=componentColours, lobeColour=lobeColour, magnitudeColour=magnitudeColour)
    positionIndex += 1



# Set tick formatting and add vertical lines 
for i, axis in enumerate(fig.axes):

    if i % 2 == 0 and len(vLinePositions) == 0: # As each axis is divided to keep widths consistant with colourbars and legends, there are always twice as many axes as data plotted. These are created sequentially in the order data axis, legend axis, and hence we can use the modulo to only get the even index.
        for label, position, colour in zip(vLineLabels, vLinePositions, vLineColours):
            # convert from string to datetime
            posTime = datetime.strptime(position, "%Y-%m-%dT%H:%M:%S")
            startTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
            endTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")
            axisPos = (posTime-startTime).total_seconds()
            axisLength = (endTime - startTime).total_seconds()

            axis.axvline(axisPos, color=colour, linestyle="--") # x coord in seconds from start
            
            if label != "" and i == 0: # Labels on top plot only
                plt.text((axisPos/axisLength)+vLineLabelSpacing, 0.9, label, transform=axis.transAxes, color=colour)

            
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
