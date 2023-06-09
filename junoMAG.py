import speasy as spz
import numpy as np
import matplotlib.dates as mdates

import junoEphemeris

def PlotData(ax, timeFrame, plotEphemeris=False):
    # Takes one of the subplot axes as input

    print("Retrieving mag data...")
    junoFGM = spz.amda.get_parameter("juno_fgm_orb60_jso", timeFrame[0], timeFrame[1])
    
    mag = np.transpose(junoFGM.values)
    magX = mag[0]
    magY = mag[1]
    magZ = mag[2]
    magTotal = [np.sqrt(x**2 + y**2 + z**2) for x,y,z in zip(magX, magY, magZ)]

    time = junoFGM.time
    if not plotEphemeris:
        time_plot = junoFGM.time
    else:
        # If ephemerides are added later, an index must be used instead of a time table for the plot
        time_plot = np.arange(len(junoFGM.time))
    
    ax.plot(time_plot, magX, color="red", label="$B_x$")
    ax.plot(time_plot, magY, color="green", label="$B_y$")
    ax.plot(time_plot, magZ, color="blue", label="$B_z$")
    ax.plot(time_plot, magTotal, color="black", label="$|B|$")

    ax.legend(loc="upper center", ncol=4, fancybox=True, shadow=True)
    # ax.grid()

    unit = junoFGM.unit
    
    ax.set_ylabel(f"Magnetic Field Strength ({unit})")

    if not plotEphemeris:
        dateFmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(dateFmt)
        ax.set_xlabel("Date and Time")
    else:
        ax = junoEphemeris.PlotEphemeris(ax, time, timeFrame)
        ax.set_xlabel("Ephemeris")
    # print(ax.xaxis.get_majorticklocs())
