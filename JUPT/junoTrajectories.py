import datetime as dt
import sys
from datetime import datetime

import numpy as np
import spiceypy as spice
from matplotlib.patches import Circle
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable


def ThreePanelTrajectories(
    ax,
    timeFrame,
    spiceDirectory,
    frame="JUNO_JSS",
    centre="JUPITER",
    timeStep_mins=1,
    scale=71492,
    unitLabel="R$_J$",
    timeExtension=25,
    plottedColour="magenta",
    extensionColour="black",
    trajectoryMajorTickLength=20,
    trajectoryMinorTickLength=10,
    majorLocator=20,
    minorLocator=10,
    xBounds=[],
    yBounds=[],
    zBounds=[],
    aspect="auto",
    magBoundariesRepoPath="",
    plotBowShock=False,
    plotMagnetopause=False,
    BS_p_dyn=0.3,
    MP_p_dyn=0.3,
    bsColour="black",
    mpColour="purple",
):
    if magBoundariesRepoPath != "":
        sys.path.append(magBoundariesRepoPath)
        from pdyn_to_ms_boundaries import pdyn_to_bs, pdyn_to_mp

    print("Plotting trajectories...")

    print("Loading SPICE kernels")
    print(spiceDirectory + "juno/metakernel_juno.txt")
    spice.furnsh(spiceDirectory + "juno/metakernel_juno.txt")

    startTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
    endTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")

    preStartTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S") - dt.timedelta(
        days=timeExtension
    )
    postEndTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(
        days=timeExtension
    )

    dates = np.arange(startTime, endTime, dt.timedelta(minutes=timeStep_mins)).astype(
        dt.datetime
    )
    extendedDates = np.arange(
        preStartTime, postEndTime, dt.timedelta(minutes=timeStep_mins)
    ).astype(dt.datetime)

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
        "x": positions_scaled[:, 0],
        "y": positions_scaled[:, 1],
        "z": positions_scaled[:, 2],
    }
    extendedPositions_scaled = []
    for position in extendedPositions:
        scaled_position = np.divide(position, scale)

        extendedPositions_scaled.append(scaled_position)

    extendedPositions_scaled = np.array(extendedPositions_scaled)
    extendedPositionsDict = {
        "x": extendedPositions_scaled[:, 0],
        "y": extendedPositions_scaled[:, 1],
        "z": extendedPositions_scaled[:, 2],
    }

    divider = make_axes_locatable(ax)
    xzAxis = divider.append_axes("left", size="100%", pad="40%")

    xyAxis = divider.append_axes("left", size="100%", pad="40%")
    yzAxis = ax

    axes = (xyAxis, xzAxis, yzAxis)

    concentricCircleRadii = np.arange(
        10,
        max(
            np.array([xBounds, yBounds, zBounds]).max(),
            np.array([xBounds, yBounds, zBounds]).min(),
            key=abs,
        )
        + 2 * majorLocator,
        majorLocator,
    )

    for ax in axes:
        ax.scatter(0, 0, color="orange", marker="o", label="Jupiter", zorder=5)
        ax.tick_params(
            which="major",
            direction="in",
            length=trajectoryMajorTickLength,
            bottom=True,
            top=True,
            left=True,
            right=True,
        )
        ax.tick_params(
            which="minor",
            direction="in",
            length=trajectoryMinorTickLength,
            bottom=True,
            top=True,
            left=True,
            right=True,
        )

        ax.xaxis.set_major_locator(MultipleLocator(majorLocator))
        ax.xaxis.set_minor_locator(MultipleLocator(minorLocator))
        ax.yaxis.set_major_locator(MultipleLocator(majorLocator))
        ax.yaxis.set_minor_locator(MultipleLocator(minorLocator))

        ax.set_aspect(aspect)

        for r in concentricCircleRadii:
            circ = Circle((0, 0), radius=r, edgecolor="lightgrey", facecolor="None")
            ax.add_artist(circ)

    xyAxis.plot(
        positionsDict["x"],
        positionsDict["y"],
        color=plottedColour,
        linewidth=4,
        zorder=10,
    )
    xyAxis.plot(
        extendedPositionsDict["x"],
        extendedPositionsDict["y"],
        color=extensionColour,
        zorder=2,
    )
    xyAxis.set_xlabel("X$_{" + f"{frame[5:]}" + "}$ (R$_J$)")
    xyAxis.set_ylabel("Y$_{" + f"{frame[5:]}" + "}$ (R$_J$)")

    xzAxis.plot(
        positionsDict["x"],
        positionsDict["z"],
        color=plottedColour,
        linewidth=4,
        zorder=10,
        label="Trajectory Plotted",
    )
    xzAxis.plot(
        extendedPositionsDict["x"],
        extendedPositionsDict["z"],
        color=extensionColour,
        zorder=2,
        label=f"Trajectory $\pm$ {timeExtension} days",
    )
    xzAxis.set_xlabel("X$_{" + f"{frame[5:]}" + "}$ (R$_J$)")
    xzAxis.set_ylabel("Z$_{" + f"{frame[5:]}" + "}$ (R$_J$)")

    yzAxis.plot(
        positionsDict["y"],
        positionsDict["z"],
        color=plottedColour,
        linewidth=4,
        zorder=10,
    )
    yzAxis.plot(
        extendedPositionsDict["y"],
        extendedPositionsDict["z"],
        color=extensionColour,
        zorder=2,
    )
    yzAxis.set_xlabel("Y$_{" + f"{frame[5:]}" + "}$ (R$_J$)")
    yzAxis.set_ylabel("Z$_{" + f"{frame[5:]}" + "}$ (R$_J$)")

    if xBounds != []:
        xyAxis.set_xlim(xBounds)
        xzAxis.set_xlim(xBounds)

    if yBounds != []:
        xyAxis.set_ylim(yBounds)
        yzAxis.set_xlim(yBounds)

    if zBounds != []:
        xzAxis.set_ylim(zBounds)
        yzAxis.set_ylim(zBounds)

    if frame != "JUNO_JSS" and (plotBowShock or plotMagnetopause) is True:
        raise ValueError(
            "Not implemented: Cannot plot magnetopsheric boundaries in coordinate systems other than JSS."
        )

    # Plot magnetopsheric boundaries
    if plotBowShock:
        (x_eq, y_eq, standoff) = pdyn_to_bs(Pdyn=BS_p_dyn, equatorial=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        xyAxis.plot(x_eq[0], y_eq[0], linestyle="dashed", color=bsColour, zorder=5)
        xyAxis.plot(x_eq[1], y_eq[1], linestyle="dashed", color=bsColour, zorder=5)

        (x_eq, z_eq, standoff) = pdyn_to_bs(Pdyn=BS_p_dyn, noon_midnight=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        xzAxis.plot(
            x_eq[0],
            z_eq[0],
            linestyle="dashed",
            color=bsColour,
            zorder=5,
            label="Bow Shock P$_{dyn}$=" + str(BS_p_dyn) + "\n    Joy et al. (2002)",
        )
        xzAxis.plot(x_eq[1], z_eq[1], linestyle="dashed", color=bsColour, zorder=5)

        (y_eq, z_eq, standoff) = pdyn_to_bs(Pdyn=BS_p_dyn, dawn_dusk=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        yzAxis.plot(y_eq[0], z_eq[0], linestyle="dashed", color=bsColour, zorder=5)
        yzAxis.plot(y_eq[1], z_eq[1], linestyle="dashed", color=bsColour, zorder=5)

    if plotMagnetopause:
        (x_eq, y_eq, standoff) = pdyn_to_mp(Pdyn=MP_p_dyn, equatorial=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        xyAxis.plot(x_eq[0], y_eq[0], linestyle="dashed", color=mpColour, zorder=5)
        xyAxis.plot(x_eq[1], y_eq[1], linestyle="dashed", color=mpColour, zorder=5)

        (x_eq, z_eq, standoff) = pdyn_to_mp(Pdyn=MP_p_dyn, noon_midnight=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        xzAxis.plot(
            x_eq[0],
            z_eq[0],
            linestyle="dashed",
            color=mpColour,
            zorder=5,
            label="Magnetopause P$_{dyn}$=" + str(MP_p_dyn) + "\n    Joy et al. (2002)",
        )
        xzAxis.plot(x_eq[1], z_eq[1], linestyle="dashed", color=mpColour, zorder=5)

        (y_eq, z_eq, standoff) = pdyn_to_mp(Pdyn=MP_p_dyn, dawn_dusk=True)
        # Plot is called twice as the function returns the positive y and negative y separately
        yzAxis.plot(y_eq[0], z_eq[0], linestyle="dashed", color=mpColour, zorder=5)
        yzAxis.plot(y_eq[1], z_eq[1], linestyle="dashed", color=mpColour, zorder=5)

    xzAxis.legend(bbox_to_anchor=(0.5, 1.2), loc="center", ncol=5, borderaxespad=0)

    return axes
