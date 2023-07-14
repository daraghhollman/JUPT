from junoWAVES import PathsFromTimeDifference
import junoEphemeris

from tqdm import tqdm
from glob import glob
from astropy.time import Time
from datetime import datetime

import os
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import pandas

def DownloadJadeMoments(dataPath, downloadPath, timeFrame):
    """ Downloads the JADE derived moments data using system command wget

    Arguments:
    dataPath -- (str) Path to directory where data will be saved
    downloadPath -- (str) Download link passed to wget
    timeFrame -- (list) The time frame with which to download data

    """

    pathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/JAD_L50_HLS_ELC_MOM_ISO_2D_ELECTRONS_%Y%j_V01.CSV")]
    print(f"Downloading Waves files from {downloadPath} to {dataPath}\n")
    for path in tqdm(pathList):
        fileName = dataDirectory + path.split("/")[-1]
        os.system(f"wget -r -q --show-progress -nd -np -nH -N -P {dataPath} -O fileName {path}")

def DeleteData(dataDirectory):
    """ Deletes all .cdf files in a directory"""
    os.system(f"rm {dataDirectory}*.csv")


def LoadMomentFiles(dataDirectory, timeFrame, downloadPath):
    print(f"Loading JADE moment files from {dataDirectory}")

    filePathsNeeded = PathsFromTimeDifference(timeFrame[0], timeFrame[1], f"{dataDirectory}JAD_L50_HLS_ELC_MOM_ISO_2D_ELECTRONS_%Y%j_V01.CSV")
    filePathsNeeded.sort()

    filePaths = glob(f"{dataDirectory}*.CSV")
    filePaths.sort()

    filesToBeDownloaded = [file for file in filePathsNeeded if file not in filePaths]

    fileLinks = PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%Y%j/JAD_L50_HLS_ELC_MOM_ISO_2D_ELECTRONS_%Y%j_V01.CSV")

    if len(filesToBeDownloaded) > 0:
        print("Downloading missing data...")
        for path in tqdm(filesToBeDownloaded):
            linkIndex = [i for i, link in enumerate(fileLinks) if path.replace(dataDirectory, '') in link][0]
            fileName = dataDirectory + path.split("/")[-1]
            os.system(f"wget -r -q -nd -nv -np -nH -N -P {dataDirectory} -O {fileName} {downloadPath}{fileLinks[linkIndex]}")

    filePaths = filePathsNeeded

    fileInfoList = []

    print("Loading data...")
    for filePath in tqdm(filePaths):
        
        fileInfoList.append(pandas.read_csv(filePath, index_col=False, names=["UTC", "SOURCE_JADE_LEVEL5_DEF_VERSION_INPUT", "INPUT_DATA_SELECTION", "PACKET_MODE", "ACCUMULATION_TIME", "SOURCE_BACKGROUND", "ISSUES", "EV_PER_Q_RANGE", "SC_POS_R", "SC_POS_LAT", "SC_POS_LOCAL_TIME", "SC_POS_SYSIII_ELONG", "DIMENSIONS", "M", "Q", "NUM_LOOK_DIRS", "null", "N_CC", "N_SIGMA_CC", "PRESSURE_PA", "PRESSURE_SIGMA_PA", "TEMP_EV", "TEMP_SIGMA_EV", "QUALITY_FLAG"], header=None))

    return fileInfoList



def PullJadeMoments(dataDirectory, timeFrame, downloadNewData):
    print("Retrieving JADE derived density")

    if downloadNewData == True:
        DeleteData(dataDirectory)
        DownloadJadeMoments(dataDirectory, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J-JAD-5-MOMENTS-V1.0/DATA/", timeFrame)

    filesWithInfo = LoadMomentFiles(dataDirectory, timeFrame, "https://pds-ppi.igpp.ucla.edu/ditdos/download?id=pds://PPI/JNO-J-JAD-5-MOMENTS-V1.0/DATA/")

    return filesWithInfo
    


def PlotDensity(fig, ax, timeFrame, dataDirectory, plotEphemeris=False, ephemerisLabels=False, downloadNewData=True):

    
    filesWithInfo = PullJadeMoments(dataDirectory, timeFrame, downloadNewData)

    totalFile = pandas.concat(filesWithInfo)
    print(len(totalFile))

    times = [datetime.strptime(el, "%Y-%jT%H:%M:%S.%f") for el in totalFile["UTC"]]

    density = totalFile["N_CC"]

    ax.scatter(times, density)
    ax.set_xlabel("Time")
    ax.set_ylabel("Number Density (cm$^{-3}$)")
    # ax.scatter(times[57:90], density[57:90])
