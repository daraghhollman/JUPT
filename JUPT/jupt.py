"""
Primary file for JUPT. This is the script that is ran to create plots.
"""

# Importing Packages
import ast
import configparser
import datetime
import os
import sys

import matplotlib.pyplot as plt

import junoDerivedMoments
import junoJade
import junoJADE_ions
import junoMAG
import junoTrajectories
import junoWAVES
import userAdditions
import vLines

# Defining default config values
defaultPlottingConfig = {
    "plotting": {
        "plot density": 0,
        "panel spacing": 0.2,
        "font size": 11,
        "major tick length": 16,
        "minor tick length": 8,
        "major tick width": 1,
        "minor tick width": 1,
        "y tick length": 12,
        "y tick width": 0.8,
    },
    "colours": {
        "magnitude colour": "black",
        "component colours": ["indianred", "mediumturquoise", "cornflowerblue"],
        "lobe colour": "gold",
    },
    "vertical lines": {
        "read from file": False,
        "file path": "",
        "file line colour": "red",
        "labels": ["Example One", "Example Two"],
        "positions": [],
        "colours": ["red", "yellow"],
        "linestyle": "--",
    },
    "Waves": {
        "frequency limit": [1, 149],
        "colour map": "viridis",
        "frequency bins": 200,
        "y scale": "log",
    },
    "JADE": {
        "pitch angle energy range": [],
        "bin pitch angles": True,
        "bin size": 10,
        "colour map": "magma",
        "high resolution": False,
    },
    "JADE Ions": {
        "colour map": "plasma",
        "TOF range": [],
    },
    "MAG": {
        "plot magnitude": True,
        "plot cartesians": False,
        "plot polars": True,
        "plot lobe": False,
        "plot lobe uncertainty": False,
        "line width": 1,
    },
    "trajectories": {
        "BS dynamic pressure": 0.5,
        "MP dynamic pressure": 0.7,
        "plot bow shock": True,
        "plot magnetopause": True,
        "bow shock colour": "black",
        "magnetopause colour": "turquoise",
        "frame": "JUNO_JSS",
        "plotted colour": "magenta",
        "extension colour": "black",
        "time extension": 30,
        "major tick length": 10,
        "minor tick length": 5,
        "major tick multiple": 25,
        "minor tick multiple": 5,
        "x bounds": [-100, 100],
        "y bounds": [-100, 100],
        "z bounds": [-100, 100],
        "equal aspect": True,
    },
}


# Reading the config files
directoryConfig = configparser.ConfigParser()
plottingConfig = configparser.ConfigParser()

plottingConfig.read_dict(defaultPlottingConfig)

directoryConfig.read("./directory_config.ini")

# Plotting config is passed as an argument to the script
plottingConfig.read(f"./{sys.argv[1]}")

# Pull out the name of the config file to be used in saving files later
configName = sys.argv[1].split("/")[-1][0:-4]

# LOADING THE CONFIG

# Set paths
dataDirectory = directoryConfig["data"]["data directory"]
spiceDirectory = directoryConfig["data"]["spice directory"]
magBoundariesRepoPath = directoryConfig["trajectories"]["magnetophere boundaries path"]

# Selected timeframe to display between
timeFrame = [
    plottingConfig["plotting"]["start time"],
    plottingConfig["plotting"]["end time"],
]

# Find which panels to plot and where
# There's got to be a better way of doing this
wavesPlotIndex = ast.literal_eval(plottingConfig["plotting"]["plot Waves"])
if wavesPlotIndex is not False:
    plotWaves = True
else:
    plotWaves = False

magPlotIndex = ast.literal_eval(plottingConfig["plotting"]["plot MAG"])
if magPlotIndex is not False:
    plotMag = True
else:
    plotMag = False

electronEnergyPlotIndex = ast.literal_eval(
    plottingConfig["plotting"]["plot JADE electron energies"]
)
if electronEnergyPlotIndex is not False:
    plotElectronEnergy = True
else:
    plotElectronEnergy = False

