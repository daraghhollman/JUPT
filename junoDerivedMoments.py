from junoWAVES import PathsFromTimeDifference
import junoEphemeris

from tqdm import tqdm
from glob import glob
from astropy.time import Time
from datetime import datetime
from mpl_toolkits import axes_grid1

import os
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import pandas
import numpy as np

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
        
        fileInfoList.append(pandas.read_csv(filePath, names=["UTC", "SOURCE_JADE_LEVEL5_DEF_VERSION_INPUT", "INPUT_DATA_SELECTION", "PACKET_MODE", "ACCUMULATION_TIME", "SOURCE_BACKGROUND", "ISSUES", "EV_PER_Q_RANGE", "SC_POS_R", "SC_POS_LAT", "SC_POS_LOCAL_TIME", "SC_POS_SYSIII_ELONG", "DIMENSIONS", "M", "Q", "NUM_LOOK_DIRS", "null", "N_CC", "N_SIGMA_CC", "PRESSURE_PA", "PRESSURE_SIGMA_PA", "TEMP_EV", "TEMP_SIGMA_EV", "QUALITY_FLAG"], header=None))

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

    totalFile = pandas.concat(filesWithInfo, ignore_index=True)

    print("Shortening data to match time frame")
    foundStart=False
    foundEnd=False

    timeFrameStart = datetime.strptime(timeFrame[0], "%Y-%m-%dT%H:%M:%S")
    timeFrameEnd = datetime.strptime(timeFrame[1], "%Y-%m-%dT%H:%M:%S")

    for index, row in tqdm(totalFile.iterrows(), total=len(totalFile)):
        time = datetime.strptime(row["UTC"], "%Y-%jT%H:%M:%S.%f")
        
        if time >= timeFrameStart and foundStart == False:
            sliceStart=index
            foundStart=True

        if time >= timeFrameEnd and foundEnd == False:
            sliceEnd = index
            foundEnd = True

    slicedFile = totalFile.truncate(sliceStart, sliceEnd)


    times = [datetime.strptime(el, "%Y-%jT%H:%M:%S.%f") for el in slicedFile["UTC"]]

    density = slicedFile["N_CC"]

    ax.plot(times, density, linestyle="dotted")
    ax.scatter(times, density, marker=".")

    ax.set_ylabel("Number Density (cm$^{-3}$)")

    if not plotEphemeris:
        ax.set_xlabel("UT")

    else:
        timesDatetime64 = []
        for t in times:
            timesDatetime64.append(np.datetime64(str(t)))

        ax = junoEphemeris.PlotEphemeris(ax, timesDatetime64, timeFrame, labels=ephemerisLabels)

    ax.margins(x=0)

    # Srink axis
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    divider = axes_grid1.make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad="2%")
    cax.axis("off")

    return ax
