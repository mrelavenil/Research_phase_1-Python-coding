import numpy as np
import matplotlib.pyplot as plt

# Actual energy values for Cu, Zr, Am
actual_energy = [8.04, 15.77, 17.5, 22.1, 59.4]

# Measured energy values for 15 Ikrum
measured_energy_15 = {
    10: [8.23, 16.23,18.05, 22.37, 60.05],
    40: [8.14, 15.4, 17.33, 21.37, 56.45]
}

measured_sigma_15 = {
    10: [1.65, 2.13, 2.43, 2.35, 6.77],
    40: [1.51, 1.83, 1.96, 2.10, 5.43]
}

measured_resolution_15 = {
    10: [48.34, 31.96, 32.78, 25.06, 26.84],
    40: [44.23, 27.46, 26.39, 22.38, 21.54]
}

# Measured energy values and sigma values for 50 Ikrum
measured_energy_50 = {
    10: [8.12, 16.04, 17.84, 22.43, 60.42],
    40: [8.27, 16.07, 17.6, 21.87, 58.22]
}

measured_sigma_50 = {
    10: [1.02, 0.89, 1.12, 1.16, 2.00],
    40: [0.97, 0.85, 1.02, 1.24, 1.69]
}
measured_resolution_50 = {
    10: [29.88, 13.35, 15.07, 12.36, 7.93],
    40: [28.39, 12.75, 13.73, 13.2, 6.71]
}


# Colors for each temperature
temp_colors = {10: "r", 40: "b"}

corrected_energy_15 = {
    10: [8.04, 15.97, 17.76, 22.05, 59.4],
    40: [8.04, 15.8, 17.81, 22.10, 59.4]
}

corrected_sigma_15 = {
    10: [1.52, 1.99, 2.29, 2.21, 6.59],
    40: [0.99, 1.33, 1.47, 1.62, 5.16]
}
corrected_resolution_15 = {
    10: [44.46, 28.89, 20.85, 23.57, 26.14],
    40: [28.96, 19.95, 19.75, 17.22, 20.46]
}

corrected_energy_50 = {
    10: [8.04, 15.81, 17.59, 21.7, 59.4],
    40: [8.04, 16.07, 17.6, 22.02, 59.4]
}

corrected_sigma_50 = {
    10: [1.07, 0.95, 1.17, 1.21, 2.03],
    40: [0.54, 0.41, 0.59, 0.82, 1.28 ]
}

corrected_resolution_50 = {
    10: [31.37, 14.16, 15.73, 12.85, 8.05],
    40: [15.71, 6.21, 7.92, 8.68, 5.07]
}
# Colors for temperature representation
temp_colors = {10: "r", 40: "b"}

# Plotting Energy and Sigma Comparisons with Error Bars
fig, ax = plt.subplots(2, 2, figsize=(10, 8))

# Common title for all subplots
fig.suptitle("Energy and Sigma Comparison: Measured vs Corrected (15 and 50 Ikrum)", fontsize=14)

# First plot: Measured Energy vs Actual Energy with Measured Sigma (15 Ikrum)
for temp, color in temp_colors.items():
    ax[0, 0].errorbar(actual_energy, measured_energy_15[temp], yerr=measured_sigma_15[temp], fmt='o', color=color, 
                      label=f"measured- {temp}C", capsize=5, linestyle='None')
    ax[0, 0].plot(actual_energy, measured_energy_15[temp], color=color, linestyle='--', marker='o', alpha=0.3)  # Connect points with solid line

ax[0, 0].set_title("15 Ikrum measured data", fontsize=10)
ax[0, 0].set_ylabel("Measured Energy (keV)", fontsize=10)
ax[0, 0].legend()

# Second plot: Corrected Energy vs Actual Energy with Corrected Sigma (15 Ikrum)
for temp, color in temp_colors.items():
    ax[0, 1].errorbar(actual_energy, corrected_energy_15[temp], yerr=corrected_sigma_15[temp], fmt='o', color=color, 
                      label=f"corrected {temp}C", capsize=5, linestyle='None')
    ax[0, 1].plot(actual_energy, corrected_energy_15[temp], color=color, linestyle='--', marker='o', alpha=0.3)  # Connect points with solid line

ax[0, 1].set_title("15 Ikrum corrected data", fontsize=10)
ax[0, 1].set_ylabel("Corrected Energy (keV)", fontsize=10)
ax[0, 1].legend()

# Third plot: Measured Energy vs Actual Energy with Measured Sigma (50 Ikrum)
for temp, color in temp_colors.items():
    ax[1, 0].errorbar(actual_energy, measured_energy_50[temp], yerr=measured_sigma_50[temp], fmt='o', color=color, 
                      label=f"measured {temp}C", capsize=5, linestyle='None')
    ax[1, 0].plot(actual_energy, measured_energy_50[temp], color=color, linestyle='--', marker='o', alpha=0.3)  # Connect points with solid line

