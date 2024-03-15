# fitting eheating low temp and high temp fitting with 1e-7A photodiode current break point
# data from 2024-03-15-1450
# fitted temperature check
# SS paddle position 2 and #123 on position 3 based fitting
import matplotlib.pyplot as plt
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


fig, ax = plt.subplots(2, 1)
degree = 4
sorted_indices = sorted(range(len(T)), key=lambda i: T[i])
# Use the sorted indices to sort list2
PDcurrent = [PDcurrent[i] for i in sorted_indices]
T = sorted(T)
T_low = []
PDcurrent_low = []
T_high = []
PDcurrent_high = []
for i in range(len(PDcurrent)):
    if PDcurrent[i] <= 1e-7:
        PDcurrent_low.append(PDcurrent[i])
        T_low.append(T[i])
    else:
        PDcurrent_high.append(PDcurrent[i])
        T_high.append(T[i])
coefficientsT_low = np.polyfit(T_low, PDcurrent_low, degree)
coefficientsT_high = np.polyfit(T_high, PDcurrent_high, degree)

# Generate y values for the polynomial curve
poly_T_low = np.polyval(coefficientsT_low, T_low)
residuals_low = np.subtract(PDcurrent_low, poly_T_low)
poly_function_low = np.poly1d(coefficientsT_low)
poly_T_high = np.polyval(coefficientsT_high, T_high)
residuals_high = np.subtract(PDcurrent_high, poly_T_high)
poly_function_high = np.poly1d(coefficientsT_high)
# print(poly_function)
# Calculate mean squared error (MSE)
mse_low = np.mean(residuals_low**2)
mse_high = np.mean(residuals_high**2)


# Define the equation
T_solution_low = []
T_solution_high = []


for i in range(len(PDcurrent_low)):
    f_low = interp1d(poly_function_low(T_low), T_low, fill_value="extrapolate")
    # print(equation_expr)
    # print('see if works for high temp',f(1e-4))
    solutions_low = f_low(PDcurrent_low[i])
    # print(solutions)
    T_solution_low.append(solutions_low)
for i in range(len(PDcurrent_high)):
    f_high = interp1d(poly_function_high(T_high), T_high, fill_value="extrapolate")
    # print(equation_expr)
    # print('see if works for high temp',f(1e-4))
    solutions_high = f_high(PDcurrent_high[i])
    # print(solutions)
    T_solution_high.append(solutions_high)
# print(fitted_temp)
T_difference_high = np.subtract(T_high, T_solution_high)
T_difference_low = np.subtract(T_low, T_solution_low)
T_error_low = np.mean(T_difference_low**2)
T_error_high = np.mean(T_difference_high**2)


def temperature_from_current(current):
    if current <= 1e-7:
        f = interp1d(poly_function_low(T_low), T_low, fill_value=-1, bounds_error=False)
        fitted_T = f(
            current
        )  # PDcurrent is fetched from serial port reading and process main.py using thread;
    else:
        f = interp1d(
            poly_function_high(T_high), T_high, fill_value=-1, bounds_error=False
        )
        fitted_T = f(
            current
        )  # PDcurrent is fetched from serial port reading and process main.py using thread;
    return fitted_T


if __name__ == "__main__":
    ax[0].plot(
        T_low,
        poly_T_low,
        color="blue",
        label=f"fitting:{poly_function_low} \n with mse:{mse_low:.2e} \n with temperature rms-error:{np.sqrt(T_error_low):.2f}C",
    )
    ax[0].plot(
        T_high,
        poly_T_high,
        color="red",
        label=f"fitting:{poly_function_high} \n with mse:{mse_high:.2e} \n with temperature rms-error:{np.sqrt(T_error_high):.2f}C",
    )
    ax[0].scatter(T, PDcurrent)
    ax[0].set_xlabel("SS paddle Temperature/C")
    ax[0].set_ylabel("Photodiode current/A")
    ax[0].legend()
    plt.show()
