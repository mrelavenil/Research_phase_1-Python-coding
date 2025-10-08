import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the energy calculated_TOT file
file_path = r'D:\Elavenil\Miun\Phase 6\Text files\New folder\New folder\15Ikrum_energy values.txt'

# Function to parse the energy calculated_TOT file
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

# Parse the file and create DataFrame
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

# Actual energy values (replace with actual known values)
actual_energy_values = {'Am':59.4, 'Ag':22.1, 'Mo': 17.5, 'Zr': 15.7, 'Cu': 8.04}

# Extract material from the group column
df['Material'] = df['Group'].str.extract(r'Group_(\w+)')

# Map the actual energies based on the 'Material' column
df['Actual Energy'] = df['Material'].map(actual_energy_values)

# Function to calculate slope forcing the fit through (0,0)
def calculate_slope_through_origin(df):
    results = []
    for temp in sorted(df['Temperature'].unique()):
        for ikrum in df['Ikrum'].unique():
            temp_ikrum_data = df[(df['Temperature'] == temp) & (df['Ikrum'] == ikrum)]
            
            if len(temp_ikrum_data) > 1:  # Ensure enough points for linear fit
                x = temp_ikrum_data['Measured Energy'].values
                y = temp_ikrum_data['Actual Energy'].values
                
                # Compute slope manually (intercept = 0)
                slope = np.sum(x * y) / np.sum(x ** 2)
                intercept = 0  # Force fit through (0,0)

                results.append((ikrum, temp, slope, intercept))
            else:
                print(f"Not enough data for Ikrum {ikrum} at Temperature {temp}.")
    
    return results

# Calculate slopes forcing intercept at (0,0)
slope_intercept_results = calculate_slope_through_origin(df)

# Function to plot multiple subplots (like a collage)
def plot_all_fits(df, slope_intercept_results):
    num_plots = len(slope_intercept_results)
    cols = 3  # Number of columns in the grid
    rows = (num_plots // cols) + (num_plots % cols > 0)  # Adjust rows based on number of plots

    fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
    axes = axes.flatten()  # Flatten the 2D array of axes for easy iteration

    for i, (ikrum, temp, slope, intercept) in enumerate(slope_intercept_results):
        ax = axes[i]
        temp_ikrum_data = df[(df['Temperature'] == temp) & (df['Ikrum'] == ikrum)]

        # Scatter plot
        ax.scatter(temp_ikrum_data['Measured Energy'], temp_ikrum_data['Actual Energy'], label="Data Points", s=100)

        # Linear fit line through (0,0)
        x_vals = np.linspace(0, temp_ikrum_data['Measured Energy'].max(), 100)
        y_vals = slope * x_vals
        ax.plot(x_vals, y_vals, linestyle='--', label=f"Fit: y={slope:.4f}x", color='red')

        # Labels and title
        ax.set_xlabel('Measured Energy (keV)')
        ax.set_ylabel('Actual Energy (keV)')
        ax.set_title(f'Ikrum {ikrum}, Temp {temp}°C')
        ax.legend()
        ax.grid(True)

    # Hide unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()  # Adjust layout
    plt.show()

# Plot all fits as separate subplots
plot_all_fits(df, slope_intercept_results)

# Path to save the slope-intercept results
output_file_path = r'D:\Elavenil\Miun\Phase 6\Text files\New folder\New folder\slope_intercept_results_15Ikrum.txt'

# Write results to a text file
with open(output_file_path, 'w') as file:
    file.write("Ikrum, Temperature (°C), Slope, Intercept\n")
    for ikrum, temp, slope, intercept in slope_intercept_results:
        file.write(f"{ikrum}, {temp}, {slope:.4f}, {intercept}\n")

print(f"Slope-intercept results saved to: {output_file_path}")
