from junoWAVES import PathsFromTimeDifference
from pdsBinaryTools import *
import junoEphemeris

from tqdm import tqdm
import os
from glob import glob
from astropy.time import Time
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from mpl_toolkits import axes_grid1
from math import floor
from datetime import timedelta
import requests

# DOWNLOADS USING WGET
def DownloadJadeData_wget(dataDirectory, downloadPath, timeFrame, hiRes=False):
    """ Downloads the JADE data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    if hiRes:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.LBL")]
    else:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.LBL")]


    print(f"Downloading {len(labelPathList)} JADE label file(s) from {downloadPath} to {dataDirectory}\n")
    for path in labelPathList:
        fileName = dataDirectory + path.split("/")[-1]
        os.system(f"wget -r -q --show-progress -nd -np -nH -P {dataDirectory} -O {fileName} {path}")

    print(f"Downloading {len(binaryPathList)} JADE binary file(s) from {downloadPath} to {dataDirectory}\n")
    for path in binaryPathList:
        fileName = dataDirectory + path.split("/")[-1]
        os.system(f"wget -r -q --show-progress -nd -np -nH -P {dataDirectory} -O {fileName} {path}")


# DOWNLOADS USING REQUESTS
def DownloadJadeData_requests(dataDirectory, downloadPath, timeFrame, hiRes=False):
    """ Downloads the JADE data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    if hiRes:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.LBL")]
    else:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ION_TOF/JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.LBL")]

    urlList = binaryPathList + labelPathList

    for url in urlList:
        response = requests.get(url, stream=True)

        with open(dataDirectory + url.split("/")[-1], "wb") as f:
            for chunk in tqdm(response.iter_content(chunk_size=1024)):
                if chunk:
                    f.write(chunk)


def LoadBinaryFiles(dataDirectory, timeFrame, downloadPath, hiRes=False):
    # Inputs are a directory containing the files to be loaded and a list of the measurements to be pulled from the files.

    # NEED TO CHECK TO ONLY LOAD FILES WITHIN THE TIME FRAME, REUSE PATHSFROMTIMEDIFFERENCE?
    """ Loads the downloaded cdf files from the data directory 
    
    Arguments:
    dataDirectory -- (str) Path do directory where data is stored

    Returns:
    A list of dictionaries of each file which contains the measurements as keys.

    """

    print(f"Loading JADE files from {dataDirectory}")

    for fileExtension in ["DAT", "LBL"]:
        # Check if all filepaths between data are in the folder
        if hiRes:
            filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.{fileExtension}")
        else:
            filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.{fileExtension}")

        filePathsNeeded.sort()

        filesToBeDownloaded = [file for file in filePathsNeeded if not os.path.exists(file)]

        if hiRes:
            fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"%Y/%Y%j/ION_TOF/JAD_L50_HLS_ION_TOF_DEF_%Y%j_V01.{fileExtension}")
        else:
            fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"%Y/%Y%j/ION_TOF/JAD_L50_LRS_ION_TOF_DEF_%Y%j_V01.{fileExtension}")

        if len(filesToBeDownloaded) > 0:
            print("Downloading missing data...")
            for path in filesToBeDownloaded:
                linkIndex = [i for i, link in enumerate(fileLinks) if path.replace(dataDirectory, '') in link][0]

                url = downloadPath + fileLinks[linkIndex]
                response = requests.get(url, stream=True)

                with open(path, "wb") as f:
                    for chunk in tqdm(response.iter_content(chunk_size=1024)):
                        if chunk:
                            f.write(chunk)
        
        filePaths = filePathsNeeded
        
        if fileExtension == "DAT":
            binaryFilePaths = filePaths

        elif fileExtension == "LBL":
            labelFilePaths = filePaths


    filesInfoList = []

    print("Loading data...")

    for labelFilePath, binaryFilePath in zip(labelFilePaths, binaryFilePaths):
        print(labelFilePath)

        labelInfo, structClass = ReadLabel(labelFilePath)

        binaryDictionary = ReadBinary(binaryFilePath, structClass, labelInfo)

        fileInfo = binaryDictionary
        # for measurment in measurements:
            # measurmentData = file.varget(measurment)
            # measurementUnit = file.varinq(measurment)["Data_Type_Description"]

            # fileInfo[measurment] = measurmentData
        
        filesInfoList.append(fileInfo)

    return filesInfoList


