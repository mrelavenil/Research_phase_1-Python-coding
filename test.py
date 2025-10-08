
import matplotlib.pyplot as plt


# Define the columns from your Excel data as a dictionary
data = {
    'materials' : ['Cu', 'Zr', 'Mo', 'Ag', 'Am'],    
    'Actual Energy': [8.04, 15.7, 17.5, 22.1, 59.4], 
  
    'Measured Energy_2IK_10': [8.71, 16.49, 18.03, 22.58, 61.22],  # Measured energy at 2IK
    'Measured Sigma_2IK_10': [12.64, 15.85, 26.13, 29.18, 75.22],  # Measured sigma for 2IK
    'Measured Energy_5IK_10': [8.52, 16.39, 18.03, 21.81, 58.93],  # Measured energy at 5IK
    'Measured Sigma_5IK_10': [5.41, 6.76, 8.62, 10.9, 23.71],  # Measured sigma for 5IK_10
    'Measured Energy_10IK_10': [8.31, 16.21, 17.59, 23.11, 60.12],  # Measured energy at 10IK_10
    'Measured Sigma_10IK_10': [2.47, 3.28, 3.94, 4.89, 11.84],  # Measured sigma for 10IK_10
    'Measured Energy_15IK_10': [8.23, 16.23, 18.09, 22.37, 60.05],  # Measured energy at 15IK_10
    'Measured Sigma_15IK_10': [1.65, 2.13, 2.43, 2.35, 6.77],  # Measured sigma for 15IK_10
    'Measured Energy_50IK_10': [8.12, 16.04, 17.84, 22.43, 60.42],  # Measured energy at 50IK_10
    'Measured Sigma_50IK_10': [1.02, 0.89, 1.12, 1.24, 2],  # Measured sigma for 50IK_10

    'Measured Energy_2IK_40': [7.3, 14.45, 16.4, 20.43, 48.24],  # Measured energy at 2IK_40
    'Measured Sigma_2IK_40': [9.36, 11.86, 15.91, 17.78, 42.95],  # Measured sigma for 2IK_40
    'Measured Energy_5IK_40': [7.89, 15.42, 16.61, 21.26, 54.49],  # Measured energy at 5IK_40
    'Measured Sigma_5IK_40': [4.57, 5.42, 5.98, 7.53, 16.93],  # Measured sigma for 5IK_40
    'Measured Energy_10IK_40': [8.07, 15.75, 16.9, 21.48, 56.04],  # Measured energy at 10IK_40
    'Measured Sigma_10IK_40': [2.13, 2.61, 2.89, 3.78, 7.83],  # Measured sigma for 10IK_40
    'Measured Energy_15IK_40': [8.14, 15.4, 17.33, 21.37, 56.45],  # Measured energy at 15IK_40
    'Measured Sigma_15IK_40': [1.51, 1.83, 1.96, 2.1, 5.43],  # Measured sigma for 15IK_40
    'Measured Energy_50IK_40': [8.27, 16.07, 17.61, 21.87, 58.22],  # Measured energy at 50IK_40
    'Measured Sigma_50IK_40': [0.97, 0.85, 1.02, 1.16, 1.69],  # Measured sigma for 50IK_40
    
    # Add data for other IK values (10IK, 15IK, 50IK)
    'Corrected Energy_2IK_10': [8.04, 15.66, 17.1, 21.66, 59.4],  # Corrected energy at 2IK_10
    'Corrected Sigma_2IK_10': [11.61, 15.21, 24.82, 27.94, 74.13],  # Corrected sigma for 2IK_10
    'Corrected Energy_5IK_10': [8.04, 15.53, 17.23, 21.11, 59.4],  # Corrected energy at 5IK_10
    'Corrected Sigma_5IK_10': [4.87, 6.23, 8.13, 10.47, 23.52],  # Corrected sigma for 5IK_10
    'Corrected Energy_10IK_10': [8.04, 15.87, 17.41, 22.88, 59.4],  # Corrected energy at 10IK_10
    'Corrected Sigma_10IK_10': [2.24, 3.05, 3.7, 4.65, 11.35],  # Corrected sigma for 10IK_10
    'Corrected Energy_15IK_10': [8.04, 15.97, 17.76, 22.05, 59.4],  # Corrected energy at 15IK_10
    'Corrected Sigma_15IK_10': [1.52, 1.99, 2.29, 2.21, 6.59],  # Corrected sigma for 15IK_10
    'Corrected Energy_50IK_10': [8.04, 15.81, 17.59, 22.1, 59.4],  # Corrected energy at 50IK_10
    'Corrected Sigma_50IK_10': [1.07, 0.94, 1.17, 1.21, 2.03],  # Corrected sigma for 50IK
   
       # Add data for other IK values (10IK, 15IK, 50IK)
    'Corrected Energy_2IK_40': [8.04, 17.01, 19.45, 24.49, 59.4],  # Corrected energy at 2IK_40
    'Corrected Sigma_2IK_40': [10.62, 13.76, 18.84, 21.19, 52.74],  # Corrected sigma for 2IK_40
    'Corrected Energy_5IK_40': [8.04, 16.37, 17.5, 22.05, 59.4],  # Corrected energy at 5IK_40
    'Corrected Sigma_5IK_40': [4.39, 5.32, 5.95, 7.66, 18.03],  # Corrected sigma for 5IK_40
    'Corrected Energy_10IK_40': [8.04, 16.7, 18.08, 22.52, 59.4],  # Corrected energy at 10IK_40
    'Corrected Sigma_10IK_40': [1.68, 2.2, 2.49, 3.45, 7.79],  # Corrected sigma for 10IK_40
    'Corrected Energy_15IK_40': [8.04, 15.8, 17.81, 22.1, 59.4],  # Corrected energy at 15IK_40
    'Corrected Sigma_15IK_40': [0.99, 1.33, 1.47, 1.62, 5.15],  # Corrected sigma for 15IK_40
    'Corrected Energy_50IK_40': [8.04, 16.07, 17.6, 22.02, 59.4],  # Corrected energy at 50IK_40
    'Corrected Sigma_50IK_40': [0.54, 0.41, 0.59, 0.82, 1.28],  # Corrected sigma for 50IK
   
}


