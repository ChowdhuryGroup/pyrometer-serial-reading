# written by Zhihan on 2024-03-16 Github uploaded
# fitting eheating low temp and high temp fitting with 1e-7A photodiode current break point
# data from 2024-03-15-1450
# fitted temperature check
# SS paddle position 2 and #123 on position 3 based fitting
import matplotlib.pyplot as plt
import loop_finding_breakpoint_for_eheating_fitting as LL
import numpy as np
from scipy.interpolate import interp1d


# PDcurrent from reading from file
T_heat = [23, 56, 119, 222, 308, 403, 479, 521, 557, 601, 708, 809, 892, 964, 996, 1078]
T_cool = [898, 790, 698, 620, 580, 520, 489, 433, 397, 344, 296, 188]
T = T_heat + T_cool
PDcurrent_heat = [
    1e-17,
    3.4682895444504425e-10,
    1.2644078006829318e-09,
    2.9709426030422037e-09,
    4.359284044852529e-09,
    1.3305852419875919e-08,
    4.081208615502874e-08,
    7.459379958163481e-08,
    1.2418077233178337e-07,
    2.1855220211364212e-07,
    7.203491918517102e-07,
    1.8430639556754613e-06,
    3.6417598039406585e-06,
    6.164129899843829e-06,
    7.570449270133395e-06,
    1.3492575817508623e-05,
]
PDcurrent_cool = [
    3.584089199648588e-06,
    1.4481013295153389e-06,
    5.805486011922767e-07,
    2.3782062896771095e-07,
    1.40902514544905e-07,
    6.167101673781872e-08,
    3.983319274425412e-08,
    1.6646508171902497e-08,
    9.9996171343264e-09,
    4.942312781253122e-09,
    2.435297297154193e-09,
    6.547646869137225e-10,
]
PDcurrent = PDcurrent_heat + PDcurrent_cool

# # Incorporating data from 2024-03-15
# manual_data = np.loadtxt("calibration/2024-03-15_1836.csv", delimiter=",", skiprows=1)
# pyro_data = np.loadtxt("calibration/2024-03-15_18-34-19.tsv", skiprows=1)
# fit_interpolated = interp1d(pyro_data[:, 0], pyro_data[:, 2])

# # Select only data above 500C, where filament background is small
# mask_500C = manual_data[:, 1] > 500.0
# T += list(manual_data[mask_500C, 1])
# PDcurrent += list(fit_interpolated(manual_data[mask_500C, 0]))

breakpoint = [2.435297297154193e-09, 4.5e-09, 2e-07]
PDcurrent_fraction, T_fraction = LL.fraction_generate(PDcurrent, T, breakpoint)
fitted_functions = {}
T_differences = {}
T_Errors = {}
poly_Ts = {}
f_catalogs = {}
PDcurrent, T = LL.sort_lists(PDcurrent, T)
for (PDcurrent_key_list, PDcurrent_list), (T_key_list, T_list) in zip(
    PDcurrent_fraction.items(), T_fraction.items()
):
    sec_fitted_function, T_difference, T_error, poly_T, f_catalog = (
        LL.sec_fitting_generate(PDcurrent_list, T_list)
    )
    fitted_functions[PDcurrent_key_list] = sec_fitted_function
    T_differences[PDcurrent_key_list] = T_difference
    T_Errors[PDcurrent_key_list] = T_error
    f_catalogs[PDcurrent_key_list] = f_catalog
    # print(poly_T)
    poly_Ts[PDcurrent_key_list] = poly_T


def temperature_from_current(PDcurrent_point):
    for i in range(len(breakpoint) - 1):
        if breakpoint[i] <= PDcurrent_point <= breakpoint[i + 1]:
            fitt_fun = f_catalogs[
                f"{breakpoint[i]} <= PDcurrent[j]< {breakpoint[i + 1]}"
            ](PDcurrent_point)
    if breakpoint[0] > PDcurrent_point:
        fitt_fun = f_catalogs[f" PDcurrent[j]< {breakpoint[0]}"](PDcurrent_point)
    elif PDcurrent_point > breakpoint[-1]:
        fitt_fun = f_catalogs[f"PDcurrent[j]> {breakpoint[-1]}"](PDcurrent_point)
    return fitt_fun


if __name__ == "__main__":
    plot = False
    repl = False

    if plot:
        fit_temperature = []
        for i in range(len(pyro_data[:, 1])):
            fit_temperature.append(temperature_from_current(pyro_data[i, 1]))

        plt.scatter(
            manual_data[:, 0], manual_data[:, 1], label="Thermocouple Temp. (C)", s=2.0
        )
        plt.scatter(pyro_data[:, 0], fit_temperature, label="Fit Temp. (C)", s=2.0)
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature (C)")
        plt.legend()
        plt.show()

        fit_interpolated = interp1d(pyro_data[:, 0], fit_temperature)
        plt.scatter(
            manual_data[:, 0], fit_interpolated(manual_data[:, 0]) - manual_data[:, 1]
        )
        plt.xlabel("Time (s)")
        plt.ylabel("Temperature Error (C)")
        plt.title("Discrepancy between fit and Thermocouple temperature")
        plt.show()

    if repl:
        while True:
            current = float(input("Enter a photodiode current in Amps: "))
            print(f"Corresponding Temperature (C): {temperature_from_current(current)}")
