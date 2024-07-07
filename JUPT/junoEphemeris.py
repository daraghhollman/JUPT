import datetime

import matplotlib.ticker as ticker
import numpy as np
import pandas
import speasy as spz


# Editted code from corentin
def format_xlabel(time, r, lon, lat, mlat):
    timeLength = len(time)
    hoursAndMinutes = pandas.to_datetime(time).strftime("%H:%M")
    dayAndMonthAndYear = pandas.to_datetime(time).strftime("%Y-%m-%d")

    def inner_function(index, pos=None):
        #  np.clip will avoid having to check the value (to see if it's outside the array)
        clipedIndex = np.clip(int(index + 0.5), 0, timeLength - 1)
        return f"{dayAndMonthAndYear[clipedIndex]}\n{hoursAndMinutes[clipedIndex]}\n{r[clipedIndex]:5.2f}\n{lon[clipedIndex]:5.2f}\n{lat[clipedIndex]:5.2f}\n{mlat[clipedIndex]:5.2f}"

    return inner_function


def PlotEphemeris(
    ax,
    dataTime,
    timeFrame,
    resolutionFactor=None,
    labels=True,
    labelFontsize=11,
    labelsPos=[-40, -40],
    posSpacer=1,
    isJade=False,
    verbosity=0
):
    """Plot ephemeris data as axix tick labels

    Arguments:
    ax -- (matplotlib axis)
    dataTime -- (list) Containing the time data corresponding to the data
    timeFrame -- (list) Time frame from which the data was pulled from
    resolutionFactor -- (int) Parameter to account for differening resolutions (This is no longer needed)
    labels -- (bool) Should the ephemeris data labels be displayed (i.e. lon, lat...)
    labelFontSize -- (float) Fontsize of the labels
    labelsPos -- (list) Coordinates of the labels
    posSpacer -- (float) Distance between each label

    """

    # Takes a subplot axis as input
    if verbosity > 0:
        print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter(
        "juno_eph_orb_jso", timeFrame[0], timeFrame[1]
    )

    distanceValues = PullEphemerisData("juno_jup_r", dataTime, timeFrame, verbosity=verbosity)
    longitudeValues = PullEphemerisData("juno_jup_lon", dataTime, timeFrame, verbosity=verbosity)
    latitudeValues = PullEphemerisData("juno_jup_lat", dataTime, timeFrame, verbosity=verbosity)
    mLatitudeValues = PullEphemerisData("juno_jup_mlat", dataTime, timeFrame, verbosity=verbosity)

    ephemerisTime = junoEphemeris.time

    # to be feed into the format_xlabel function, time array needs to be a datetime.datetime object
    # from numpy.datetime64 --> datetime.datetime, one first needs to transform numpy.datetime64 --> numpy.array(dtype='str'):
    # then to datetime
    timeTransformed = datetime64_to_datetime(dataTime, isJade=isJade)

    if verbosity > 1:
        print("Setting ticks")

    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(
            format_xlabel(
                timeTransformed,
                distanceValues,
                longitudeValues,
                latitudeValues,
                mLatitudeValues,
            )
        )
    )

    # Following section adapted from Corentin
    timedelta_seconds = np.timedelta64(
        ephemerisTime[-1] - ephemerisTime[0]
    ).astype(
        "timedelta64[s]"
    )  # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds
    if verbosity > 2:
        print(f"TIMEDELTA; Type: {type(timedelta_seconds)}, Value: {timedelta_seconds}")

    major_locator, minor_locator = CalculateTickSpread(timedelta_seconds, verbosity=verbosity)

    if resolutionFactor is None:
        resolutionFactor = len(dataTime) / (timedelta_seconds.astype("float") / 60)
        if verbosity > 2:
            print(f"Resolution factor calculated to be {resolutionFactor}")

    major_locator = np.multiply(
        major_locator, resolutionFactor
    )  # resolutionFactor is simply a multiplier to deal with data of differening resolution. It multiplies the tick location - which by default expect the time axis to be of resolution 1 minute - such that the ticks spread over the whole axis.
    minor_locator = np.multiply(minor_locator, resolutionFactor)

    ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))

    if verbosity > 1:
        print("Calculated tick spread")

    # Set ephemeris labels

    if labels:
        ax.annotate(
            "R (R$_J$)",
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(labelsPos[0], labelsPos[1] - 0 * labelFontsize),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="center",
            fontsize=labelFontsize,
        )
        ax.annotate(
            "Lon$_{III}$ ($^\circ$)",
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(labelsPos[0], labelsPos[1] - 1 * labelFontsize - posSpacer),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="center",
            fontsize=labelFontsize,
        )
        ax.annotate(
            "Lat ($^\circ$)",
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(labelsPos[0], labelsPos[1] - 2 * labelFontsize - 2 * posSpacer),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="center",
            fontsize=labelFontsize,
        )
        ax.annotate(
            "MLat ($^\circ$)",
            xy=(0, 0),
            xycoords="axes fraction",
            xytext=(labelsPos[0], labelsPos[1] - 3 * labelFontsize - 3 * posSpacer),
            textcoords="offset points",
            horizontalalignment="right",
            verticalalignment="center",
            fontsize=labelFontsize,
        )
    else:
        ax.set_xticklabels("")

    return ax


