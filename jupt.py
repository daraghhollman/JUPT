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
import junoTrajectories

config.read("./config.ini")

# Selected timeframe to display between
timeFrame = [config["plotting"]["start time"], config["plotting"]["end time"]]

# Set path to place data
dataDirectory = config["data"]["data directory"]
spiceDirectory = config["data"]["spice directory"]

# Set parameters for the shape of ticks
majorTickLength = config["plotting"].getfloat("major tick length")
majorTickWidth = config["plotting"].getfloat("major tick width")
minorTickLength = config["plotting"].getfloat("minor tick length")
minorTickWidth = config["plotting"].getfloat("minor tick width")

# Select which panels to plot
wavesPlotIndex = ast.literal_eval(config["plotting"]["plot Waves"])
if wavesPlotIndex != False:
    plotWaves = True
else:
    plotWaves = False

magPlotIndex = ast.literal_eval(config["plotting"]["plot MAG"])
if magPlotIndex != False:
    plotMag = True
else:
    plotMag = False

electronEnergyPlotIndex = ast.literal_eval(config["plotting"]["plot JADE electron energies"])
if electronEnergyPlotIndex != False:
    plotElectronEnergy = True
else:
    plotElectronEnergy = False

pitchAnglePlotIndex = ast.literal_eval(config["plotting"]["plot JADE electron pitch angles"])
if pitchAnglePlotIndex != False:
    plotPitchAngle = True
else:
    plotPitchAngle = False

if plotElectronEnergy or plotPitchAngle:
    plotJADE = True
else:
    plotJADE = False

trajectoriesPlotIndex = ast.literal_eval(config["plotting"]["plot trajectories"])
if trajectoriesPlotIndex != False:
    plotTrajectories = True
else:
    plotTrajectories = False

# JADE Moments
densityPlotIndex = ast.literal_eval(config["plotting"]["plot density"])
if densityPlotIndex != False:
    plotDensity = True
else:
    plotDensity = False

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

panelsList = [plotWaves, plotMag, plotElectronEnergy, plotPitchAngle, plotDensity, plotTrajectories]
numSubPlots = 0
for plotType in panelsList:
    if plotType != False:
        numSubPlots += 1


fig = plt.figure()
plt.rcParams.update({'font.size': fontsize}) # Changes the default fontsize


# Section controlling Waves plotting
if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, wavesPlotIndex)

    # Plot the Waves data from the junoWAVES script
    if wavesPlotIndex < numSubPlots:
        junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=ast.literal_eval(config["Waves"]["frequency limit"]), plotEphemeris=True, ephemerisLabels=False, colourmap=config["Waves"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), yscale=config["Waves"]["y scale"])
        axWaves.set_xticklabels('')
    else:
        junoWAVES.PlotData(fig, axWaves, timeFrame, dataDirectory = dataDirectory, yLim=ast.literal_eval(config["Waves"]["frequency limit"]), plotEphemeris=True, ephemerisLabels=True, colourmap=config["Waves"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), yscale=config["Waves"]["y scale"])

    axWaves.tick_params("y", which="major", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
    axWaves.tick_params("y", which="minor", length=config["plotting"].getfloat("y tick length")/2, width=config["plotting"].getfloat("y tick width"))
    axWaves.margins(x=0)

    if wavesPlotIndex == 1:
        axWaves.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axWaves.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)
    else:
        axWaves.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axWaves.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)
  

if plotJADE:
   
    if plotElectronEnergy:
        axJade = fig.add_subplot(numSubPlots, 1, electronEnergyPlotIndex)

        if electronEnergyPlotIndex < numSubPlots:
            
            junoJade.PlotData(fig, axJade, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=False, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), plotElectronEnergy=True, plotPitchAngle=False)
            axJade.set_xticklabels('')
        else:
            junoJade.PlotData(fig, axJade, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=True, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), plotElectronEnergy=True, plotPitchAngle=False)

        axJade.tick_params("y", which="major", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
        axJade.tick_params("y", which="minor", length=config["plotting"].getfloat("y tick length")/2, width=config["plotting"].getfloat("y tick width"))
        axJade.margins(x=0)
    
        if electronEnergyPlotIndex == 1:
            axJade.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
            axJade.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

        else:
            axJade.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
            axJade.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

    if plotPitchAngle:
        axJadePitch = fig.add_subplot(numSubPlots, 1, pitchAnglePlotIndex)

        if pitchAnglePlotIndex < numSubPlots:

            junoJade.PlotData(fig, axJadePitch, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=False, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), plotElectronEnergy=False, plotPitchAngle=True, reBin=config["JADE"].getboolean("bin pitch angles"), pitchBinStep=config["JADE"].getint("bin size"), pitchAngleEnergyRange=ast.literal_eval(config["JADE"]["pitch angle energy range"]))
            axJadePitch.set_xticklabels('')
        else:
            junoJade.PlotData(fig, axJadePitch, timeFrame, dataDirectory=dataDirectory, hiRes=config["JADE"].getboolean("high resolution"), plotEphemeris=True, ephemerisLabels=True, colourmap=config["JADE"]["colour map"], downloadNewData=config["data"].getboolean("download new data"), plotElectronEnergy=False, plotPitchAngle=True, pitchBinStep=config["JADE"].getint("bin size"), pitchAngleEnergyRange=ast.literal_eval(config["JADE"]["pitch angle energy range"]))

        axJadePitch.tick_params("y", which="major", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
        axJadePitch.tick_params("y", which="minor", length=config["plotting"].getfloat("y tick length")/2, width=config["plotting"].getfloat("y tick width"))
        axJadePitch.margins(x=0)

        if pitchAnglePlotIndex == 1:
            axJadePitch.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
            axJadePitch.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

        else:
            axJadePitch.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
            axJadePitch.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

# Moments
if plotDensity:
    axDensity = fig.add_subplot(numSubPlots, 1, densityPlotIndex)

    if densityPlotIndex < numSubPlots:
        junoDerivedMoments.PlotDensity(fig, axDensity, timeFrame, dataDirectory, plotEphemeris=True, ephemerisLabels=False, downloadNewData=config["data"].getboolean("download new data"))
    else:
        junoDerivedMoments.PlotDensity(fig, axDensity, timeFrame, dataDirectory, plotEphemeris=True, ephemerisLabels=True, downloadNewData=config["data"].getboolean("download new data"))

    if densityPlotIndex == 1:
        axDensity.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axDensity.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

    else:
        axDensity.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axDensity.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)


