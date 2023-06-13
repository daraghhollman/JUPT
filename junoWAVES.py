import cdflib
from astropy.time import Time, TimeDelta
import datetime
import numpy as np
import matplotlib.colors as colors
from tqdm import tqdm
import os

def PathsFromTimeDifference(t1, t2, pathFormat):
    # Inputs are time in format "2022-06-01T00:00:00"
    # Outputs a list of paths to the data containing the time
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

    pathList = [f"{downloadPath}{extension}" for extension in PathsFromTimeDifference(timeFrame[0], timeFrame[1], "%Y/%m/jno_wav_cdr_lesia_%Y%m%d_v02.cdf")]
    for path in tqdm(pathList):
        print(f"Downloading from: {path}")
        os.system(f"wget -r -nd -nv -np -nH -N -P {dataPath} {path}")



def PlotData(fig, ax, timeFrame, vmin=False, vmax=False, plotEphemeris=False):
    # Takes one of the subplot axes as input
    # NOTE: Functionality to automatically download the data would be useful
    
    print("Retrieving waves data...")

    DownloadWavesData(r"/home/daraghhollman/Main/data/", "https://maser.obspm.fr/repository/juno/waves/data/l3a_v02/data/cdf/", timeFrame) # Path should be in format .../data/

    wavesPath = "/home/daraghhollman/Main/data/jno_wav_cdr_lesia_20220101_v02.cdf"

    wavesCDF = cdflib.CDF(wavesPath)
    
    epoch = wavesCDF.varget("Epoch")
    epochUnit = wavesCDF.varinq("Epoch")["Data_Type_Description"] # Time since 2000-01-01 in nanoseconds

    time = Time(epoch, format="cdf_tt2000")
    time.format = "isot"

    # Check if WAVES time matches overall timeFrame
    if time[0] >= timeFrame[0] or time[-1] <= timeFrame[1]:
        print("WARNING: Waves epoch from file is shorter than that provided time frame")
        print(f"WARNING: Waves start time: {time[0]}, waves end time: {time[-1]}")
        print(f"WARNING: Timeframe: {timeFrame}")

    frequency = wavesCDF.varget("Frequency")
    # print(frequency)

    wavesData = np.transpose(wavesCDF.varget("Data"))
    # print(np.shape(wavesData))

    # Calibrating by dividing by 377 Ohms
    for frequencyRow in wavesData:
        for flux in frequencyRow:
            flux = flux / 377

    # Adapted code taken from Corentin
    index_array = range(len(time))

    if vmin == False and vmax == False:
        vmin=np.quantile(wavesData,0.05)
        vmax=np.quantile(wavesData,0.95)
    
    image = ax.pcolormesh(index_array, frequency, wavesData, cmap="Spectral_r", norm=colors.LogNorm(vmin, vmax))
    ax.set_yscale("log")
    
    ax.set_ylabel("Frequency (kHz)")
    ax.set_xlabel("Time (s)")

    # cax = divider.append_axes("right", size=0.15, pad=0.2)

    fig.colorbar(image, extend='both', shrink=0.9,ax=ax, label="Flux Density (W m$^{-2}$ Hz$^{-1}$)")


def DateRange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
