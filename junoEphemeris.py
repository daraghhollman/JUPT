import speasy as spz
import numpy as np
import matplotlib.ticker as ticker
import datetime
import pandas

# Editted code from corentin
def format_xlabel(time, r, lon, lat, mlat):
    timeLength = len(time)
    hoursAndMinutes = pandas.to_datetime(time).strftime('%H:%M')
    dayAndMonthAndYear = pandas.to_datetime(time).strftime('%Y-%m-%d')
    
    def inner_function(index, pos=None):
        #  np.clip will avoid having to check the value (to see if it's outside the array) 
        clipedIndex = np.clip(int(index + 0.5), 0, timeLength - 1)
        return f"{dayAndMonthAndYear[clipedIndex]}\n{hoursAndMinutes[clipedIndex]}\n{r[clipedIndex]:5.2f}\n{lon[clipedIndex]:5.2f}\n{lat[clipedIndex]:5.2f}\n{mlat[clipedIndex]:5.2f}"
    
    return inner_function


def PlotEphemeris(ax, dataTime, timeFrame):
    # Takes a subplot axis as input
    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    distanceValues = PullEphemerisData("juno_jup_r", dataTime, timeFrame)
    longitudeValues = PullEphemerisData("juno_jup_lon", dataTime, timeFrame)
    latitudeValues = PullEphemerisData("juno_jup_lat", dataTime, timeFrame)
    mLatitudeValues = PullEphemerisData("juno_jup_mlat", dataTime, timeFrame)

    ephemerisTime = junoEphemeris.time

    # to be feed into the format_xlabel function, time array needs to be a datetime.datetime object
    # from numpy.datetime64 --> datetime.datetime, one first needs to transform numpy.datetime64 --> numpy.array(dtype='str'):
    # then to datetime
    timeTransformed = datetime64_to_datetime(dataTime)
   
    print("Setting ticks")

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, distanceValues, longitudeValues, latitudeValues, mLatitudeValues)))
 
    # Following section adapted from Corentin
    timedelta_hours = np.timedelta64(ephemerisTime[-1] - ephemerisTime[0]).astype("timedelta64[h]") # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds
    print(f"TIMEDELTA; Type: {type(timedelta_hours)}, Value: {timedelta_hours}")

    major_locator, minor_locator = CalculateTickSpread(timedelta_hours)
    major_locator = np.multiply(major_locator, 60)
    minor_locator = np.multiply(minor_locator, 60)
    # ax.set_xlim((0, major_locator[-1]))

    ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))

    print("Calculated tick spread")
   
    # Set ephemeris labels
    labelFontsize = 10
    labelsPos = [-40, -37]
    posSpacer = 1

    ax.annotate('R',xy=(0,0), xycoords='axes fraction', xytext=(labelsPos[0], labelsPos[1]-0*labelFontsize), textcoords='offset points', horizontalalignment='right', verticalalignment='center',fontsize=labelFontsize)
    ax.annotate('Lon',xy=(0,0), xycoords='axes fraction', xytext=(labelsPos[0], labelsPos[1]-1*labelFontsize - posSpacer), textcoords='offset points', horizontalalignment='right', verticalalignment='center',fontsize=labelFontsize)
    ax.annotate('Lat',xy=(0,0), xycoords='axes fraction', xytext=(labelsPos[0], labelsPos[1]-2*labelFontsize - 2*posSpacer), textcoords='offset points', horizontalalignment='right', verticalalignment='center',fontsize=labelFontsize)
    ax.annotate('M Lat',xy=(0,0), xycoords='axes fraction', xytext=(labelsPos[0], labelsPos[1]-3*labelFontsize - 3*posSpacer), textcoords='offset points', horizontalalignment='right', verticalalignment='center',fontsize=labelFontsize)

    return ax


def PullEphemerisData(amdaId, inputTime, timeFrame):
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
    dayLength_mins = 1400 # number of minutes in one day

    timeDelta = timeDelta.astype("int")

    if (timeDelta < 0.5):
        #Plot every 5 mins
        major = np.arange(0, dayLength_mins, 5)
        minor = np.arange(0, dayLength_mins, 1)
    elif (timeDelta >= 0.5 and timeDelta < 1.):
        # Plot every 10 mins
        major = np.arange(0, dayLength_mins, 10)
        minor = np.arange(0, dayLength_mins, 2)
    elif (timeDelta >= 1. and timeDelta < 2.):
        # Plot every 15 mins
        major = np.arange(0, dayLength_mins, 15)
        minor = np.arange(0, dayLength_mins, 5) 
    elif (timeDelta >= 2. and timeDelta < 3.):
        # Plot every 20 mins
        major = np.arange(0, dayLength_mins, 20)
        minor = np.arange(0, dayLength_mins, 5) 
    elif (timeDelta >= 3. and timeDelta < 4.):
        # Plot every 30 mins
        major = np.arange(0, dayLength_mins, 30)
        minor = np.arange(0, dayLength_mins, 10) 
    elif (timeDelta >= 4. and timeDelta < 8.):
        # Plot every hour
        major = np.arange(0, dayLength_mins, 60)
        minor = np.arange(0, dayLength_mins, 20) 
    elif (timeDelta >= 8. and timeDelta < 16.):
        # Plot every 2 hours
        major = np.arange(0, dayLength_mins, 60*2)
        minor = np.arange(0, dayLength_mins, 30) 
    elif (timeDelta >= 16. and timeDelta < 24.):
        # Plot every 3 hours
        major = np.arange(0, dayLength_mins, 60*3)
        minor = np.arange(0, dayLength_mins, 60) 
    elif (timeDelta >= 24. and timeDelta < 48.):
        # Plot every 6 hours
        major = np.arange(0, dayLength_mins*2, 60*6)
        minor = np.arange(0, dayLength_mins*2, 60*2) 
    elif (timeDelta >= 2*24. and timeDelta < 5*24.):
        # Plot every 12 hours
        major = np.arange(0, dayLength_mins*(timeDelta/24 + 1), 60*12)
        minor = np.arange(0, dayLength_mins*(timeDelta/24 + 1), 60*3) 
    elif (timeDelta >= 5*24.):
        # Plot every day
        major = np.arange(0, dayLength_mins*(timeDelta/24 + 1), 60*24)
        minor = np.arange(0, dayLength_mins*(timeDelta/24 + 1), 60*8) 

    print(f"Major ticks every: {(major[1] - major[0])/60} hours, Minor ticks every: {(minor[1] - minor[0])/60} hours")
    # print(f"Major: {major}")
    # print(f"Minor: {minor}")
  
    return (major, minor)

@np.vectorize
def datestring_to_datetime(time):
    #return datetime.datetime.strptime(np.datetime_as_string(time,unit="s"),"%Y-%m-%dT%H:%M:%S")
    return datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")