pitchAnglePlotIndex = ast.literal_eval(
    plottingConfig["plotting"]["plot JADE electron pitch angles"]
)
if pitchAnglePlotIndex is not False:
    plotPitchAngle = True
else:
    plotPitchAngle = False

ionEnergyPlotIndex = ast.literal_eval(
    plottingConfig["plotting"]["plot JADE ion energies"]
)
if ionEnergyPlotIndex is not False:
    plotIonEnergy = True
else:
    plotIonEnergy = False

if plotElectronEnergy or plotPitchAngle or plotIonEnergy:
    plotJADE = True
else:
    plotJADE = False

trajectoriesPlotIndex = ast.literal_eval(
    plottingConfig["plotting"]["plot trajectories"]
)
if trajectoriesPlotIndex is not False:
    plotTrajectories = True
else:
    plotTrajectories = False

# JADE Moments
densityPlotIndex = ast.literal_eval(plottingConfig["plotting"]["plot density"])
if densityPlotIndex is not False:
    plotDensity = True
else:
    plotDensity = False


# Set font parameters
fontsize = plottingConfig["plotting"].getfloat("font size")

# Set parameters for the shape of ticks
majorTickLength = plottingConfig["plotting"].getfloat("major tick length")
majorTickWidth = plottingConfig["plotting"].getfloat("major tick width")
minorTickLength = plottingConfig["plotting"].getfloat("minor tick length")
minorTickWidth = plottingConfig["plotting"].getfloat("minor tick width")

# Space between the panels
panelSpacing = plottingConfig["plotting"].getfloat("panel spacing")

# Parameters for vertical lines
vLineLabels = ast.literal_eval(plottingConfig["vertical lines"]["labels"])
vLinePositions = ast.literal_eval(plottingConfig["vertical lines"]["positions"])
vLineStyle = plottingConfig["vertical lines"]["linestyle"]
vLineLabelSpacing = 1 / 32  # In units of axis length

# Colour Parameters
vLineColours = ast.literal_eval(plottingConfig["vertical lines"]["colours"])
componentColours = ast.literal_eval(plottingConfig["colours"]["component colours"])
magnitudeColour = plottingConfig["colours"]["magnitude colour"]
lobeColour = plottingConfig["colours"]["lobe colour"]

# Loop through all possible panels to find the number of subplots needed
panelsList = [
    plotWaves,
    plotMag,
    plotElectronEnergy,
    plotPitchAngle,
    plotIonEnergy,
    plotDensity,
    plotTrajectories,
]
numSubPlots = 0
for plotType in panelsList:
    if plotType is not False:
        numSubPlots += 1


#######################################
# CHECKING FOR COMMON CONFIG MISTAKES
print("Checking config validity...")

# Check if end time is before start time
startTime = datetime.datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
endTime = datetime.datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")

if (endTime - startTime) < datetime.timedelta(seconds=0):
    raise ValueError("CONFIG ERROR -> End time occurs before start time")

# Check if largest panel index matches the number of panels
panelIndices = [
    magPlotIndex,
    wavesPlotIndex,
    trajectoriesPlotIndex,
    electronEnergyPlotIndex,
    ionEnergyPlotIndex,
    pitchAnglePlotIndex,
]
for index in panelIndices:
    if index > (numSubPlots):
        raise ValueError(
            "CONFIG ERROR -> Assigned panel index is larger than the number of panels."
            "Check panel index assignment."
        )

# Check if a panel index is repeated
# Ignoring 0s
checkPanelIndices = [i for i in panelIndices if i != 0]
if len(checkPanelIndices) > len(set(checkPanelIndices)):
    raise ValueError(
        "CONFIG ERROR -> Repeated index in assigned panel indices. Check panel index assignment."
    )

# Further config error detection should be included here as discovered
print("Config parameters passed checks")
###########################################

print("Constructing Plot")
# An arbitrary figure size set based on testing
fig = plt.figure(figsize=(16, 5 * numSubPlots))
plt.rcParams.update({"font.size": fontsize})  # Changes the default fontsize


