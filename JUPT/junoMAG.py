import datetime

import matplotlib.dates as mdates
import numpy as np
import speasy as spz
from mpl_toolkits import axes_grid1

import junoEphemeris


def PlotData(
    ax,
    timeFrame,
    plotMeasurements,
    componentColours=["red", "green", "blue"],
    lobeColour="orange",
    magnitudeColour="black",
    plotEphemeris=False,
    ephemerisLabels=False,
    polarCoordinates=True,
    linewidth=1,
    plotLobeField=False,
):
    # Takes one of the subplot axes as input
    """Plots Juno MAG data from the AMDA database

    Arguments:
    ax -- Matplotlib subplot axis
    timeFrame -- (list) A list containing the start and end time of the plot in string format eg. ["2016-12-18T00:00:00", "2016-12-20T12:00:00"]
    plotDict -- (dictionary) A dictionary which describes what elements should be plotted

    plotEphemeris -- (bool) Should the x axis be reformatted for ephemeris data
    ephemerisLabels -- (bool) Should the ephemeris data be displayed on the x axis of this subplot

    polarCoordinates -- (bool) Should the MAG data be plotted in spherical polar coordinates instead of cartesians

    linewidth -- (float) Thickness of the lines plotted
    plotLobeField -- (bool) Should the expected lobe field be plotted

    Returns:
    ax -- Matplotlib subplot axis
    """

    print("Retrieving mag data...")
    junoFGM = spz.amda.get_parameter("juno_fgm_orb1_jso", timeFrame[0], timeFrame[1])

    mag = np.transpose(junoFGM.values)
    magX = mag[0]
    magY = mag[1]
    magZ = mag[2]
    magTotal = [np.sqrt(x**2 + y**2 + z**2) for x, y, z in zip(magX, magY, magZ)]

    time = junoFGM.time
    if not plotEphemeris:
        timePlotted = junoFGM.time
    else:
        # If ephemerides are added later, an index must be used instead of a time table for the plot
        timePlotted = np.arange(len(junoFGM.time))

    radialDist = junoEphemeris.PullEphemerisData("juno_jup_r", time, timeFrame)
    bLobe = []
    bLobe_err_plus = []
    bLobe_err_minus = []
    for r in radialDist:
        lobeField = LobeField(r)
        bLobe.append(lobeField[0])
        bLobe_err_plus.append(lobeField[1])
        bLobe_err_minus.append(lobeField[2])

    if plotMeasurements["total"]:
        ax.plot(
            timePlotted,
            magTotal,
            color=magnitudeColour,
            label="$|B|$",
            linewidth=linewidth,
        )

    if plotMeasurements["cartesians"]:
        ax.plot(
            timePlotted,
            magX,
            color=componentColours[0],
            label="$B_x$",
            linewidth=linewidth,
        )
        ax.plot(
            timePlotted,
            magY,
            color=componentColours[1],
            label="$B_y$",
            linewidth=linewidth,
        )
        ax.plot(
            timePlotted,
            magZ,
            color=componentColours[2],
            label="$B_z$",
            linewidth=linewidth,
        )

    if plotMeasurements["polars"]:
        magR, magTheta, magPhi = CartesiansToPolars(magX, magY, magZ, time, timeFrame)

        ax.plot(
            timePlotted,
            magR,
            color=componentColours[0],
            label="$B_r$",
            linewidth=linewidth,
        )
        ax.plot(
            timePlotted,
            magTheta,
            color=componentColours[1],
            label="$B_\\theta$",
            linewidth=linewidth,
        )
        ax.plot(
            timePlotted,
            magPhi,
            color=componentColours[2],
            label="$B_\phi$",
            linewidth=linewidth,
        )

    if plotMeasurements["lobe"]:
        ax.plot(
            timePlotted,
            bLobe,
            color=lobeColour,
            label="B$_{Lobe}$\nK & K (2002)",
            linewidth=3 * linewidth,
        )

    if plotMeasurements["lobeUncertainty"]:
        ax.plot(
            timePlotted,
            bLobe_err_plus,
            color=lobeColour,
            linewidth=2 * linewidth,
            linestyle="dashed",
        )
        ax.plot(
            timePlotted,
            bLobe_err_minus,
            color=lobeColour,
            linewidth=2 * linewidth,
            linestyle="dashed",
        )
        ax.fill_between(
            timePlotted,
            bLobe_err_minus,
            bLobe_err_plus,
            color=lobeColour,
            alpha=0.2,
            label="B$_{Lobe}$\nerror\nregion",
        )

    # Add dotted line at y=0
    ax.hlines(
        0, xmin=timePlotted[0], xmax=timePlotted[-1], colors="grey", linestyles="dotted"
    )

    # Shrink axis by 20% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    divider = axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad="2%")
    cax.axis("off")

    legend = ax.legend(
        loc="center left", ncol=1, bbox_to_anchor=(1, 0.5), labelspacing=2
    )

    # change the line width for the legend
    for line in legend.get_lines():
        line.set_linewidth(2 * linewidth)

    unit = junoFGM.unit

    ax.set_ylabel(f"B ({unit})")

    if not plotEphemeris:
        dateFormat = mdates.DateFormatter("%H:%M")
        ax.xaxis.set_major_formatter(dateFormat)

    else:
        ax = junoEphemeris.PlotEphemeris(ax, time, timeFrame, labels=ephemerisLabels)

    return ax


