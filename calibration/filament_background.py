import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

slow_decay_data = np.genfromtxt("calibration/x-2024-03-08 19 38 09.txt", skip_header=3)

time = slow_decay_data[:, 0]
current = slow_decay_data[:, 2]


def poly(x, a, b, c):
    # a, b, c = -5.22678849e-03  1.96808264e-06 -4.18026309e-10
    d = 5.13894306e-17
    return a * x + b * x**2 + c * x**3 + d * x**4


guess_params = [-np.log(2) / 150.0, 0.0, 0.0]
# guess_params = [0.0]

normalized_log_data = np.log(current / current[0])
popt, pcov = curve_fit(
    poly,
    time,
    normalized_log_data,
    bounds=(
        [2 * guess_params[0], -1.0, -1.0],
        [0.25 * guess_params[0], 1.0, 1.0],
    ),
)
print(f"Optimized parameters: {popt}")

fig, axis = plt.subplots(1, 1)
axis.plot(time, np.exp(normalized_log_data))
# axis.set_yscale("log")
plt.plot(time, np.exp(poly(time, *popt)))
plt.xlabel("Time (s)")
plt.ylabel("Photocurrent (A)")
plt.title("Cooldown before Radiative Heating 2024-03-09")
plt.show()

#######################################

radiant_run_data = np.genfromtxt("calibration/x-2024-03-08 21 50 26.txt", skip_header=3)
time = radiant_run_data[:, 0]
current = radiant_run_data[:, 2]

plt.plot(time, current)
plt.xlabel("Time (s)")
plt.ylabel("Photodiode Current (A)")
plt.title("Radiative Heating Test 2024-03-09")
plt.show()

filament_contributions = []
filament_powers = np.array(
    [
        96,
        86.8,
        75.4,
        67.2,
        58.3,
        50,
        41.4,
        35.2,
        28,
        22.2,
        17,
        11.2,
        7.2,
        3.6,
        1.3,
    ]
)

time_windows = [
    (5622, 5635),
    (5736, 5746),
    (5824, 5838),
    (5953, 5967),
    (6095, 6101),
    (6200, 6210),
    (6295, 6304),
    (6382, 6390),
    (6505, 6513),
    (6577, 6590),
    (6762, 6769),
    (6885, 6895),
    (7028, 7044),
    (7188, 7225),
    (7374, 7426),
]


def linear(x, m, b):
    return m * x + b


def get_contribution(start_time: float, end_time: float) -> float:
    selected_indices = (time > start_time) & (time < end_time)
    selected_time = time[selected_indices] - time[selected_indices][0]
    guess_params = [1.0e-8, 6.0e-8]
    popt, _ = curve_fit(linear, selected_time[-15:], current[selected_indices][-15:])

    if False:
        plt.plot(
            selected_time, current[selected_indices] - linear(selected_time, *popt)
        )
        plt.show()
    contribution = abs(np.min(current[selected_indices] - linear(selected_time, *popt)))
    print(contribution)
    return contribution


for i in range(len(time_windows)):
    filament_contributions.append(
        get_contribution(time_windows[i][0], time_windows[i][1])
    )
print(filament_contributions)


def second_order_poly(x, a, b):
    return a * x + b * x**2


def r_squared(xdata, ydata, f, *popt):
    residuals = ydata - f(xdata, *popt)
    sum_of_squares_residuals = np.sum(residuals**2)
    sum_of_squares_total = np.sum((ydata - np.mean(ydata)) ** 2)
    return 1 - sum_of_squares_residuals / sum_of_squares_total


popt, pcov = curve_fit(second_order_poly, filament_powers, filament_contributions)
print(popt, pcov)

print(
    f"R squared: {r_squared(filament_powers, filament_contributions, second_order_poly, *popt)}"
)

plt.scatter(filament_powers, filament_contributions)
plt.plot(filament_powers, second_order_poly(filament_powers, *popt))
plt.ylabel("Photocurrent (A)")
plt.xlabel("Filament Power (W)")
plt.title("Filament Contribution to Photocurrent in Radiative Cooldown")
plt.show()
