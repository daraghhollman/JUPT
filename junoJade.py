from junoWaves import PathsFromTimeDifference
from pdsBinaryTools import *

def DownloadJadeData(dataPath, downloadPath, timeFrame):
    """ Downloads the JADE data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    binaryPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.DAT")]
    labelPathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/ELECTRONS/JAD_L50_LRS_ELC_ANY_DEF_%Y%j_V01.LBL")]
    print(binaryPathList)

    print(f"Downloading JADE files from {downloadPath} to {dataPath}\n")
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


def PlotData(fig, ax, timeFrame, dataDirectory, vmin=False, vmax=False, plotEphemeris=False, ephemerisLabels=False)
    DownloadJadeData(dataDirectory, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J_SW-JAD-5-CALIBRATED-V1.0/DATA/", timeFrame)

