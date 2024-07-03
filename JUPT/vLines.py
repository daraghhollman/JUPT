from datetime import datetime

import matplotlib.pyplot as plt
import pandas


def PlotVLines(ax, axisIndex, timeFrame, positions, labels, colours, linestyle):
    for position, label, colour in zip(positions, labels, colours):
        # convert from string to datetime
        posTime = datetime.strptime(position, "%Y-%m-%dT%H:%M:%S")
        startTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
        endTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")
        axisPos = (posTime - startTime).total_seconds()
        axisLength = (endTime - startTime).total_seconds()

        ax.axvline(
            axisPos, color=colour, linestyle=linestyle
        )  # x coord in seconds from start

        if label != "" and axisIndex == 0:  # Labels on top plot only
            plt.text(
                (axisPos / axisLength),
                1.05,
                label,
                transform=ax.transAxes,
                color=colour,
                ha="center",
                va="center",
            )


def PlotFromFile(ax, axisIndex, timeFrame, path, colour, linestyle):
    data = pandas.read_csv(path, sep=";")

    dates = data["Date (year/month/day)"]
    times = data["Time (HH:MM)"]
    boundaries = data["Boundary"]
    labels = data["In/Out"]

    for date, time, label, boundary in zip(dates, times, labels, boundaries):
        if boundary == "bow shock":
            if label == "in":
                label = "BS-I"
            elif label == "out":
                label = "BS-O"

        elif boundary == "magnetopause":
            if label == "in":
                label = "MP-I"
            elif label == "out":
                label = "MP-O"

        # convert from string to datetime
        posTime = datetime.strptime(date + time, "%Y/%m/%d%H:%M")

        startTime = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
        endTime = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")

        axisPos = (posTime - startTime).total_seconds()
        axisLength = (endTime - startTime).total_seconds()

        if axisPos < 0 or axisPos > axisLength:
            continue

        ax.axvline(
            axisPos, color=colour, linestyle=linestyle
        )  # x coord in seconds from start

        if axisIndex == 0:
            plt.text(
                (axisPos / axisLength),
                1.05,
                label,
                transform=ax.transAxes,
                color=colour,
                ha="center",
                va="center",
            )