ax[1, 0].set_title("50 Ikrum Measured data", fontsize=10)
ax[1, 0].set_xlabel("Actual Energy (keV)", fontsize=10)
ax[1, 0].set_ylabel("Measured Energy (keV)", fontsize=10)
ax[1, 0].legend()

# Fourth plot: Corrected Energy vs Actual Energy with Corrected Sigma (50 Ikrum)
for temp, color in temp_colors.items():
    ax[1, 1].errorbar(actual_energy, corrected_energy_50[temp], yerr=corrected_sigma_50[temp], fmt='o', color=color, 
                      label=f"corrected {temp}C", capsize=5, linestyle='None')
    ax[1, 1].plot(actual_energy, corrected_energy_50[temp], color=color, linestyle='--', marker='o', alpha=0.3)  # Connect points with solid line

ax[1, 1].set_title("50 Ikrum Corrected data", fontsize=10)
ax[1, 1].set_xlabel("Actual Energy (keV)", fontsize=10)
ax[1, 1].set_ylabel("Corrected Energy (keV)", fontsize=10)
ax[1, 1].legend()

# Adjust font size for x and y axis
for ax_row in ax.flat:
    ax_row.tick_params(axis='both', labelsize=7)

plt.tight_layout()
plt.show()


# Plotting the resolution comparison in a 2x2 collage layout
fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # Reduced figure size for clarity

bar_width = 0.2  # Width of the bars
index = np.arange(len(actual_energy))  # X-axis positions

# Common title for all subplots
fig.suptitle("Resolution Comparison: Measured vs Corrected (15 and 50 Ikrum)", fontsize=14)

# 1st plot: 15 Ikrum at 10°C
axs[0, 0].bar(index - bar_width / 2, measured_resolution_15[10], bar_width, label="Measured", color='r')
axs[0, 0].bar(index + bar_width / 2, corrected_resolution_15[10], bar_width, label="Corrected", color='r', alpha=0.5)
axs[0, 0].set_title("15 Ikrum at 10°C", fontsize=12)
axs[0, 0].set_ylabel("Resolution (%)", fontsize=10)
axs[0, 0].set_xticks(index)
axs[0, 0].set_xticklabels([f"{e} keV" for e in actual_energy], fontsize=9)
axs[0, 0].legend(fontsize=9)

# 2nd plot: 15 Ikrum at 40°C
axs[0, 1].bar(index - bar_width / 2, measured_resolution_15[40], bar_width, label="Measured", color='g')
axs[0, 1].bar(index + bar_width / 2, corrected_resolution_15[40], bar_width, label="Corrected", color='g', alpha=0.5)
axs[0, 1].set_title("15 Ikrum at 40°C", fontsize=12)
axs[0, 1].set_ylabel("Resolution (%)", fontsize=10)
axs[0, 1].set_xticks(index)
axs[0, 1].set_xticklabels([f"{e} keV" for e in actual_energy], fontsize=9)
axs[0, 1].legend(fontsize=9)

# 3rd plot: 50 Ikrum at 10°C
axs[1, 0].bar(index - bar_width / 2, measured_resolution_50[10], bar_width, label="Measured", color='b')
axs[1, 0].bar(index + bar_width / 2, corrected_resolution_50[10], bar_width, label="Corrected", color='b', alpha=0.5)
axs[1, 0].set_title("50 Ikrum at 10°C", fontsize=12)
axs[1, 0].set_xlabel("Actual Energy (keV)", fontsize=10)
axs[1, 0].set_ylabel("Resolution (%)", fontsize=10)
axs[1, 0].set_xticks(index)
axs[1, 0].set_xticklabels([f"{e} keV" for e in actual_energy], fontsize=9)
axs[1, 0].legend(fontsize=9)

# 4th plot: 50 Ikrum at 40°C
axs[1, 1].bar(index - bar_width / 2, measured_resolution_50[40], bar_width, label="Measured", color='y')
axs[1, 1].bar(index + bar_width / 2, corrected_resolution_50[40], bar_width, label="Corrected", color='y', alpha=0.5)
axs[1, 1].set_title("50 Ikrum at 40°C", fontsize=12)
axs[1, 1].set_xlabel("Actual Energy (keV)", fontsize=10)
axs[1, 1].set_ylabel("Resolution (%)", fontsize=10)
axs[1, 1].set_xticks(index)
axs[1, 1].set_xticklabels([f"{e} keV" for e in actual_energy], fontsize=9)
axs[1, 1].legend(fontsize=9)

# Adjusting the layout and displaying the plot
plt.tight_layout(rect=[0, 0, 1, 0.96])  # Make space for the common title
plt.show()