def PlotData(fig, ax, timeFrame, dataDirectory, colourmap="viridis", vmin=False, vmax=False, plotEphemeris=False, ephemerisLabels=False, downloadNewData=False, hiRes=True, colorbarSize="3%", colorbarPad="2%", plotIonEnergy=False, ionTimeOfFlightRange=[]):

    if downloadNewData:
        DownloadJadeData_requests(dataDirectory, "https://search-pdsppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", timeFrame, hiRes=hiRes)

    filesWithInfo = LoadBinaryFiles(dataDirectory, timeFrame, "https://search-pdsppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", hiRes=hiRes)

    # print(filesWithInfo[0]["time of flight"][0])

    startTime = []
    endTime = []
    data = []

    print("Shortening data to match time frame. This may take some time")
    for i, fileInfo in enumerate(filesWithInfo):

        if i == 0 and i == len(filesWithInfo) -1:
            print("Note: using only one file")
            sliceStart = 0

            print("Finding start point")
            for j, t in tqdm(enumerate(fileInfo["startTime"])):
                t = Time(t, format="isot")
                t.format="datetime"

                tFrame = Time(timeFrame[0], format="isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceStart = j+1

            print("Found start point")
            
            sliceEnd = 0

            print("Finding end point")

            for j, t in tqdm(enumerate(fileInfo["startTime"])):

                t = Time(t, format="isot")
                t.format="datetime"

                tFrame = Time(timeFrame[1], format="isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceEnd = j

            print("Found end point")

            if sliceStart == sliceEnd:
                raise ValueError(f"Timeframe start point and end point are closer than timestep in JADE data")

            startTime = fileInfo["startTime"][sliceStart:sliceEnd]
            endTime = fileInfo["endTime"][sliceStart:sliceEnd]
            data = fileInfo["data"][sliceStart:sliceEnd]

        elif i == 0:
            sliceStart = 0
            print("Finding start point")

            for j, t in tqdm(enumerate(fileInfo["startTime"])):
                t = Time(t, format="isot")
                t.format="datetime"

                tFrame = Time(timeFrame[0], format="isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceStart = j+1

            print("Found start point")
            startTime.extend(fileInfo["startTime"][sliceStart:])
            endTime.extend(fileInfo["endTime"][sliceStart:])
            data.extend(fileInfo["data"][sliceStart:])

        elif i == len(filesWithInfo) -1:
            sliceEnd = 0

            print("Finding end point")

            for j, t in tqdm(enumerate(fileInfo["startTime"])):
                
                t = Time(t, format="isot")
                t.format="datetime"

                tFrame = Time(timeFrame[1], format="isot")
                tFrame.format="datetime"

                if t >= tFrame:
                    break
                sliceEnd = j

            print("Found end point")
            startTime.extend(fileInfo["startTime"][:sliceEnd])
            endTime.extend(fileInfo["endTime"][:sliceEnd])
            data.extend(fileInfo["data"][:sliceEnd])

        else:
            startTime.extend(fileInfo["startTime"])
            endTime.extend(fileInfo["endTime"])
            data.extend(fileInfo["data"])

    timeFmt = "%Y-%m-%dT%H:%M:%S.%f"

    dtStart = []
    dtEnd = []
    for t1, t2 in zip(startTime, endTime):
        dtStart.append(datetime.strptime(t1, timeFmt))
        dtEnd.append(datetime.strptime(t2, timeFmt))

    # Sum over the look directions to create energies plot
    data = np.sum(data, axis=2) # Transpose to get to shape (numEnergyBins, Time)
    print(np.shape(data))
    
    # Average over TOF range
    if ionTimeOfFlightRange != []:
        # Indicies of TOF within band specified
        timeOfFlightBandIndices = np.where((filesWithInfo[0]["time of flight"][0] > ionTimeOfFlightRange[0]) & (filesWithInfo[0]["time of flight"][0] < ionTimeOfFlightRange[1]))

        print(timeOfFlightBandIndices)

        # Loop through energy bins
        timeOfFlightToExclude = []
        for i in range(int(np.shape(data)[1])):
            if np.isin(timeOfFlightToExclude, i).any():
                continue
            else:
                timeOfFlightToExclude.append(i)


        data = np.delete(data, timeOfFlightToExclude, axis=2)
        ionData = np.transpose(np.sum(data, axis=2)) / np.shape(data)[1]

    else:
        ionData = np.transpose(np.sum(data, axis=2)) / np.shape(data)[1]


    print("Drawing JADE image...")

    for fileInfo in filesWithInfo:
        if not (fileInfo["energy scale"] == filesWithInfo[0]["energy scale"]).all():
            raise RuntimeError("Energy channel values inconsistant across list of files")
        # if np.max(fileInfo["pitch angle scale"]) > 180:
                        # raise RuntimeError(f"Pitch Angle missing data (value: {np.max(fileInfo['pitch angle scale'])})for this timestep")


    timeFrame_dt = [datetime.strptime(el, "%Y-%m-%dT%H:%M:%S") for el in timeFrame]

    # Accounting for data gaps for electron energies:
    newGridHeight = int(len(filesWithInfo[0]["energy scale"]))
    dt = (dtEnd[0] - dtStart[0]).total_seconds()
    newGridWidth = int((timeFrame_dt[1] - timeFrame_dt[0]).total_seconds() / dt + 1)

    newDataArray = np.empty((newGridHeight -1, newGridWidth -1)); newDataArray.fill(np.nan)   

    dataIndex = ([floor((t - timeFrame_dt[0]).total_seconds() / dt) for t in dtStart])


    newDataArray[:, dataIndex] = ionData[:-1, :]
    

    index_array = range(newGridWidth)
    tickTime = []
    for i, timeIndex in enumerate(index_array):
        tickTime.append((timeFrame_dt[0] + timedelta(seconds=dt*i)).strftime("%Y-%m-%dT%H:%M:%S.%f"))

    if plotIonEnergy:
        image = ax.pcolormesh(index_array, [el for el in filesWithInfo[0]["energy scale"]], newDataArray, cmap=colourmap, norm=colors.LogNorm())
        ax.set_ylabel("Ion Energy (eV)")
        ax.set_yscale("log")


    if not plotEphemeris:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_xlabel(index_array, tickTime)))
        ax.set_xlabel(f"Time from {timeFrame[0]} (s)")

    else:
        timeDatetime64 = []
        for t in tickTime:
            timeDatetime64.append(np.datetime64(str(t)))

        print(f"plotting ephemeris for {newGridWidth} points")
        if hiRes:
            ax = junoEphemeris.PlotEphemeris(ax, timeDatetime64, timeFrame, labels=ephemerisLabels, isJade=True)
        else:
            ax = junoEphemeris.PlotEphemeris(ax, timeDatetime64, timeFrame, labels=ephemerisLabels, isJade=True)


    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    divider = axes_grid1.make_axes_locatable(ax)

    cax = divider.append_axes("right", size=colorbarSize, pad=colorbarPad)

    if filesWithInfo[0]["data units"] == (3,):
        if plotIonEnergy:
            fig.colorbar(image, cax=cax, ax=ax, label="Diff. Energy Flux\n(m$^{-2}$ sr$^{-1}$ s$^{-1}$)")

    else:
        raise RuntimeError("Unknown data units")


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
