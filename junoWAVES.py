import cdflib
from astropy.time import Time, TimeDelta
import datetime
import numpy as np
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from tqdm import tqdm
import os
from glob import glob
import pandas
from mpl_toolkits import axes_grid1

import junoEphemeris

def PathsFromTimeDifference(t1, t2, pathFormat):
    """ Creates output path names between two times in a specified format 

    Arguments:
    t1, t2 -- (str) Input times between which the paths will be created. Must be in the format "YYYY-MM-DDThh:mm:ss"
    pathFormat -- (str) Path format which the files to be downloaded are in

    Returns:
    A list of the paths following the pathFormat. One path for each day between t1 and t2

    """
    date1, time1 = t1.split("T")
    date2, time2 = t2.split("T")

    year1, month1, day1 = date1.split("-")
    year2, month2, day2 = date2.split("-")

    hours1, minutes1, seconds1 = time1.split(":")

    startDate = datetime.date(int(year1), int(month1), int(day1)) 
    # NOTE: Waves files start from 00:01:09 on each day and end on 00:01:08 the next day meaning to plot from 00:00:00 we need the day before's data.
    if hours1 == "00" and int(minutes1) <= 1 and int(seconds1) < 10:
        startDate = startDate - datetime.timedelta(days=1)

    endDate = datetime.date(int(year2), int(month2), int(day2))

    pathExtensions = []

    if startDate == endDate:
        pathExtensions.append(startDate.strftime(pathFormat))
    
    else:
        for date in DateRange(startDate, endDate):
            pathExtension = date.strftime(pathFormat)
            pathExtensions.append(pathExtension)

    return pathExtensions

