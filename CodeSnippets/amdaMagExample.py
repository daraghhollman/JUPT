import speasy as spz
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

print("Retrieving Data...")
junoFGM = spz.amda.get_parameter("juno_fgm_orb60_jso", "2018-01-01T00:00:00", "2018-01-1T12:00:00")


mag = np.transpose(junoFGM.values)
magX = mag[0]
magY = mag[1]
magZ = mag[2]
magTotal = [np.sqrt(x**2 + y**2 + z**2) for x,y,z in zip(magX, magY, magZ)]

time = junoFGM.time

plt.figure()

plt.plot(time, magX, color="red", label="$B_x$")
plt.plot(time, magY, color="green", label="$B_y$")
plt.plot(time, magZ, color="blue", label="$B_z$")
plt.plot(time, magTotal, color="black", label="$|B|$")

plt.legend(loc="upper center", ncol=4, fancybox=True, shadow=True)
plt.grid()

unit = junoFGM.unit
plt.ylabel(f"Magnetic Field ({unit})")
plt.xlabel("Date and Time")

plt.show()
