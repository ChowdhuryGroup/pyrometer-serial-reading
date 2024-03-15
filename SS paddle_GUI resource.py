# fitting and plotting file for SS paddle --GUI file source

import calibration.SS_fitting as SS
from scipy.interpolate import interp1d
from time import time


# Priliminary test with plot temp read from pyrometer via serial port
# plot for threads
# Function to plot data


# add fitting and plot based received photodiode current
# add fitting and plot based received photodiode current
def f(PDcurrent_point):
    f = interp1d(
        SS.poly_function(SS.collated_temperatures),
        SS.collated_temperatures,
        fill_value="extrapolate",
    )
    fitted_T = f(
        PDcurrent_point
    )  # PDcurrent is fetched from serial port reading and process main.py using thread;
    return fitted_T