# This next section is a complete mess and could definitely use a rewrite (potentially the use of
# objects could be critical in the passing of information between the scripts).
# Its role is to check the config parameters for the panels needed, and to pass through relevant
# options

# Create axes dictionary
axesDict = {}

# Section controlling Waves plotting
if plotWaves:
    axWaves = fig.add_subplot(numSubPlots, 1, wavesPlotIndex)
    axesDict["Waves"] = axWaves

    # Plot the Waves data from the junoWAVES script
    if wavesPlotIndex < numSubPlots:
        junoWAVES.PlotData(
            fig,
            axWaves,
            timeFrame,
            dataDirectory=dataDirectory,
            yLim=ast.literal_eval(plottingConfig["Waves"]["frequency limit"]),
            plotEphemeris=True,
            ephemerisLabels=False,
            colourmap=plottingConfig["Waves"]["colour map"],
            downloadNewData=directoryConfig["data"].getboolean("download new data"),
            yscale=plottingConfig["Waves"]["y scale"],
        )
        axWaves.set_xticklabels("")
    else:
        junoWAVES.PlotData(
            fig,
            axWaves,
            timeFrame,
            dataDirectory=dataDirectory,
            yLim=ast.literal_eval(plottingConfig["Waves"]["frequency limit"]),
            plotEphemeris=True,
            ephemerisLabels=True,
            colourmap=plottingConfig["Waves"]["colour map"],
            downloadNewData=directoryConfig["data"].getboolean("download new data"),
            yscale=plottingConfig["Waves"]["y scale"],
        )

    axWaves.tick_params(
        "y",
        which="major",
        length=plottingConfig["plotting"].getfloat("y tick length"),
        width=plottingConfig["plotting"].getfloat("y tick width"),
    )
    axWaves.tick_params(
        "y",
        which="minor",
        length=plottingConfig["plotting"].getfloat("y tick length") / 2,
        width=plottingConfig["plotting"].getfloat("y tick width"),
    )
    axWaves.margins(x=0)

    if wavesPlotIndex == 1:
        axWaves.tick_params(
            "x",
            which="major",
            top=False,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axWaves.tick_params(
            "x",
            which="minor",
            top=False,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )
    else:
        axWaves.tick_params(
            "x",
            which="major",
            top=True,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axWaves.tick_params(
            "x",
            which="minor",
            top=True,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )


if plotJADE:
    if plotElectronEnergy:
        axJade = fig.add_subplot(numSubPlots, 1, electronEnergyPlotIndex)
        axesDict["JADE-E energy"] = axJade

        if electronEnergyPlotIndex < numSubPlots:
            junoJade.PlotData(
                fig,
                axJade,
                timeFrame,
                dataDirectory=dataDirectory,
                hiRes=plottingConfig["JADE"].getboolean("high resolution"),
                plotEphemeris=True,
                ephemerisLabels=False,
                colourmap=plottingConfig["JADE"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotElectronEnergy=True,
                plotPitchAngle=False,
            )
            axJade.set_xticklabels("")
        else:
            junoJade.PlotData(
                fig,
                axJade,
                timeFrame,
                dataDirectory=dataDirectory,
                hiRes=plottingConfig["JADE"].getboolean("high resolution"),
                plotEphemeris=True,
                ephemerisLabels=True,
                colourmap=plottingConfig["JADE"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotElectronEnergy=True,
                plotPitchAngle=False,
            )

        axJade.tick_params(
            "y",
            which="major",
            length=plottingConfig["plotting"].getfloat("y tick length"),
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJade.tick_params(
            "y",
            which="minor",
            length=plottingConfig["plotting"].getfloat("y tick length") / 2,
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJade.margins(x=0)

        if electronEnergyPlotIndex == 1:
            axJade.tick_params(
                "x",
                which="major",
                top=False,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJade.tick_params(
                "x",
                which="minor",
                top=False,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

        else:
            axJade.tick_params(
                "x",
                which="major",
                top=True,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJade.tick_params(
                "x",
                which="minor",
                top=True,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

    if plotIonEnergy:
        axJadeIons = fig.add_subplot(numSubPlots, 1, ionEnergyPlotIndex)
        axesDict["JADE I energy"] = axJadeIons

        if ionEnergyPlotIndex < numSubPlots:
            junoJADE_ions.PlotData(
                fig,
                axJadeIons,
                timeFrame,
                dataDirectory=dataDirectory,
                plotEphemeris=True,
                ephemerisLabels=False,
                colourmap=plottingConfig["JADE Ions"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotIonEnergy=True,
                ionTimeOfFlightRange=ast.literal_eval(
                    plottingConfig["JADE Ions"]["TOF range"]
                ),
            )
            axJadeIons.set_xticklabels("")
        else:
            junoJADE_ions.PlotData(
                fig,
                axJadeIons,
                timeFrame,
                dataDirectory=dataDirectory,
                plotEphemeris=True,
                ephemerisLabels=True,
                colourmap=plottingConfig["JADE Ions"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotIonEnergy=True,
                ionTimeOfFlightRange=ast.literal_eval(
                    plottingConfig["JADE Ions"]["TOF range"]
                ),
            )

        axJadeIons.tick_params(
            "y",
            which="major",
            length=plottingConfig["plotting"].getfloat("y tick length"),
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJadeIons.tick_params(
            "y",
            which="minor",
            length=plottingConfig["plotting"].getfloat("y tick length") / 2,
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJadeIons.margins(x=0)

        if ionEnergyPlotIndex == 1:
            axJadeIons.tick_params(
                "x",
                which="major",
                top=False,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJadeIons.tick_params(
                "x",
                which="minor",
                top=False,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

        else:
            axJadeIons.tick_params(
                "x",
                which="major",
                top=True,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJadeIons.tick_params(
                "x",
                which="minor",
                top=True,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

    if plotPitchAngle:
        axJadePitch = fig.add_subplot(numSubPlots, 1, pitchAnglePlotIndex)
        axesDict["JADE-E pitch"] = axJadePitch

        if pitchAnglePlotIndex < numSubPlots:
            junoJade.PlotData(
                fig,
                axJadePitch,
                timeFrame,
                dataDirectory=dataDirectory,
                hiRes=plottingConfig["JADE"].getboolean("high resolution"),
                plotEphemeris=True,
                ephemerisLabels=False,
                colourmap=plottingConfig["JADE"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotElectronEnergy=False,
                plotPitchAngle=True,
                reBin=plottingConfig["JADE"].getboolean("bin pitch angles"),
                pitchBinStep=plottingConfig["JADE"].getint("bin size"),
                pitchAngleEnergyRange=ast.literal_eval(
                    plottingConfig["JADE"]["pitch angle energy range"]
                ),
            )
            axJadePitch.set_xticklabels("")
        else:
            junoJade.PlotData(
                fig,
                axJadePitch,
                timeFrame,
                dataDirectory=dataDirectory,
                hiRes=plottingConfig["JADE"].getboolean("high resolution"),
                plotEphemeris=True,
                ephemerisLabels=True,
                colourmap=plottingConfig["JADE"]["colour map"],
                downloadNewData=directoryConfig["data"].getboolean("download new data"),
                plotElectronEnergy=False,
                plotPitchAngle=True,
                pitchBinStep=plottingConfig["JADE"].getint("bin size"),
                pitchAngleEnergyRange=ast.literal_eval(
                    plottingConfig["JADE"]["pitch angle energy range"]
                ),
            )

        axJadePitch.tick_params(
            "y",
            which="major",
            length=plottingConfig["plotting"].getfloat("y tick length"),
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJadePitch.tick_params(
            "y",
            which="minor",
            length=plottingConfig["plotting"].getfloat("y tick length") / 2,
            width=plottingConfig["plotting"].getfloat("y tick width"),
        )
        axJadePitch.margins(x=0)

        if pitchAnglePlotIndex == 1:
            axJadePitch.tick_params(
                "x",
                which="major",
                top=False,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJadePitch.tick_params(
                "x",
                which="minor",
                top=False,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

        else:
            axJadePitch.tick_params(
                "x",
                which="major",
                top=True,
                bottom=True,
                direction="inout",
                length=majorTickLength,
                width=majorTickWidth,
            )
            axJadePitch.tick_params(
                "x",
                which="minor",
                top=True,
                bottom=True,
                direction="inout",
                length=minorTickLength,
                width=minorTickWidth,
            )

# Moments
if plotDensity:
    axDensity = fig.add_subplot(numSubPlots, 1, densityPlotIndex)
    axesDict["JADE density"]

    if densityPlotIndex < numSubPlots:
        junoDerivedMoments.PlotDensity(
            fig,
            axDensity,
            timeFrame,
            dataDirectory,
            plotEphemeris=True,
            ephemerisLabels=False,
            downloadNewData=directoryConfig["data"].getboolean("download new data"),
        )
    else:
        junoDerivedMoments.PlotDensity(
            fig,
            axDensity,
            timeFrame,
            dataDirectory,
            plotEphemeris=True,
            ephemerisLabels=True,
            downloadNewData=directoryConfig["data"].getboolean("download new data"),
        )

    if densityPlotIndex == 1:
        axDensity.tick_params(
            "x",
            which="major",
            top=False,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axDensity.tick_params(
            "x",
            which="minor",
            top=False,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )

    else:
        axDensity.tick_params(
            "x",
            which="major",
            top=True,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axDensity.tick_params(
            "x",
            which="minor",
            top=True,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )


# Section controlling MAG plotting
if plotMag:
    axMag = fig.add_subplot(numSubPlots, 1, magPlotIndex)
    axesDict["MAG"] = axMag

    if magPlotIndex < numSubPlots:
        # Plot the MAG data from the junoMAG script
        junoMAG.PlotData(
            axMag,
            timeFrame,
            plotMeasurements={
                "total": plottingConfig["MAG"].getboolean("plot magnitude"),
                "cartesians": plottingConfig["MAG"].getboolean("plot cartesians"),
                "polars": plottingConfig["MAG"].getboolean("plot polars"),
                "lobe": plottingConfig["MAG"].getboolean("plot lobe"),
                "lobeUncertainty": plottingConfig["MAG"].getboolean(
                    "plot lobe uncertainty"
                ),
            },
            plotEphemeris=True,
            ephemerisLabels=False,
            linewidth=plottingConfig["MAG"].getfloat("line width"),
            componentColours=componentColours,
            lobeColour=lobeColour,
            magnitudeColour=magnitudeColour,
        )
    else:
        junoMAG.PlotData(
            axMag,
            timeFrame,
            plotMeasurements={
                "total": plottingConfig["MAG"].getboolean("plot magnitude"),
                "cartesians": plottingConfig["MAG"].getboolean("plot cartesians"),
                "polars": plottingConfig["MAG"].getboolean("plot polars"),
                "lobe": plottingConfig["MAG"].getboolean("plot lobe"),
                "lobeUncertainty": plottingConfig["MAG"].getboolean(
                    "plot lobe uncertainty"
                ),
            },
            plotEphemeris=True,
            ephemerisLabels=True,
            linewidth=plottingConfig["MAG"].getfloat("line width"),
            componentColours=componentColours,
            lobeColour=lobeColour,
            magnitudeColour=magnitudeColour,
        )

    axMag.tick_params(
        "y",
        length=plottingConfig["plotting"].getfloat("y tick length"),
        width=plottingConfig["plotting"].getfloat("y tick width"),
    )
    axMag.margins(x=0)

    if magPlotIndex == 1:
        axMag.tick_params(
            "x",
            which="major",
            top=False,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axMag.tick_params(
            "x",
            which="minor",
            top=False,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )

    else:
        axMag.tick_params(
            "x",
            which="major",
            top=True,
            bottom=True,
            direction="inout",
            length=majorTickLength,
            width=majorTickWidth,
        )
        axMag.tick_params(
            "x",
            which="minor",
            top=True,
            bottom=True,
            direction="inout",
            length=minorTickLength,
            width=minorTickWidth,
        )


# Set tick formatting and add vertical lines
for i, axis in enumerate(fig.axes):
    # vLines from file
    if (
        i % 2 == 0
        and plottingConfig["vertical lines"].getboolean("read from file") is True
    ):
        vLines.PlotFromFile(
            axis,
            i,
            timeFrame,
            plottingConfig["vertical lines"]["file path"],
            plottingConfig["vertical lines"]["file line colour"],
            vLineStyle,
        )

    # Manual vLines
    # As each axis is divided to keep widths consistant with colourbars and legends, there are
    # always twice as many axes as data plotted. These are created sequentially in the order data
    # axis, legend axis, and hence we can use the modulo to only get the even positionIndex.
    if i % 2 == 0 and len(vLinePositions) != 0:
        vLines.PlotVLines(
            axis, i, timeFrame, vLinePositions, vLineLabels, vLineColours, vLineStyle
        )

    axis.format_coord = (
        lambda x, y: ""
        # Disables the cursor coordinate display. This feature causes major slowdowns when resizing
        # the plot window.
    )


if plotTrajectories:
    axTrajectories = fig.add_subplot(numSubPlots, 1, trajectoriesPlotIndex)
    axesDict["Trajectories"] = axTrajectories

    if plottingConfig["trajectories"].getboolean("equal aspect") is True:
        aspect = "equal"
    else:
        aspect = "auto"

    axTrajectories = junoTrajectories.ThreePanelTrajectories(
        axTrajectories,
        timeFrame,
        spiceDirectory,
        frame=plottingConfig["trajectories"]["frame"],
        plottedColour=plottingConfig["trajectories"]["plotted colour"],
        extensionColour=plottingConfig["trajectories"]["extension colour"],
        timeExtension=plottingConfig["trajectories"].getint("time extension"),
        trajectoryMajorTickLength=plottingConfig["trajectories"].getfloat(
            "major tick length"
        ),
        trajectoryMinorTickLength=plottingConfig["trajectories"].getfloat(
            "minor tick length"
        ),
        majorLocator=plottingConfig["trajectories"].getfloat("major tick multiple"),
        minorLocator=plottingConfig["trajectories"].getfloat("minor tick multiple"),
        xBounds=ast.literal_eval(plottingConfig["trajectories"]["x bounds"]),
        yBounds=ast.literal_eval(plottingConfig["trajectories"]["y bounds"]),
        zBounds=ast.literal_eval(plottingConfig["trajectories"]["z bounds"]),
        aspect=aspect,
        magBoundariesRepoPath=magBoundariesRepoPath,
        plotBowShock=plottingConfig["trajectories"].getboolean("plot bow shock"),
        plotMagnetopause=plottingConfig["trajectories"].getboolean("plot magnetopause"),
        BS_p_dyn=plottingConfig["trajectories"].getfloat("BS dynamic pressure"),
        MP_p_dyn=plottingConfig["trajectories"].getfloat("MP dynamic pressure"),
        bsColour=plottingConfig["trajectories"]["bow shock colour"],
        mpColour=plottingConfig["trajectories"]["magnetopause colour"],
    )

# Move the subplots together and add room below for ephemeris labels
plt.subplots_adjust(hspace=panelSpacing, bottom=0.2)


userAdditions.UserAdditions(fig=fig, axes=axesDict)

if not directoryConfig["plotting"].getboolean("save figure"):
    print("Showing figure")
    plt.show()
else:
    # Test if output directory exists
    if not os.path.exists("./JUPT_output/"):
        os.system("mkdir ./JUPT_output/")

    plt.savefig("./JUPT_output/" + str(configName) + ".png", format="png")
