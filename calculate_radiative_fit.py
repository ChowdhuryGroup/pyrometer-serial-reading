# written by Zhihan on 2024-03-16
# fitting eheating low temp and high temp fitting with 1e-7A photodiode current break point
# data from 2024-03-15-1450
# fitted temperature check
# SS paddle position 2 and #123 on position 3 based fitting
#
# modified by Liam Clink on 2025-04-23
# Get Temperature from PhotioDiode current while doing
# radiative heating of a stainless steel paddle

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import interp1d

# import loop_finding_breakpoint_for_heating_fitting as LL

fig, ax = plt.subplots(2, 1)
ax1 = ax[0].twinx()
ax[0].set_xlabel("SS TC temp/C")
ax[0].set_ylabel("Photodiode current/A")
ax1.set_ylabel("Fitted temp error/C")
# PDcurrent from reading from file
temperature_heating_2 = [
    23,
    48,
    97,
    151,
    200,
    251,
    303,
    356,
    399,
    430,
    463,
    488,
    513,
    535,
    557,
]
temperature_cooling_2 = [535, 494, 451, 386, 343, 270, 204]
pd_current_2 = [
    1.57563e-14,
    1.36552e-10,
    5.95930e-10,
    1.11267e-9,
    1.75246e-9,
    2.22992e-9,
    3.50299e-9,
    6.60268e-9,
    1.29115e-8,
    1.95156e-8,
    3.18625e-8,
    4.59664e-8,
    6.52400e-8,
    8.86026e-8,
    1.18615e-7,
    8.86026e-8,
    5.03735e-8,
    2.57612e-8,
    9.63213e-9,
    4.23566e-9,
    1.26999e-9,
    1.92568e-10,
]

temperature_heating_3 = [
    23,
    38,
    78,
    91,
    171,
    245,
    307,
    364,
    391,
    428,
    460,
    482,
    512,
    533,
    555,
]
temperature_cooling_3 = [400, 237, 158]
pd_current_3 = [
    2.92245e-11,
    1.88338e-10,
    5.52298e-10,
    1.01623e-9,
    1.69966e-9,
    2.49622e-9,
    4.11771e-9,
    7.84387e-9,
    1.19155e-8,
    2.02186e-8,
    3.24033e-8,
    4.48962e-8,
    6.85131e-8,
    1.04963e-7,
    1.22096e-7,
    1.16205e-8,
    1.12471e-9,
    4.62789e-10,
]

T = np.array(
    (
        temperature_heating_2
        + temperature_cooling_2
        + temperature_heating_3
        + temperature_cooling_3
    )
)
PDcurrent = np.array((pd_current_2 + pd_current_3))


def black_body_fit(temperature, scale, zero_temperature, shift, lin_slope):
    """
    Model of photodiode response to black body radiation
    """
    shifted_temperature = temperature - zero_temperature
    result = scale * shifted_temperature**4
    mask = shifted_temperature <= 0
    result[mask] = 0
    result += shift + lin_slope * temperature
    result[result < 0] = 0
    return result


popt, _ = curve_fit(
    black_body_fit,
    T,
    PDcurrent,
)

plt.clf()
plt.scatter(T, PDcurrent, s=0.5)
plt.xlabel("Temperature (C)")
plt.ylabel("Photodiode Current (A)")
test_temperatures = np.linspace(0, 560, 1000)
plt.plot(test_temperatures, black_body_fit(test_temperatures, *popt))
plt.show()

current_interpolator = interp1d(
    test_temperatures, black_body_fit(test_temperatures, *popt)
)
test_temperatures = np.linspace(250, 560, 1000)
temperature_interpolator = interp1d(
    current_interpolator(test_temperatures),
    test_temperatures,
    fill_value=-1,
    bounds_error=False,
)
test_currents = current_interpolator(test_temperatures)
np.savetxt(
    "radiative_calibration.tsv",
    np.vstack(
        (
            test_currents[test_temperatures >= 350],
            test_temperatures[test_temperatures >= 350],
        )
    ).T,
    delimiter="\t",
)

current = sorted(PDcurrent)[:-1]
plt.scatter(current, temperature_interpolator(current))
plt.show()

plt.scatter(PDcurrent, temperature_interpolator(PDcurrent) - T, s=0.5)
plt.ylabel("Temperature Error (C)")
plt.xlabel("Photodiode Current (A)")
plt.show()
