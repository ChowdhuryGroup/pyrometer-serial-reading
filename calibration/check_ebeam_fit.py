import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

manual_data = np.loadtxt("calibration/2024-03-15_1836.csv", delimiter=",", skiprows=1)
pyro_data = np.loadtxt("calibration/2024-03-15_18-34-19.tsv", skiprows=1)

plt.scatter(manual_data[:, 0], manual_data[:, 1], label="Thermocouple Temp. (C)", s=2.0)
plt.scatter(pyro_data[:, 0], pyro_data[:, 2], label="Fit Temp. (C)", s=2.0, alpha=0.5)
plt.xlabel("Time (s)")
plt.ylabel("Temperature (C)")
plt.legend()
plt.show()

fit_interpolated = interp1d(pyro_data[:, 0], pyro_data[:, 2])
plt.scatter(manual_data[:, 0], fit_interpolated(manual_data[:, 0]) - manual_data[:, 1])
plt.xlabel("Time (s)")
plt.ylabel("Temperature Error (C)")
plt.title("Discrepancy between fit and Thermocouple temperature")
plt.show()
