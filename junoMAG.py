import speasy as spz
import numpy as np
import matplotlib.dates as mdates
import datetime
from mpl_toolkits import axes_grid1

import junoEphemeris

def PlotData(ax, timeFrame, plotEphemeris=False, ephemerisLabels=False, polarCoordinates=True, linewidth=1):
    # Takes one of the subplot axes as input

    print("Retrieving mag data...")
    junoFGM = spz.amda.get_parameter("juno_fgm_orb1_jso", timeFrame[0], timeFrame[1])
    
    mag = np.transpose(junoFGM.values)
    magX = mag[0]
    magY = mag[1]
    magZ = mag[2]
    magTotal = [np.sqrt(x**2 + y**2 + z**2) for x,y,z in zip(magX, magY, magZ)]

    time = junoFGM.time
    if not plotEphemeris:
        timePlotted = junoFGM.time
    else:
        # If ephemerides are added later, an index must be used instead of a time table for the plot
        timePlotted = np.arange(len(junoFGM.time))
   
    if not polarCoordinates:
        ax.plot(timePlotted, magX, color="red", label="$B_x$", linewidth=linewidth)
        ax.plot(timePlotted, magY, color="green", label="$B_y$", linewidth=linewidth)
        ax.plot(timePlotted, magZ, color="blue", label="$B_z$", linewidth=linewidth)
        ax.plot(timePlotted, magTotal, color="black", label="$|B|$", linewidth=linewidth)
    else:
        polarCoords = CartesianPosToPolarPos(magX, magY, magZ, time, timeFrame)
        magR = polarCoords[0]
        magTheta = polarCoords[1]
        magPhi = polarCoords[2]

        ax.plot(timePlotted, magR, color="red", label="$B_R$", linewidth=linewidth)
        ax.plot(timePlotted, magTheta, color="green", label="$B_\\theta$", linewidth=linewidth)
        ax.plot(timePlotted, magPhi, color="blue", label="$B_\phi$", linewidth=linewidth)
        ax.plot(timePlotted, magTotal, color="black", label="$|B|$", linewidth=linewidth)

    ax.hlines(0, xmin=timePlotted[0], xmax=timePlotted[-1], colors="grey", linestyles="dotted")

    # Shrink axis by 20% to make room for legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    divider = axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad="2%")
    cax.axis("off")

    ax.legend(loc="center left", ncol=1, bbox_to_anchor=(1, 0.5), labelspacing=2)

    unit = junoFGM.unit
    
    ax.set_ylabel(f"B ({unit})")
    ax.margins(0)

    if not plotEphemeris:
        dateFormat = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(dateFormat)
        # ax.set_xlabel("Date and Time") 
        # ax.set_xticklabels([])

    else:
        ax = junoEphemeris.PlotEphemeris(ax, time, timeFrame, resolutionFactor=60, labels=ephemerisLabels)
        # ax.set_xlabel("Ephemeris")


def CartesianPosToPolarPos(bX, bY, bZ, dataTime, timeFrame):
    # Method adapted from corentin
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
    spacecraftR = np.sqrt(spacecraftX_interp**2 + spacecraftY_interp**2 + spacecraftZ_interp**2)
    spacecraftTheta = np.arccos(spacecraftZ_interp / spacecraftR)
    spacecraftPhi = np.arctan2(spacecraftY_interp, spacecraftX_interp)

    # These can now be used to transform the magnetic field data to polar coordinates
    bR = bX * np.sin(spacecraftTheta) * np.cos(spacecraftPhi) + bY * np.sin(spacecraftTheta) * np.sin(spacecraftPhi) + bZ * np.cos(spacecraftTheta)
    bTheta = bX * np.cos(spacecraftTheta) * np.cos(spacecraftPhi) + bY * np.cos(spacecraftTheta) * np.sin(spacecraftPhi) - bZ * np.sin(spacecraftTheta)
    bPhi = bY * np.cos(spacecraftPhi) - bX * np.sin(spacecraftPhi)
        
    return [bR, bTheta, bPhi]

def datetime64_to_datetime(time):
    timeStr = [np.datetime_as_string(t, unit="s") for t in time]
    return datestring_to_datetime(timeStr)

@np.vectorize
def datestring_to_datetime(time):
    #return datetime.datetime.strptime(np.datetime_as_string(time,unit="s"),"%Y-%m-%dT%H:%M:%S")
    return datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")
