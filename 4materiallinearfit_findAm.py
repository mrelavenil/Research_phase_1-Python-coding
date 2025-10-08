import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Path to the text file
file_path = r'D:\Elavenil\Miun\Phase 6\Text files\energy calibrated_TOT_4material.txt'

def parse_line(line):
    line = line.replace('Â', '').strip()
    if not line or "Group" not in line or "Temperature" not in line or "Energy" not in line:
        return None

    parts = line.split(',')

    try:
        group = parts[0].split(':')[0].strip()
        ikrum_group = parts[0].split(':')[1].strip()
        temperature = int(parts[1].split(':')[1].strip().replace('°C', ''))
        measured_energy = float(parts[2].split(':')[1].strip().replace('keV', ''))

        return group, ikrum_group, temperature, measured_energy

    except (IndexError, ValueError):
        return None

# Parse file and create DataFrame
groups, ikrum_groups, temperatures, measured_energies = [], [], [], []

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        result = parse_line(line)
        if result:
            group, ikrum_group, temperature, measured_energy = result
            groups.append(group)
            ikrum_groups.append(ikrum_group)
            temperatures.append(temperature)
            measured_energies.append(measured_energy)

df = pd.DataFrame({
    'Group': groups,
    'Ikrum': ikrum_groups,
    'Temperature': temperatures,
    'Measured Energy': measured_energies,
})

# Extract material from Group column
df['Material'] = df['Group'].str.extract(r'Group_(\w+)')

# Define actual energy values for four materials
actual_energy_values = {'Ag': 22.1,'Mo': 17.5, 'Zr': 15.7, 'Cu': 8.04, 'Target': 59.4}  # Added 'Target' material
df['Actual Energy'] = df['Material'].map(actual_energy_values)

# Define temperature colors
temp_colors = {10: 'green', 20: 'blue', 40: 'red'}

# Ensure Cu → Zr → Mo → Target order
material_order = {'Cu': 1, 'Zr': 2, 'Mo': 3, 'Target': 4}

# Target actual energy values to estimate
target_actual_energies = [ 59.4]  # Added 59.4 keV

# Get first 10 unique Ikrum values
unique_ikrum_values = df['Ikrum'].unique()[:10]

# Create a 2-row, 5-column subplot layout
fig, axes = plt.subplots(2, 5, figsize=(18, 7))  
axes = axes.flatten()  # Convert to 1D array for easier looping

# Store estimated measured energy values
estimated_measured_energies = {temp: [] for temp in temp_colors.keys()}

# Generate plots in the subplots
for idx, ikrum in enumerate(unique_ikrum_values):
    ax = axes[idx]  # Select the current subplot

    # Filter data for current Ikrum value
    ikrum_data = df[df['Ikrum'] == ikrum]

    # Scatter plot for all materials at each temperature
    for temp in sorted(df['Temperature'].unique()):  
        temp_data = ikrum_data.loc[ikrum_data['Temperature'] == temp]
        
        if not temp_data.empty:
            ax.scatter(
                temp_data['Measured Energy'], 
                temp_data['Actual Energy'], 
                color=temp_colors[temp], 
                marker='o',
                s=20  # Smaller marker size
            )

    # Linear fit for Cu → Zr → Mo → Target at each temperature, starting from (0,0)
    for temp in sorted(df['Temperature'].unique()):
        temp_data = ikrum_data.loc[ikrum_data['Temperature'] == temp].copy()
        temp_data['Material Order'] = temp_data['Material'].map(material_order)
        temp_data = temp_data.sort_values(by='Material Order')  # Enforce Cu → Zr → Mo → Target order
        
        if len(temp_data) > 1:  # Ensure at least two points to fit
            x = temp_data['Measured Energy'].values
            y = temp_data['Actual Energy'].values

            # Fit line: y = m*x
            coeff = np.sum(y * x) / np.sum(x**2)  # Calculate slope manually
            x_fit = np.linspace(0, max(x) + 5, 100)  
            y_fit = coeff * x_fit  

            # Plot fitted line
            ax.plot(x_fit, y_fit, linestyle='-', color=temp_colors[temp], alpha=0.8, linewidth=1)  

            # Estimate measured energy for 22.1, 24.9, and 59.4 keV
            estimated_x = np.array(target_actual_energies) / coeff
            estimated_measured_energies[temp].append(estimated_x)

            # Mark estimated points on the graph
            ax.scatter(estimated_x, target_actual_energies, color=temp_colors[temp], marker='x', s=30, label=f"Est. {temp}°C")

    # Subplot formatting
    ax.set_xlabel('Measured Energy (keV)', fontsize=8)
    ax.set_ylabel('Actual Energy (keV)', fontsize=8)
    ax.set_title(f'Ikrum: {ikrum}', fontsize=9)
    ax.set_xlim(0, 70)  # Adjusted for 59.4 keV
    ax.set_ylim(0, 70)  
    ax.tick_params(axis='both', labelsize=7)  
    ax.grid(True, linewidth=0.5)

# Add a legend
legend_patches = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=6, label=f"{temp}°C") 
                  for temp, color in temp_colors.items()]
fig.legend(handles=legend_patches, title="Temperature", loc='upper center', fontsize=8, ncol=3)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.95])  
plt.suptitle('Energy Comparison for Different Ikrum Values (Extended Fit)', fontsize=14, fontweight='bold')

plt.show()

# Print estimated values for measured energy
for temp in estimated_measured_energies.keys():
    print(f"Estimated Measured Energy for {temp}°C:")
    
    if not estimated_measured_energies[temp]:  # Check if the list is empty
        print(f"  No estimated values for {temp}°C (insufficient data)")
        continue

    for i, ikrum in enumerate(unique_ikrum_values):
        if i >= len(estimated_measured_energies[temp]):  # Prevent out-of-range errors
            print(f"  Ikrum {ikrum}: No estimation available (missing data)")
            continue
        
        est_vals = estimated_measured_energies[temp][i]
        print(f"  Ikrum {ikrum}: For Actual Energy 59.4 keV → {est_vals[0]:.2f} keV")

