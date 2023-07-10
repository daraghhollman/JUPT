from junoWAVES import PathsFromTimeDifference
from pdsBinaryTools import *
from tqdm import tqdm
import os
from glob import glob

def DownloadJadeData(dataPath, downloadPath, timeFrame):
    """ Downloads the JADE data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

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


def LoadBinaryFiles(dataDirectory, timeFrame, downloadPath):
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
        filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.{fileExtension}")
        filePathsNeeded.sort()
        # print(f"NEEDED: {filePathsNeeded}")
        
        filePaths = glob(f"{dataDirectory}*.{fileExtension}") # returns a list of downloaded file paths (unsorted)
        filePaths.sort() # Because the date in in the file is in format yyyymmdd it can be sorted numerically.
        # print(f"HAVE: {filePaths}")

        filesToBeDownloaded = [file for file in filePathsNeeded if file not in filePaths]

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


def PlotData(fig, ax, timeFrame, dataDirectory, vmin=False, vmax=False, plotEphemeris=False, ephemerisLabels=False, downloadNewData=False):

    if downloadNewData:
        DeleteData(dataDirectory)
        DownloadJadeData(dataDirectory, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", timeFrame)

    LoadBinaryFiles(dataDirectory, timeFrame, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/")