def LobeField(r):
    """Plots the lobe field estimation where r is the radial distance from the jupiter"""
    # From Sean McEntee
    bLobe = 2900 * r ** (-1.37)  # Khurana definition
    bLobe_err_plus = 2970 * r ** (-1.36)
    bLobe_err_minus = 2830 * r ** (-1.38)

    return (bLobe, bLobe_err_plus, bLobe_err_minus)


def CartesiansToPolars(bX, bY, bZ, dataTime, timeFrame):
    # Method adapted from corentin
    """Converts MAG data in cartesians to spherical polar coordinates using the spacecraft's position

    Arguments:
    bX, bY, bZ -- (list) MAG data in cartesian coordinates

    dataTime -- (list) The time parameter corresponding to the cartesian data. As the position of the spacecraft is needed to convert to polars, the time is required to interpolate the data to match the time of the ephemeris data.
    timeFrame -- (list) The time frame with which to pull the ephemeris data. This should be the same as used to pull the cartesian data.

    Returns:
    A touple contain the MAG data in polar spherical coordinates.
    """

    ephemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])
    ephemerisTime = ephemeris.time

    spacecraftCoords = np.transpose(ephemeris.values)

    spacecraftX = spacecraftCoords[0]
    spacecraftY = spacecraftCoords[1]
    spacecraftZ = spacecraftCoords[2]

    ephemerisTimeTransformed = datetime64_to_datetime(ephemerisTime)
    dataTimeTransformed = datetime64_to_datetime(dataTime)

    ephemerisTime_seconds = [el.timestamp() for el in ephemerisTimeTransformed]
    dataTime_seconds = [el.timestamp() for el in dataTimeTransformed]

    # Interpolate to match the coordinates to the data
    spacecraftX_interp = np.interp(dataTime_seconds, ephemerisTime_seconds, spacecraftX)
    spacecraftY_interp = np.interp(dataTime_seconds, ephemerisTime_seconds, spacecraftY)
    spacecraftZ_interp = np.interp(dataTime_seconds, ephemerisTime_seconds, spacecraftZ)

    # Transfrom to new coordinates
    spacecraftR = np.sqrt(
        spacecraftX_interp**2 + spacecraftY_interp**2 + spacecraftZ_interp**2
    )
    spacecraftTheta = np.arccos(spacecraftZ_interp / spacecraftR)
    spacecraftPhi = np.arctan2(spacecraftY_interp, spacecraftX_interp)

    # These can now be used to transform the magnetic field data to polar coordinates
    bR = (
        bX * np.sin(spacecraftTheta) * np.cos(spacecraftPhi)
        + bY * np.sin(spacecraftTheta) * np.sin(spacecraftPhi)
        + bZ * np.cos(spacecraftTheta)
    )
    bTheta = (
        bX * np.cos(spacecraftTheta) * np.cos(spacecraftPhi)
        + bY * np.cos(spacecraftTheta) * np.sin(spacecraftPhi)
        - bZ * np.sin(spacecraftTheta)
    )
    bPhi = bY * np.cos(spacecraftPhi) - bX * np.sin(spacecraftPhi)

    return (bR, bTheta, bPhi)


def datetime64_to_datetime(time):
    """Converts numpy type datetime64 to type datetime"""
    timeStr = [np.datetime_as_string(t, unit="s") for t in time]
    return datestring_to_datetime(timeStr)


@np.vectorize
def datestring_to_datetime(time):
    """Converts datestring (i.e. np.datetime_as_string) to type datetime"""
    return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
