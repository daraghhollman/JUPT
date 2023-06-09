#−∗− coding : utf−8 −∗−

import speasy as spz
import numpy as np
import matplotlib.ticker as ticker
import datetime
import pandas

# Editted code from corentin
def format_xlabel(time, x, y, z):
    time_length = len(time)
    str_time = pandas.to_datetime(time).strftime('%H:%M')
    def inner_function(index, pos=None):
        #  np.clip will avoid having to check the value (to see if it's outside the array) 
        cliped_index = np.clip(int(index + 0.5), 0, time_length - 1)
        return f"{str_time[cliped_index]}\n{x[cliped_index]:5.2f}\n{y[cliped_index]:3.2f}\n{z[cliped_index]:3.2f}"
    return inner_function

def PlotEphemeris(ax, time, timeFrame):
    # Takes a subplot axis as input
    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    time_ephem = junoEphemeris.time
    coords = junoEphemeris.values
    coords = np.transpose(coords)
    
    xCoords = coords[0]
    yCoords = coords[1]
    zCoords = coords[2]

    # Ephemerides must be interpolated on the data time table
    time_ephem_str = [np.datetime_as_string(t, unit="s") for t in time_ephem]
    time_ephem_Transformed = datestring_to_datetime(time_ephem_str)

    time_data_str = [np.datetime_as_string(t, unit="s") for t in time]
    time_data_Transformed = datestring_to_datetime(time_data_str)

    time_data_sec = [elt.timestamp() for elt in time_data_Transformed]
    time_ephem_sec = [elt.timestamp() for elt in time_ephem_Transformed]
    xCoords=np.interp(time_data_sec,time_ephem_sec,xCoords)
    yCoords=np.interp(time_data_sec,time_ephem_sec,yCoords) 
    zCoords=np.interp(time_data_sec,time_ephem_sec,zCoords)

    print("Setting ticks")

    # to be feed into the format_xlabel function, time array needs to be a datetime.datetime object
    # from numpy.datetime64 --> datetime.datetime, one first needs to transform numpy.datetime64 --> numpy.array(dtype='str'):
    time_str = [np.datetime_as_string(t, unit="s") for t in time]
    # then to datetime
    timeTransformed = datestring_to_datetime(time_str)
   
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, xCoords, xCoords, zCoords)))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(timeTransformed, xCoords, yCoords, zCoords)))
   
    
    # Following section adapted from Corentin
    timedelta_hours = np.timedelta64(time_ephem[-1] - time_ephem[0]).astype("timedelta64[h]") # time[i] is of format datetime64[ns] and hence the unit of timedelta is in nanoseconds
    #major_locator, minor_locator = CalculateTickSpread(timedelta_hours)

    # print(f"Ticks Before: {ax.xaxis.get_majorticklocs()}")

    #ax.xaxis.set_major_locator(ticker.FixedLocator(major_locator))
    #ax.xaxis.set_minor_locator(ticker.FixedLocator(minor_locator))

    print("Calculated tick spread")



    
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
def datestring_to_datetime(time):
    #return datetime.datetime.strptime(np.datetime_as_string(time,unit="s"),"%Y-%m-%dT%H:%M:%S")
    return datetime.datetime.strptime(time,"%Y-%m-%dT%H:%M:%S")


def CartesianPosToPolarPos(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return [r, theta, phi]


