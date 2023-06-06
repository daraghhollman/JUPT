import speasy as spz
import numpy as np

# Adjusted code from CORENTIN, juno_waves_cdf_data_rough_routines.py
def format_xlabel(time,x,y,z):
	def inner_function(index,pos=None):
		int_index = int(index)
		if int_index >= len(time):
			return ''
		return f'{time[int_index].strftime("%H:%M")}\n{x[int_index]:5.2f}\n{y[int_index]:3.2f}\n{z[int_index]:3.2f}'
	return inner_function
# End code from CORENTIN

def PlotEphemeris(ax, timeFrame):
    # Takes a subplot axis as input

    print("Retreiving ephemeris data...")
    # Pulls ephemeris data in x, y, z
    junoEphemeris = spz.amda.get_parameter("juno_eph_orb_jso", timeFrame[0], timeFrame[1])

    time = junoEphemeris.time

    ticksAmmount = 5
    timeInterval = len(time)/ticksAmmount

    ticksPos = [int(timeInterval*i) for i in range(ticksAmmount)] 

    ticksLabels = [str(time[int(timeInterval*i)])[0:10]+f"\nx\ny\nz" for i in range(ticksAmmount)]

    ax.set_xticks(ticksPos, labels=ticksLabels)

def CartesianPosToPolarPos(x, y, z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)
    phi = np.arctan2(y, x)

    return [r, theta, phi]
