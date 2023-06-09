import speasy as spz
import numpy as np
import matplotlib.ticker as ticker
import datetime
import pandas

# Editted code from corentin
def format_xlabel(time, x, y, z):
    timeLength = len(time)
    hoursAndMinutes = pandas.to_datetime(time).strftime('%H:%M')
    dayAndMonth = pandas.to_datetime(time).strftime('%d/%m')
    
    def inner_function(index, pos=None):
        #  np.clip will avoid having to check the value (to see if it's outside the array) 
        clipedIndex = np.clip(int(index + 0.5), 0, timeLength - 1)
        return f"{dayAndMonth[clipedIndex]}\n{hoursAndMinutes[clipedIndex]}\n{x[clipedIndex]:5.2f}\n{y[clipedIndex]:3.2f}\n{z[clipedIndex]:3.2f}"
    
    return inner_function

def PlotEphemeris(ax, dataTime, timeFrame):
    # Takes a subplot axis as input
    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    ephemerisTime = junoEphemeris.time
    coords = np.transpose(junoEphemeris.values)
    
    xCoords = coords[0]
    yCoords = coords[1]
    zCoords = coords[2]

    # Ephemerides must be interpolated on the data time table
    ephemerisTimeTransformed = datetime64_to_datetime(ephemerisTime)

    dataTimeTransformed = datetime64_to_datetime(dataTime)

    dataTime_seconds = [elt.timestamp() for elt in dataTimeTransformed]
    ephemerisTime_seconds = [elt.timestamp() for elt in ephemerisTimeTransformed]
    xCoords=np.interp(dataTime_seconds,ephemerisTime_seconds,xCoords)
    yCoords=np.interp(dataTime_seconds,ephemerisTime_seconds,yCoords) 
    zCoords=np.interp(dataTime_seconds,ephemerisTime_seconds,zCoords)

    print("Setting ticks")

    # to be feed into the format_xlabel function, time array needs to be a datetime.datetime object
    # from numpy.datetime64 --> datetime.datetime, one first needs to transform numpy.datetime64 --> numpy.array(dtype='str'):
    # then to datetime
    # timeTransformed = datestring_to_datetime(time_str)
    timeTransformed = datetime64_to_datetime(dataTime)
   
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, xCoords, xCoords, zCoords)))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, xCoords, yCoords, zCoords)))
 
    
    # Following section adapted from Corentin
    timedelta_hours = np.timedelta64(ephemerisTime[-1] - ephemerisTime[0]).astype("timedelta64[h]") # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds
    # major_locator, minor_locator = CalculateTickSpread(timedelta_hours)

    # print(f"Ticks Before: {ax.xaxis.get_majorticklocs()}")

    # ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    # ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))

    print("Calculated tick spread")
    
    return ax

def datetime64_to_datetime(time):
    timeStr = [np.datetime_as_string(t, unit="s") for t in time]
    return datestring_to_datetime(timeStr)

def CoordLengthsToMatchTime(time, coords):
    newCoordsList = []
    for direction in coords:
        newCoordinates = []

        for i in range(1, len(time)+1):
            newCoordinates.append(direction[int(len(direction)/len(time) * i)-1])

        newCoordsList.append(newCoordinates)
    return newCoordsList


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
    elif (timeDelta >= 1. and timeDelta < 2.):
        # Plot every 15 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/4.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.) 
    elif (timeDelta >= 2. and timeDelta < 3.):
        # Plot every 20 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/3.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.) 
    elif (timeDelta >= 3. and timeDelta < 4.):
        # Plot every 30 mins
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/2.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/60.) 
    elif (timeDelta >= 4. and timeDelta < 8.):
        # Plot every hour
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/1.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/4.) 
    elif (timeDelta >= 8. and timeDelta < 16.):
        # Plot every 2 hours
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/2.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs) 
    elif (timeDelta >= 16. and timeDelta < 24.):
        # Plot every 3 hours
        major = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs/3.)
        minor = np.arange(0, dayLength_sec, dayLength_sec/dayLength_hrs) 
    elif (timeDelta >= 24. and timeDelta < 48.):
        # Plot every 6 hours
        major = np.arange(0, dayLength_sec*2, dayLength_sec/dayLength_hrs/6.)
        minor = np.arange(0, dayLength_sec*2, dayLength_sec/dayLength_hrs) 
    elif (timeDelta >= 2*24. and timeDelta < 5*24.):
        # Plot every 12 hours
        major = np.arange(0, dayLength_sec*(timeDelta/24 + 1), dayLength_sec/2.)
        minor = np.arange(0, dayLength_sec*(timeDelta/24 + 1), dayLength_sec/8.) 
    elif (timeDelta >= 5*24.):
        # Plot every day
        major = np.arange(0, dayLength_sec*(timeDelta/24 + 1), dayLength_sec)
        minor = np.arange(0, dayLength_sec*(timeDelta/24 + 1), dayLength_sec/2.) 
  
    return (major, minor)

@np.vectorize
def datestring_to_datetime(time):
    #return datetime.datetime.strptime(np.datetime_as_string(time,unit="s"),"%Y-%m-%dT%H:%M:%S")
    return datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")


def CartesianPosToPolarPos(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return [r, theta, phi]


