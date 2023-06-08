import speasy as spz
import numpy as np
import matplotlib.ticker as ticker
import datetime

# Editted code from corentin
def format_xlabel(time, x, y, z):
    def inner_function(index, pos=None):
        int_index = int(index)

        if int_index >= len(time):
            return ""
        return f"{str(time)}"#\n{x[int_index]}\n{y[int_index]}\n{z[int_index]}"

def PlotEphemeris(ax, time, timeFrame):
    # Takes a subplot axis as input

    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    coords = junoEphemeris.values
    coords = np.transpose(coords)

    xCoords = coords[0]
    yCoords = coords[1]
    zCoords = coords[2]

    # Following section adapted from Corentin
    timedelta_hours = np.timedelta64(time[-1] - time[0]).astype("timedelta64[h]") # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds

    major_locator, minor_locator = CalculateTickSpread(timedelta_hours)

    print("Calculated tick spread")

    print(type(time[0]))
    timeTransformed = [np.datetime_as_string(t, unit="D") for t in time]
    # timeTransformed = datetime64_to_datetime(time)
    print(type(timeTransformed[0]))
    print(timeTransformed[0])

    # print(timeTransformed[0].strftime("%H:%M"))

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, xCoords, xCoords, zCoords)))

    print("Setting ticks")
    
    # print(f"Ticks Before: {ax.xaxis.get_majorticklocs()}")

    ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))
    
    return ax


def CalculateTickSpread(timeDelta):
    # Adjusted code taken from Corentin, function takes the timedelta plotted in hours.
    dayLength_sec = 86400 # number of seconds in one day
    dayLength_hrs = 24 # number of hours in one day

    timeDelta = timeDelta.astype("int")

    if (timeDelta < 0.5):
        #Plot every 5 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/6./2.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.)
    elif (timeDelta >= 0.5 and timeDelta < 1.):
        # Plot every 10 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/6.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.)
        
    return (major, minor)

@np.vectorize
def datetime64_to_datetime(time):
    return time.astype(datetime.datetime)


def CartesianPosToPolarPos(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return [r, theta, phi]

