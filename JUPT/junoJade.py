from junoWAVES import PathsFromTimeDifference
from pdsBinaryTools import *
import junoEphemeris

from tqdm import tqdm
import os
from glob import glob
from astropy.time import Time, TimeDelta
import matplotlib.colors as colors
import matplotlib.ticker as ticker
from mpl_toolkits import axes_grid1
from math import floor
from datetime import timedelta

def DownloadJadeData(dataPath, downloadPath, timeFrame, hiRes=False):
    """ Downloads the JADE data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    if hiRes:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_HRS_ELC_TWO_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_HRS_ELC_TWO_DEF_%Y%j_V01.LBL")]
    else:
        binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.DAT")]
        labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.LBL")]


    print(f"Downloading {len(labelPathList)} JADE label file(s) from {downloadPath} to {dataPath}\n")
    for path in labelPathList:
        fileName = dataPath + path.split("/")[-1]
        os.system(f"wget -r -q --show-progress -nd -np -nH -P {dataPath} -O {fileName} {path}")

    print(f"Downloading {len(binaryPathList)} JADE binary file(s) from {downloadPath} to {dataPath}\n")
    for path in binaryPathList:
        fileName = dataPath + path.split("/")[-1]
        os.system(f"wget -r -q --show-progress -nd -np -nH -P {dataPath} -O {fileName} {path}")


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
            filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_HRS_ELC_TWO_DEF_%Y%j_V01.{fileExtension}")
        else:
            filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.{fileExtension}")

        filePathsNeeded.sort()
        # print(f"NEEDED: {filePathsNeeded}")
        
        filePaths = glob(f"{dataDirectory}*.{fileExtension}") # returns a list of downloaded file paths (unsorted)
        filePaths.sort() # Because the date in in the file is in format yyyymmdd it can be sorted numerically.
        # print(f"HAVE: {filePaths}")

        filesToBeDownloaded = [file for file in filePathsNeeded if file not in filePaths]

        if hiRes:
            fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"%Y/%Y%j/ELECTRONS/JAD_L50_HRS_ELC_TWO_DEF_%Y%j_V01.{fileExtension}")
        else:
            fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"%Y/%Y%j/ELECTRONS/JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.{fileExtension}")

        if len(filesToBeDownloaded) > 0:
            print("Downloading missing data...")
            for path in filesToBeDownloaded:
                linkIndex = [i for i, link in enumerate(fileLinks) if path.replace(dataDirectory, '') in link][0]
                fileName = dataDirectory + path.split("/")[-1]
                os.system(f"wget -r -q --show-progress -nd -np -nH -P {dataDirectory} -O {fileName} {downloadPath}{fileLinks[linkIndex]}")
        
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


def DeleteData(dataDirectory):
    """ Deletes all .cdf files in a directory"""
    os.system(f"rm {dataDirectory}*.DAT")
    os.system(f"rm {dataDirectory}*.LBL")


def PlotData(fig, ax, timeFrame, dataDirectory, colourmap="viridis", vmin=False, vmax=False, plotEphemeris=False, ephemerisLabels=False, downloadNewData=False, hiRes=True, colorbarSize="3%", colorbarPad="2%", plotElectronEnergy=True, plotPitchAngle=False, reBin=True, pitchBinStep=10, pitchAngleEnergyRange=[]):

    if downloadNewData:
        DeleteData(dataDirectory)
        DownloadJadeData(dataDirectory, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", timeFrame, hiRes=hiRes)

    filesWithInfo = LoadBinaryFiles(dataDirectory, timeFrame, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", hiRes=hiRes)

    startTime = []
    endTime = []
    energy = []
    data = []
    pitchAngles = []

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
            pitchAngles = fileInfo["pitch angle scale"][sliceStart:sliceEnd]

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
            pitchAngles.extend(fileInfo["pitch angle scale"][sliceStart:])

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
            pitchAngles.extend(fileInfo["pitch angle scale"][:sliceEnd])

        else:
            startTime.extend(fileInfo["startTime"])
            endTime.extend(fileInfo["endTime"])
            data.extend(fileInfo["data"])
            pitchAngles.extend(fileInfo["pitch angle scale"])

    timeFmt = "%Y-%m-%dT%H:%M:%S.%f"

    dtStart = []
    dtEnd = []
    for t1, t2 in zip(startTime, endTime):
        dtStart.append(datetime.strptime(t1, timeFmt))
        dtEnd.append(datetime.strptime(t2, timeFmt))

    # Sum over the look directions to create energies plot
    sumOverLookAngles = np.transpose(np.sum(data, axis=2)) # Transpose to get to shape (numEnergyBins, Time)


    # Average over energies for pitch angle plot
    if pitchAngleEnergyRange != []:
        # Indicies of energy scale where energy is within band specified
        energyBandIndices = np.where((filesWithInfo[0]["energy scale"][:,0] > pitchAngleEnergyRange[0]) & (filesWithInfo[0]["energy scale"][:,0] < pitchAngleEnergyRange[1]))

        # Loop through energy bins
        energiesToExclude = []
        for i in range(int(np.shape(data)[1])):
            if np.isin(energyBandIndices, i).any():
                continue
            else:
                energiesToExclude.append(i)


        data = np.delete(data, energiesToExclude, axis=1)
        lookAnglesData = np.transpose(np.sum(data, axis=1)) / np.shape(data)[1]

    else:
        lookAnglesData = np.transpose(np.sum(data, axis=1)) / np.shape(data)[1]

    pitchAngles = np.array(pitchAngles)

    # index_array = range(len(startTime))


    print("Drawing JADE image...")

    for fileInfo in filesWithInfo:
        if not (fileInfo["energy scale"][:,0] == filesWithInfo[0]["energy scale"][:,0]).all():
            raise RuntimeError("Energy channel values inconsistant across list of files")
        # if np.max(fileInfo["pitch angle scale"]) > 180:
                        # raise RuntimeError(f"Pitch Angle missing data (value: {np.max(fileInfo['pitch angle scale'])})for this timestep")


    timeFrame_dt = [datetime.strptime(el, "%Y-%m-%dT%H:%M:%S") for el in timeFrame]

    # Accounting for data gaps for electron energies:
    newGridHeight = int(len(filesWithInfo[0]["energy scale"][:,0]))
    dt = (dtEnd[0] - dtStart[0]).total_seconds()
    newGridWidth = int((timeFrame_dt[1] - timeFrame_dt[0]).total_seconds() / dt + 1)

    newDataArray = np.empty((newGridHeight -1, newGridWidth -1)); newDataArray.fill(np.nan)   
    print(np.shape(newDataArray))
    print(np.shape(sumOverLookAngles))

    dataIndex = ([floor((t - timeFrame_dt[0]).total_seconds() / dt) for t in dtStart])

    print(np.shape(dataIndex))

    newDataArray[:, dataIndex] = sumOverLookAngles[:-1, :]
    

    index_array = range(newGridWidth)
    tickTime = []
    for i, timeIndex in enumerate(index_array):
        tickTime.append((timeFrame_dt[0] + timedelta(seconds=dt*i)).strftime("%Y-%m-%dT%H:%M:%S.%f"))

    if plotElectronEnergy:
        image = ax.pcolormesh(index_array, [el for el in filesWithInfo[0]["energy scale"][:,0]], newDataArray, cmap=colourmap, norm=colors.LogNorm())
        ax.set_ylabel("Electron Energy (eV)")
        ax.set_yscale("log")


    if plotPitchAngle:

        invalidPitchAngleIndices = []
        for i, timestep in enumerate(pitchAngles):
            if np.max(timestep) > 180:
                invalidPitchAngleIndices.append(i)

        np.put(pitchAngles, invalidPitchAngleIndices, np.nan)
        np.put(lookAnglesData, invalidPitchAngleIndices, np.nan)


        pitchAngleValues = np.transpose([np.sum(i, axis=0) / len(filesWithInfo[0]["energy scale"][:,0]) for i in pitchAngles])

        timeArray = np.tile(index_array, (len(pitchAngleValues[:, :-1]), 1))
        

        # Accounting for data gaps for electron PAD:
        newGridHeight = int(len(np.arange(0, 180+pitchBinStep, pitchBinStep)))
        dt = (dtEnd[0] - dtStart[0]).total_seconds()
        newGridWidth = int((timeFrame_dt[1] - timeFrame_dt[0]).total_seconds() / dt +1)

        newDataArray = np.empty((newGridHeight -1, newGridWidth -1)); newDataArray.fill(np.nan)   
        print(np.shape(newDataArray))
        print(np.shape(pitchAngleValues))

        dataIndex = ([floor((t - timeFrame_dt[0]).total_seconds() / dt) for t in dtStart])

        if reBin:
            reBinnedData = np.zeros((int(180 / pitchBinStep), len(pitchAngleValues[0])))
            for t in range(len(pitchAngleValues[0])):
                pitchBins = np.arange(0, 180+pitchBinStep, pitchBinStep) # the bottom and left edges of the mesh ranging from 0 to 180+step
                
                for i in range(len(pitchBins)-1):
                    # print(f"Greater than {pitchBins[i]}, less than {pitchBins[i+1]}")
                    binIndices = np.where((pitchAngleValues[:,t] > pitchBins[i]) & (pitchAngleValues[:,t] < pitchBins[i+1]))
                    reBinnedData[i][t] = np.mean(lookAnglesData[:,t][binIndices])

            # reBinnedData = reBinnedData[:,:-1]
            print(np.shape(reBinnedData))
            print(np.shape(newDataArray))
            newDataArray[:, dataIndex] =reBinnedData[:, :]

            image = ax.pcolormesh(index_array, pitchBins, newDataArray, cmap=colourmap, norm=colors.LogNorm(), shading="flat")
        else:
            print(np.shape(timeArray))
            print(np.shape(pitchAngleValues))
            print(np.shape(lookAnglesData))
            image = ax.pcolormesh(timeArray, pitchAngleValues, lookAnglesData, cmap=colourmap, norm=colors.LogNorm())

        if pitchAngleEnergyRange != []:
            ax.set_ylabel(f"Pitch Angle (deg)\nfrom:{pitchAngleEnergyRange[0]/1000} - {pitchAngleEnergyRange[1]/1000} keV")
        else:
            ax.set_ylabel(f"Pitch Angle (deg)")
        ax.set_yscale("linear")


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
        if plotElectronEnergy:
            fig.colorbar(image, cax=cax, ax=ax, label="Diff. Energy Flux\n(m$^{-2}$ sr$^{-1}$ s$^{-1}$)")
        elif plotPitchAngle:
            fig.colorbar(image, cax=cax, ax=ax, label=f"Mean Diff. Energy Flux \n(m$^{-2}$ sr$^{-1}$ s$^{-1}$)")


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