import matplotlib.pyplot as plt

# Materials list for labeling the x-axis
materials = ['Cu', 'Zr', 'Mo', 'Ag', 'Am']

# List of all IK values
ik_values = ['2IK', '5IK', '10IK', '15IK', '50IK']

# Create a 2-row, 5-column subplot layout with a compact figsize
fig, axes = plt.subplots(2, 5, figsize=(12, 8))   
axes = axes.flatten()  # Convert to 1D array for easier looping

# Loop through each IK value and plot the data
for i, ik in enumerate(ik_values):
    # Extract data for each IK
    actual_energy = data['Actual Energy']
    measured_energy_10 = data[f'Measured Energy_{ik}_10']
    measured_sigma_10 = data[f'Measured Sigma_{ik}_10']
    measured_energy_40 = data[f'Measured Energy_{ik}_40']
    measured_sigma_40 = data[f'Measured Sigma_{ik}_40']

    corrected_energy_10 = data.get(f'Corrected Energy_{ik}_10', [None]*5)
    corrected_sigma_10 = data.get(f'Corrected Sigma_{ik}_10', [None]*5)
    corrected_energy_40 = data.get(f'Corrected Energy_{ik}_40', [None]*5)
    corrected_sigma_40 = data.get(f'Corrected Sigma_{ik}_40', [None]*5)

    # Plot Actual Energy vs Measured Energy with error bars (temperature 10°C and 40°C)
    axes[i].errorbar(actual_energy, measured_energy_10, yerr=measured_sigma_10, fmt='--o', label='Measured 10°C', color='blue', capsize=5)
    axes[i].errorbar(actual_energy, measured_energy_40, yerr=measured_sigma_40, fmt='--s', label='Measured 40°C', color='red', capsize=5,alpha=0.5)
    axes[i].set_title(f'{ik} Actual vs Measured Energy', fontsize=9)  # Smaller font size for subplot titles
    axes[i].set_xlabel('Actual Energy (KeV)', fontsize=8)  # Smaller font size for x-axis label
    axes[i].set_ylabel('Measured Energy (KeV)', fontsize=8)  # Smaller font size for y-axis label
    axes[i].legend(loc='best', fontsize=7)  # Smaller font size for legend

    # Plot Actual Energy vs Corrected Energy with error bars (temperature 10°C and 40°C)
    axes[i + 5].errorbar(actual_energy, corrected_energy_10, yerr=corrected_sigma_10, fmt='--o', label='Corrected 10°C', color='blue', capsize=5)
    axes[i + 5].errorbar(actual_energy, corrected_energy_40, yerr=corrected_sigma_40, fmt='--s', label='Corrected 40°C', color='red', capsize=5,alpha=0.5)
    axes[i + 5].set_title(f'{ik} Actual vs Corrected Energy', fontsize=9)  # Smaller font size for subplot titles
    axes[i + 5].set_xlabel('Actual Energy (KeV)', fontsize=8)  # Smaller font size for x-axis label
    axes[i + 5].set_ylabel('Corrected Energy (KeV)', fontsize=8)  # Smaller font size for y-axis label
    axes[i + 5].legend(loc='best', fontsize=7)  # Smaller font size for legend

# Add a general title for the whole figure
fig.suptitle('Comparison of Measured and Corrected Energy', fontsize=14)

# Adjust layout to avoid overlap and ensure readability
plt.tight_layout()
plt.subplots_adjust(top=0.92)  # To make room for the general title

# Show the plot
plt.show()