def DownloadWavesData(dataPath, downloadPath, timeFrame):
    """ Downloads the waves data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    pathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%m/jno_wav_cdr_lesia_%Y%m%d_v02.cdf")]
    print(f"Downloading Waves files from {downloadPath} to {dataPath}\n")
    for path in tqdm(pathList):
        os.system(f"wget -r -q -nd -nv -np -nH -N -P {dataPath} {path}")


def LoadCdfFiles(dataDirectory, measurements, timeFrame, downloadPath):
    # Inputs are a directory containing the files to be loaded and a list of the measurements to be pulled from the files.

    # NEED TO CHECK TO ONLY LOAD FILES WITHIN THE TIME FRAME, REUSE PATHSFROMTIMEDIFFERENCE?
    """ Loads the downloaded cdf files from the data directory 
    
    Arguments:
    dataDirectory -- (str) Path do directory where data is stored
    measurements -- (list) A list containing strings of the data measurments to pull from the cdf files 

    Returns:
    A list of dictionaries of each file which contains the measurements as keys.

    """


    print(f"Loading CDF files from {dataDirectory}")

    # Check if all filepaths between data are in the folder
    filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}jno_wav_cdr_lesia_%Y%m%d_v02.cdf")
    filePathsNeeded.sort()
    
    filePaths = glob(f"{dataDirectory}*.cdf") # returns a list of downloaded file paths (unsorted)
    filePaths.sort() # Because the date in in the file is in format yyyymmdd it can be sorted numerically.

    filesToBeDownloaded = [file for file in filePathsNeeded if file not in filePaths]

    fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%m/jno_wav_cdr_lesia_%Y%m%d_v02.cdf")

    if len(filesToBeDownloaded) > 0:
        print("Downloading missing data...")
        for path in tqdm(filesToBeDownloaded):
            linkIndex = [i for i, link in enumerate(fileLinks) if path.replace(dataDirectory, '') in link][0]
            os.system(f"wget -r -q -nd -nv -np -nH -N -P {dataDirectory} {downloadPath}{fileLinks[linkIndex]}")

    filePaths = filePathsNeeded


    filesInfoList = []

    print("Loading data...")
    for filePath in tqdm(filePaths):
        file = cdflib.CDF(filePath)

        fileInfo = dict()
        for measurment in measurements:
            measurmentData = file.varget(measurment)
            # measurementUnit = file.varinq(measurment)["Data_Type_Description"]

            fileInfo[measurment] = measurmentData
        
        filesInfoList.append(fileInfo)

    return filesInfoList

def DeleteData(dataDirectory):
    """ Deletes all .cdf files in a directory"""
    os.system(f"rm {dataDirectory}*.cdf")
    
def PlotData(fig, ax, timeFrame, dataDirectory, vmin=False, vmax=False, plotEphemeris=False, ephemerisLabels=False, frequencyBins=1000, yLim=[], colourmap="viridis", colorbarSize="3%", colorbarPad="2%", saveData=False, downloadNewData=True, numFreqBins=126):
    """ Plots the Waves data 

    Arguments:
    fig -- (matplotlib.pyplot figure)
    ax -- (matplotlib.pyplot axis)
    timeFrame -- (list) Contains a start time and end time of data to be plotted in the format "YYYY-MM-DDThh:mm:dd"
    dataDirectory -- (str) Path to directory where data will be stored
    vmin, vmax -- (float) Bounds of the colourbar
    plotEphemeris -- (bool) Should the time axis use ephemeris
    ephemerisLabels -- (bool) Should the x axis labels be ephemeris data 
    downloadNewData -- (bool) Should new data be downloaded and the old data deleted (NOTE: not fully implimented)
    frequencyBins -- (int) Number of bins to interpolate the data into
    yLim -- (list) List containing the bounds of the frequency axis
    colourmap -- (str) What matplotlib cmap to use
    colorbarSize, colorbarPad -- (str) Parameters to determine the size of the colourbar
    saveData, loadData -- (bool) Parameters defining the saving and loading processes instead of downloading data each time.
    numFreqBins -- (int) Number of frequency bins to interpolate the data to. Default 126 for no interpolation

    """
    
    print("Retrieving waves data...")

    if downloadNewData == True:
        DeleteData(dataDirectory)
        DownloadWavesData(dataDirectory, "https://maser.obspm.fr/repository/juno/waves/data/l3a_v02/data/cdf/", timeFrame) # Path should be in format .../data/

    filesWithInfo = LoadCdfFiles(dataDirectory, ["Epoch", "Frequency", "Data"], timeFrame, "https://maser.obspm.fr/repository/juno/waves/data/l3a_v02/data/cdf/")

    # Initialise lists to put the data into
    time = []
    frequency = []
    data = []

    for i, fileInfo in enumerate(filesWithInfo): # enumerate could be computationally expensive here. Perhaps change to a boolean test as it is only a one time use?
        # Next we must contract the lists to the timeframe we have selected.
        if i==0:
            sliceStart = 0
            
            print("Shortening data to match time frame. This may take some time")
            print("Finding start point...")
            for j, t in tqdm(enumerate(fileInfo["Epoch"]), total=len(fileInfo["Epoch"])): # this is quite slow, takes around 30 seconds
                t = Time(t, format="cdf_tt2000")
                t.format="datetime"
                tFrame = Time(timeFrame[0], format = "isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceStart = j
            
            print("Found start point")
            time.extend(fileInfo["Epoch"][sliceStart:])
            data.extend(fileInfo["Data"][sliceStart:])

        elif i==len(filesWithInfo)-1:
            sliceEnd = 0
            
            print("Finding end point...")
            for j, t in tqdm(enumerate(fileInfo["Epoch"]), total=len(fileInfo["Epoch"])): # Similarly very slow around 30 seconds
                t = Time(t, format="cdf_tt2000")
                t.format="datetime"
                tFrame = Time(timeFrame[1], format = "isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceEnd = j
                    
            print("Found end point")
            time.extend(fileInfo["Epoch"][:sliceEnd])            
            data.extend(fileInfo["Data"][:sliceEnd])
        
        else:
            time.extend(fileInfo["Epoch"])
            data.extend(fileInfo["Data"])
        
    # Reformat time into something we can use
    wavesTime = Time(time, format="cdf_tt2000")
    wavesTime.format = "isot"
    
    wavesFrequencies = filesWithInfo[0]["Frequency"]

    wavesData = np.transpose(data)

    # Calibrating by dividing by 377 Ohms
    for frequencyRow in wavesData:
        frequencyRow = frequencyRow / 377

    # Adapted code taken from Corentin
    index_array = range(len(wavesTime))

    # rebin frequencies
    print("Re-binning frequencies")
    rescaledFrequencies = FrequencyRemap(wavesFrequencies, numFreqBins)
    newFlux = np.zeros((len(index_array), len(rescaledFrequencies)), dtype=float)

    # interpolate frequencies
    print("Interpolating Data")
    for i in tqdm(range(len(index_array)), total= len(index_array)):
        newFlux[i,:] = np.interp(x=rescaledFrequencies, xp=wavesFrequencies, fp=wavesData.T[i,:])
    newFlux=newFlux.T
        
    # Find colourbar max and min
    if vmin == False and vmax == False:
        vmin=np.quantile(wavesData,0.05)
        vmax=np.quantile(wavesData,0.95)
    
    print("Drawing Waves image... this may take some time")
    image = ax.pcolormesh(index_array, rescaledFrequencies, newFlux, cmap=colourmap, norm=colors.LogNorm(vmin, vmax))
    ax.set_yscale("log")
    
    if not plotEphemeris:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(index_array, wavesTime)))
        ax.set_xlabel(f"Time from {timeFrame[0]} (s)")
    else:
        # junoEphemeris.PlotEphemeris requires 
        wavesTimeDatetime64 = []
        for time in wavesTime:
            wavesTimeDatetime64.append(np.datetime64(str(time)))

        ax = junoEphemeris.PlotEphemeris(ax, wavesTimeDatetime64, timeFrame, resolutionFactor=60, labels=ephemerisLabels)        
    
    ax.set_ylabel("Frequency (kHz)")
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    divider = axes_grid1.make_axes_locatable(ax)

    cax = divider.append_axes("right", size=colorbarSize, pad=colorbarPad)

    fig.colorbar(image, cax=cax, ax=ax, label="Flux Density (W m$^{-2}$ Hz$^{-1}$)")

    if yLim != []:
        ax.set_ylim(yLim[0], yLim[1])



# Following two functions for interpolating the frequency bins
def FrequencyRemap(originalFrequencyBins, newFrequencyBins):
    return 10**np.linspace(
        start = np.log10(originalFrequencyBins[0]),
        stop = np.log10(originalFrequencyBins[-1]),
        num = newFrequencyBins,
        dtype = float
    )

def format_xlabel(timeIndex, time):
    """ matplotlib ticker custom function formatter to reformat the ephemeris tick labels 
    
    Arguments:
    timeIndex -- (list) An index list of the time coordinates
    time -- (list) The time coordinates 

    """
    timeLength = len(time)
    time = [el.to_datetime() for el in time]
    hoursAndMinutes = pandas.to_datetime(time).strftime('%H:%M')
    dayAndMonthAndYear = pandas.to_datetime(time).strftime('%Y-%m-%d')
    
    def inner_function(index, pos=None):
        #  np.clip will avoid having to check the value (to see if it's outside the array) 
        clipedIndex = np.clip(int(index + 0.5), 0, timeLength - 1)
        return f"{dayAndMonthAndYear[clipedIndex]}\n{hoursAndMinutes[clipedIndex]}"

    return inner_function



def DateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1): # NOTE: adding +1 to include endDate
        yield start_date + datetime.timedelta(n)