def PullEphemerisData(amdaId, inputTime, timeFrame, verbosity=0):
    if verbosity > 1:
        print(f"Retrieving {amdaId}")
    spzData = spz.amda.get_parameter(amdaId, timeFrame[0], timeFrame[1])

    data = np.transpose(spzData.values)[0]
    time = spzData.time

    # Interpolate to match data
    inputTimeTransformed = datetime64_to_datetime(inputTime)
    timeTransformed = datetime64_to_datetime(time)

    inputTime_seconds = [el.timestamp() for el in inputTimeTransformed]
    time_seconds = [el.timestamp() for el in timeTransformed]

    interpolatedData = np.interp(inputTime_seconds, time_seconds, data)

    return interpolatedData


def datetime64_to_datetime(time, isJade=False):
    timeStr = [np.datetime_as_string(t, unit="s") for t in time]
    return datestring_to_datetime(timeStr, isJade)


def CoordLengthsToMatchTime(time, coords):
    newCoordsList = []
    for direction in coords:
        newCoordinates = []

        for i in range(1, len(time) + 1):
            newCoordinates.append(direction[int(len(direction) / len(time) * i) - 1])

        newCoordsList.append(newCoordinates)
    return newCoordsList


def CalculateTickSpread(timeDelta, verbosity=0):
    # Adjusted code taken from Corentin, function takes the timedelta plotted in hours.
    dayLength_mins = 1400  # number of minutes in one day

    timeDelta = timeDelta.astype("float") / 3600

    if timeDelta < 0.25:
        # Plot every 5 mins
        major = np.arange(0, dayLength_mins, 1)
        minor = np.arange(0, dayLength_mins, 0.1)

    elif timeDelta >= 0.25 and timeDelta < 0.5:
        # Plot every 5 mins
        major = np.arange(0, dayLength_mins, 5)
        minor = np.arange(0, dayLength_mins, 1)
    elif timeDelta >= 0.5 and timeDelta < 1.0:
        # Plot every 10 mins
        major = np.arange(0, dayLength_mins, 10)
        minor = np.arange(0, dayLength_mins, 2)
    elif timeDelta >= 1.0 and timeDelta < 2.0:
        # Plot every 15 mins
        major = np.arange(0, dayLength_mins, 15)
        minor = np.arange(0, dayLength_mins, 5)
    elif timeDelta >= 2.0 and timeDelta < 3.0:
        # Plot every 20 mins
        major = np.arange(0, dayLength_mins, 20)
        minor = np.arange(0, dayLength_mins, 5)
    elif timeDelta >= 3.0 and timeDelta < 4.0:
        # Plot every 30 mins
        major = np.arange(0, dayLength_mins, 30)
        minor = np.arange(0, dayLength_mins, 10)
    elif timeDelta >= 4.0 and timeDelta < 8.0:
        # Plot every hour
        major = np.arange(0, dayLength_mins, 60)
        minor = np.arange(0, dayLength_mins, 10)
    elif timeDelta >= 8.0 and timeDelta < 16.0:
        # Plot every 2 hours
        major = np.arange(0, dayLength_mins, 60 * 2)
        minor = np.arange(0, dayLength_mins, 15)
    elif timeDelta >= 16.0 and timeDelta < 24.0:
        # Plot every 3 hours
        major = np.arange(0, dayLength_mins, 60 * 3)
        minor = np.arange(0, dayLength_mins, 60)
    elif timeDelta >= 24.0 and timeDelta < 48.0:
        # Plot every 6 hours
        major = np.arange(0, dayLength_mins * 2, 60 * 6)
        minor = np.arange(0, dayLength_mins * 2, 60)
    elif timeDelta >= 2 * 24.0 and timeDelta < 5 * 24.0:
        # Plot every 12 hours
        major = np.arange(0, dayLength_mins * (timeDelta / 24 + 1), 60 * 12)
        minor = np.arange(0, dayLength_mins * (timeDelta / 24 + 1), 60 * 2)
    elif timeDelta >= 5 * 24.0:
        # Plot every day
        major = np.arange(0, dayLength_mins * (timeDelta / 24 + 1), 60 * 24)
        minor = np.arange(0, dayLength_mins * (timeDelta / 24 + 1), 60 * 4)

    if verbosity > 2:
        print(
            f"Major ticks every: {(major[1] - major[0])/60} hours, Minor ticks every: {(minor[1] - minor[0])/60} hours"
        )

    return (major, minor)


@np.vectorize
def datestring_to_datetime(time, isJade=False):
    if isJade:
        return datetime.datetime.strptime(
            time, "%Y-%m-%dT%H:%M:%S"
        ) + datetime.timedelta(seconds=1)
    else:
        return datetime.datetime.strptime(time, "%Y-%m-%dT%H:%M:%S")
