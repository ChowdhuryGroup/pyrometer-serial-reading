import matplotlib.pyplot as plt
import numpy as np

heatup_data = np.loadtxt("plots/2024-03-15_14-48-08_heatup.tsv", skiprows=1)
cooldown_data = np.loadtxt("plots/2024-03-15_15-30-27_cooldown.tsv", skiprows=1)

heatup_time = heatup_data[:, 0]
cooldown_time = cooldown_data[:, 0]

collated_time = np.concatenate((heatup_time, cooldown_time + heatup_time[-1]))
collated_current = np.concatenate((heatup_data[:, 1], cooldown_data[:, 1]))
collated_temperature = np.concatenate((heatup_data[:, 2], cooldown_data[:, 2]))

fig, axes = plt.subplots(1, 2)
axes[0].plot(collated_time, collated_current)
axes[0].set_xlabel("Time (s)")
axes[0].set_ylabel("Photodiode Camera (A)")
axes[1].plot(collated_time, collated_temperature)
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Fit Temperature (C)")
plt.show()