# Section controlling MAG plotting
if plotMag:

    axMag = fig.add_subplot(numSubPlots, 1, magPlotIndex)

    if magPlotIndex < numSubPlots:
        # Plot the MAG data from the junoMAG script
        junoMAG.PlotData(axMag, timeFrame, plotMeasurements={
            "total": config["MAG"].getboolean("plot magnitude"),
            "cartesians": config["MAG"].getboolean("plot cartesians"),
            "polars": config["MAG"].getboolean("plot polars"),
            "lobe": config["MAG"].getboolean("plot lobe"),
            "lobeUncertainty": config["MAG"].getboolean("plot lobe uncertainty")
        }, plotEphemeris=True, ephemerisLabels=False, linewidth=config["MAG"].getfloat("line width"), componentColours=componentColours, lobeColour=lobeColour, magnitudeColour=magnitudeColour)
    else:
        junoMAG.PlotData(axMag, timeFrame, plotMeasurements={
            "total": config["MAG"].getboolean("plot magnitude"),
            "cartesians": config["MAG"].getboolean("plot cartesians"),
            "polars": config["MAG"].getboolean("plot polars"),
            "lobe": config["MAG"].getboolean("plot lobe"),
            "lobeUncertainty": config["MAG"].getboolean("plot lobe uncertainty")
        }, plotEphemeris=True, ephemerisLabels=True, linewidth=config["MAG"].getfloat("line width"), componentColours=componentColours, lobeColour=lobeColour, magnitudeColour=magnitudeColour)

    axMag.tick_params("y", length=config["plotting"].getfloat("y tick length"), width=config["plotting"].getfloat("y tick width"))
    axMag.margins(x=0)

    if magPlotIndex == 1:
        axMag.tick_params("x", which="major", top=False, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axMag.tick_params("x", which="minor", top=False, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)

    else:
        axMag.tick_params("x", which="major", top=True, bottom=True, direction="inout", length=majorTickLength, width=majorTickWidth)
        axMag.tick_params("x", which="minor", top=True, bottom=True, direction="inout", length=minorTickLength, width=minorTickWidth)


# Set tick formatting and add vertical lines 
for i, axis in enumerate(fig.axes):

    # vLines from file
    if i % 2 == 0 and config["vertical lines"].getboolean("read from file") == True:
        vLines.PlotFromFile(axis, i, timeFrame, config["vertical lines"]["file path"], config["vertical lines"]["file line colour"], vLineStyle)

    # Manual vLines
    if i % 2 == 0 and len(vLinePositions) != 0: # As each axis is divided to keep widths consistant with colourbars and legends, there are always twice as many axes as data plotted. These are created sequentially in the order data axis, legend axis, and hence we can use the modulo to only get the even positionIndex
        vLines.PlotVLines(axis, i, timeFrame, vLinePositions, vLineLabels, vLineColours, vLineStyle)

            
    axis.format_coord = lambda x, y: '' # Disables the cursor coordinate display. This feature causes major slowdowns when resizing the window.


if plotTrajectories:

    axTrajectories = fig.add_subplot(numSubPlots, 1, trajectoriesPlotIndex)

    axTrajectories = junoTrajectories.ThreePanelTrajectories(axTrajectories, timeFrame, spiceDirectory, frame=config["trajectories"]["frame"], plottedColour=config["trajectories"]["plotted colour"], extensionColour=config["trajectories"]["extension colour"], timeExtension=config["trajectories"].getint("time extension"))


# Move the subplots together and add room below for ephemeris labels
plt.subplots_adjust(hspace=panelSpacing, bottom=0.2)


print("Showing figure")
plt.show()
