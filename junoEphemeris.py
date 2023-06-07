import speasy as spz
import numpy as np
import matplotlib.ticker as ticker

# Editted code from corentin
def format_xlabel(time, x, y, z):
    def inner_function(index, pos=None):
        int_index = int(index)

        if int_index >= len(time):
            return ""
        print(f"{time[int_index]}\n{x[int_index]}\n{y[int_index]}\n{z[int_index]}")
        return f"{time[int_index]}\n{x[int_index]}\n{y[int_index]}\n{z[int_index]}"

def PlotEphemeris(ax, time, timeFrame):
    # Takes a subplot axis as input

    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    # time = junoEphemeris.time

    coords = junoEphemeris.values
    coords = np.transpose(coords)

    xCoords = coords[0]
    yCoords = coords[1]
    zCoords = coords[2]

    print(f"X COORD: {np.dtype(xCoords[0])}")

    # Following section adapted from Corentin
    timedelta_hours = np.timedelta64(time[-1] - time[0]).astype("timedelta64[h]") # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds

    major_locator, minor_locator = CalculateTickSpread(timedelta_hours)

    print("Calculated tick spread")

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(time, xCoords, xCoords, zCoords)))

    print("Setting ticks")
    
    # print(f"Ticks Before: {ax.xaxis.get_majorticklocs()}")

    ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))
    
    # ax.xaxis.set_major_locator(ticker.AutoLocator())
    
    print(f"Ticks After: {ax.xaxis.get_majorticklocs()}")

    return ax


def CalculateTickSpread(timeDelta):
    # Adjusted code taken from Corentin, function takes the timedelta plotted in hours.
    dayLength_sec = 86400 # number of seconds in one day
    dayLength_hrs = 24 # number of hours in one day

    print(f"TIMEDELTA: {timeDelta}")

    timeDelta = timeDelta.astype("int")

    print(timeDelta)

    if (timeDelta < 0.5):
        #Plot every 5 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/6./2.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.)
    elif (timeDelta >= 0.5 and timeDelta < 1.):
        # Plot every 10 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/6.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.)
        
    print(len(major))
    print(len(minor))

    # major = [el / dayLength_sec for el in major]

    return (major, minor)


def CartesianPosToPolarPos(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return [r, theta, phi]


"""
ticksAmmount = 5
timeInterval = len(time)/ticksAmmount

ticksPos = [int(timeInterval*i) for i in range(ticksAmmount)] 

ticksLabels = [str(time[int(timeInterval*i)])[0:10]+f"\nx\ny\nz" for i in range(ticksAmmount)]
"""
