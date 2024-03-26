# fitting eheating low temp and high temp fitting with 1e-7A photodiode current break point
# data from 2024-03-15-1450 and 2024-03-15-1836
# fitted temperature check
# SS paddle position 2 and #123 on position 3 based fitting
import numpy as np
from scipy.interpolate import interp1d
import loop_finding_breakpoint_for_eheating_fitting as LL


manual_data1 = np.loadtxt("calibration/2024-03-20-1230.csv", delimiter=",")
pyro_data1 = np.loadtxt("calibration/2024-03-20_12-18-59.tsv", skiprows=1)
interpolated_photocurrent1 = interp1d(pyro_data1[:, 0], pyro_data1[:, 1])
manual_data2 = np.loadtxt("calibration/2024-03-20-1410.csv", delimiter=",")
pyro_data2 = np.loadtxt("calibration/2024-03-20_14-10-33.tsv", skiprows=1)
interpolated_photocurrent2 = interp1d(pyro_data2[:, 0], pyro_data2[:, 1])
PDcurrent1 = interpolated_photocurrent1(manual_data1[:, 0])
PDcurrent2 = interpolated_photocurrent2(manual_data2[:, 0])
PDcurrent1 = list(PDcurrent1)
PDcurrent2 = list(PDcurrent2)
PDcurrent = PDcurrent1 + PDcurrent2
T1 = manual_data1[:, 1]
T2 = manual_data2[:, 1]
T1 = T1.tolist()
T2 = T2.tolist()
T = T1 + T2

# breakpoint=[5e-8]
breakpoint = [2e-7]
PDcurrent, T = LL.sort_lists(PDcurrent, T)
PDcurrent_fraction, T_fraction = LL.fraction_generate(PDcurrent, T, breakpoint)
fitted_functions = {}
T_differences = {}
T_Errors = {}
poly_Ts = {}
f_catalogs = {}
for (PDcurrent_key_list, PDcurrent_list), (T_key_list, T_list) in zip(
    PDcurrent_fraction.items(), T_fraction.items()
):
    sorted_lists = sorted(
        zip(T_list, PDcurrent_list)
    )  # use sorted pdcurrent index sort T
    # Unpack the sorted lists
    T_list, PDcurrent_list = zip(*sorted_lists)
    sec_fitted_function, T_difference, T_error, poly_T, f_catalog = (
        LL.sec_fitting_generate(PDcurrent_list, T_list)
    )
    fitted_functions[PDcurrent_key_list] = sec_fitted_function
    T_differences[PDcurrent_key_list] = T_difference
    T_Errors[PDcurrent_key_list] = T_error
    f_catalogs[PDcurrent_key_list] = f_catalog
    poly_Ts[PDcurrent_key_list] = poly_T


def temperature_from_current(PDcurrent_point):
    if not breakpoint:
        fitt_fun = f_catalogs["all"](PDcurrent_point)
    else:
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
    fitted_T = []
    for i in range(len(PDcurrent)):
        fitted_T.append(temperature_from_current(PDcurrent[i]))
    T_difference = np.subtract(T, fitted_T)
