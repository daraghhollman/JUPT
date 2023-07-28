import spiceypy as spice
from datetime import datetime
import datetime as dt
from mpl_toolkits.axes_grid1 import make_axes_locatable, SubplotDivider
from matplotlib.patches import Circle 
import numpy as np

def ThreePanelTrajectories(ax, timeFrame, spiceDirectory, frame="JUNO_JSS", centre="JUPITER", timeStep_mins=1, scale=71492, unitLabel="R$_J$", timeExtension=25, plottedColour="magenta", extensionColour="black"):

    print("Plotting trajectories...")

    print("Loading SPICE kernels")
    print(spiceDirectory + "juno/metakernel_juno.txt")
    spice.furnsh(spiceDirectory + "juno/metakernel_juno.txt")

    startTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")

    preStartTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S") - dt.timedelta(days=timeExtension)
    postEndTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(days=timeExtension)

    dates = np.arange(startTime, endTime, dt.timedelta(minutes=timeStep_mins)).astype(dt.datetime)
    extendedDates = np.arange(preStartTime, postEndTime, dt.timedelta(minutes=timeStep_mins)).astype(dt.datetime)

    ets = [spice.datetime2et(date) for date in dates]
    extendedEts = [spice.datetime2et(date) for date in extendedDates]

    print("Querying SPICE")
    positions, ltimes = spice.spkpos("Juno", ets, frame, "NONE", centre)
    extendedPositions, ltimes = spice.spkpos("Juno", extendedEts, frame, "NONE", centre)


    print("Rescalling positions")
    # Normalise by scale factor (Jupiter Radius by default)
    positions_scaled = []
    for position in positions:
        scaled_position = np.divide(position, scale)

        positions_scaled.append(scaled_position)

    positions_scaled = np.array(positions_scaled)
    positionsDict = {
        "x": positions_scaled[:,0],
        "y": positions_scaled[:,1],
        "z": positions_scaled[:,2]
    }
    extendedPositions_scaled = []
    for position in extendedPositions:
        scaled_position = np.divide(position, scale)

        extendedPositions_scaled.append(scaled_position)

    extendedPositions_scaled = np.array(extendedPositions_scaled)
    extendedPositionsDict = {
        "x": extendedPositions_scaled[:,0],
        "y": extendedPositions_scaled[:,1],
        "z": extendedPositions_scaled[:,2]
    }


    divider = make_axes_locatable(ax)
    xzAxis = divider.append_axes("left", size="100%", pad="40%")

    xyAxis = divider.append_axes("left", size="100%", pad="40%")
    yzAxis = ax


    axes = (xyAxis, xzAxis, yzAxis)


    for ax in axes:
        jupiterCircle = Circle((0,0), 1, facecolor="black", edgecolor="black")
        ax.add_patch(jupiterCircle)

        ax.set_aspect("equal")

    xyAxis.plot(positionsDict["x"], positionsDict["y"], color=plottedColour, linewidth=4, zorder=10, label="Trajectory Plotted")
    xyAxis.plot(extendedPositionsDict["x"], extendedPositionsDict["y"], color=extensionColour, label=f"Trajectory $\pm$ {timeExtension} days")
    xyAxis.set_xlabel("X$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")
    xyAxis.set_ylabel("Y$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")

    xzAxis.plot(positionsDict["x"], positionsDict["z"], color=plottedColour, linewidth=4, zorder=10)
    xzAxis.plot(extendedPositionsDict["x"], extendedPositionsDict["z"], color=extensionColour)
    xzAxis.set_xlabel("X$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")
    xzAxis.set_ylabel("Z$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")

    yzAxis.plot(positionsDict["y"], positionsDict["z"], color=plottedColour, linewidth=4, zorder=10)
    yzAxis.plot(extendedPositionsDict["y"], extendedPositionsDict["z"], color=extensionColour)
    yzAxis.set_xlabel("Y$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")
    yzAxis.set_ylabel("Z$_{"+ f"{frame[5:]}" + "}$ (R$_J$)")

    xyAxis.legend()


    return axes
