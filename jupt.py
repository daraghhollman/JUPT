print("Importing packages")

import matplotlib.pyplot as plt
from datetime import datetime
import configparser
import ast

config = configparser.ConfigParser()

# Importing plotting scripts
import junoMAG
import junoEphemeris
import junoWAVES
import junoJade
import vLines
import junoDerivedMoments

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
plotJADE = config["plotting"].getboolean("plot JADE")
plotDensity = config["plotting"].getboolean("plot density")

# Set font parameters
fontsize = config["plotting"].getfloat("font size")

# Space between the panels
panelSpacing = config["plotting"].getfloat("panel spacing")

# Parameters for vertical lines
vLineLabels = ast.literal_eval(config["vertical lines"]["labels"])
vLinePositions = ast.literal_eval(config["vertical lines"]["positions"])
vLineStyle = config["vertical lines"]["linestyle"]
vLineLabelSpacing = 1/32 # In units of axis length

# Colour Parameters
vLineColours = ast.literal_eval(config["vertical lines"]["colours"])
componentColours = ast.literal_eval(config["colours"]["component colours"])
magnitudeColour = config["colours"]["magnitude colour"]
lobeColour = config["colours"]["lobe colour"]

panelsBooleanList = [plotWaves, plotMag, plotJADE, plotDensity]
numSubPlots = sum(panelsBooleanList)


fig = plt.figure()
plt.rcParams.update({'font.size': fontsize}) # Changes the default fontsize

positionIndex = 1 # Define a position index to tell each subplot what position it should be in

# Section controlling Waves plotting
if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, positionIndex)

    # Plot the Waves data from the junoWAVES script
    if plotMag or plotJADE:
        junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=ast.literal_eval(config["Waves"]["frequency limit"]), plotEphemeris=True, ephemerisLabels=False, colourmap=config["Waves"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), yscale=config["Waves"]["y scale"])
        axWaves.set_xticklabels('')
    else:
        junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=ast.literal_eval(config["Waves"]["frequency limit"]), plotEphemeris=True, ephemerisLabels=True, colourmap=config["Waves"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), yscale=config["Waves"]["y scale"])

    axWaves.tick_params("y", which="major", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
    axWaves.tick_params("y", which="minor", length=config["plotting"].getfloat("y tick length")/2, width=config["plotting"].getfloat("y tick width"))
    axWaves.margins(x=0)
  
    positionIndex += 1

    if numSubPlots != 1:
        # Make the ephemerisLabels invisible if in a multipanel plot
        plt.setp(axWaves.get_xticklabels(), visible=False)

if plotJADE:
    """
    if plotWaves:
        axJade = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axWaves)
    else:
        axJade = fig.add_subplot(numSubPlots, 1, positionIndex)
    """
    axJade = fig.add_subplot(numSubPlots, 1, positionIndex)

    if plotMag:
        junoJade.PlotData(fig, axJade, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=False, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"))
        axJade.set_xticklabels('')
    else:
        junoJade.PlotData(fig, axJade, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=True, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), plotElectronEnergy=False, plotLookAngle=True)
        
    axJade.tick_params("y", which="major", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
    axJade.tick_params("y", which="minor", length=config["plotting"].getfloat("y tick length")/2, width=config["plotting"].getfloat("y tick width"))
    axJade.margins(x=0)

    positionIndex += 1

# Moments
if plotDensity:
    axDensity = fig.add_subplot(numSubPlots, 1, positionIndex)
    junoDerivedMoments.PlotDensity(fig, axDensity, timeFrame, dataDirectory, plotEphemeris=False, ephemerisLabels=False, downloadNewData=config["data"].getboolean("download new data"))

    positionIndex += 1
    




# Section controlling MAG plotting
if plotMag:
    # Test if this subplot needs to share axes
    if plotWaves:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axWaves)
    elif plotJADE:
        axMag = fig.add_subplot(numSubPlots, 1, positionIndex, sharex=axJade)
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

    axMag.tick_params("y", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
    axMag.margins(x=0)


# Set tick formatting and add vertical lines 
for i, axis in enumerate(fig.axes):

    # vLines from file
    if i % 2 == 0 and config["vertical lines"].getboolean("read from file") == True:
        vLines.PlotFromFile(axis, i, timeFrame, config["vertical lines"]["file path"], config["vertical lines"]["file line colour"], vLineStyle)

    # Manual vLines
    if i % 2 == 0 and len(vLinePositions) != 0: # As each axis is divided to keep widths consistant with colourbars and legends, there are always twice as many axes as data plotted. These are created sequentially in the order data axis, legend axis, and hence we can use the modulo to only get the even positionIndex
        vLines.PlotVLines(axis, i, timeFrame, vLinePositions, vLineLabels, vLineColours, vLineStyle)

            
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
