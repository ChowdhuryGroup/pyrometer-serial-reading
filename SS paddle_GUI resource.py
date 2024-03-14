#fitting and plotting file for SS paddle --GUI file source

import SS_fitting as SS
import main

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sympy as sp
from scipy.interpolate import interp1d
import os
from time import time


#Priliminary test with plot temp read from pyrometer via serial port
#plot for threads
# Function to plot data
    
    


#add fitting and plot based received photodiode current
def f(PDcurrent_point):   
    f = interp1d(SS.poly_function(SS.T), SS.T,fill_value='extrapolate')
    fitted_T=f(PDcurrent_point) #PDcurrent is fetched from serial port reading and process main.py using thread;
    return fitted_T
