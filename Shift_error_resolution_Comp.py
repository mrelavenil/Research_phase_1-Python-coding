import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.lines as mlines

# Path to the text file
file_path = r'D:\Elavenil\Miun\Phase 6\Text files\Thresholdscan\Meanshift_thresholdscan.txt'

def parse_line(line):
    # Remove unwanted characters and strip any extra spaces
    line = line.replace('Â', '').strip()

    # Check if the line contains necessary keywords
    if not line or "Group" not in line or "Temperature" not in line or "Absolute Shift" not in line or "Relative Error" not in line or "Energy Resolution" not in line:
        print(f"Skipping line due to missing keywords: {line}")
        return None

    # Split the line into parts by commas
    parts = line.split(',')

    try:
        # Extract group and ikrum_group from the first part
        group = parts[0].split(':')[0].strip()
        ikrum_group = parts[0].split(':')[1].strip()

        # Extract and convert the temperature
        temperature_part = parts[1].split(':')[1].strip().replace('°C', '')
        temperature = int(temperature_part)

        # Extract and convert the shift
        shift_part = parts[2].split(':')[1].strip().replace('keV', '')
        shift = float(shift_part)

        # Extract and convert the relative error
        error_part = parts[3].split(':')[1].strip().replace('%', '')
        relative_error = float(error_part)

        # Extract and convert the energy resolution
        resolution_part = parts[4].split('=')[1].strip().replace('%', '')
        energy_resolution = float(resolution_part)

    except IndexError as e:
        print(f"Skipping malformed line: {line}")
        return None
    except ValueError as e:
        print(f"Error parsing values in line: {line} ({e})")
        return None

    # Return the parsed values
    return group, ikrum_group, temperature, shift, relative_error, energy_resolution



# Create lists to store the parsed data
groups = []
ikrum_groups = []
temperatures = []
shifts = []
relative_errors = []
energy_resolutions = []

# Open and read the text file
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        result = parse_line(line)
        
        if result is not None:
            group, ikrum_group, temperature, shift, relative_error, energy_resolution = result
            groups.append(group)
            ikrum_groups.append(ikrum_group)
            temperatures.append(temperature)
            shifts.append(shift)
            relative_errors.append(relative_error)
            energy_resolutions.append(energy_resolution)

# Convert the lists into a DataFrame
df = pd.DataFrame({
    'Group': groups,
    'Ikrum': ikrum_groups,
    'Temperature': temperatures,
    'Absolute_Shift': shifts,
    'Relative_Error': relative_errors,
    'Energy_Resolution': energy_resolutions
})

# Ensure the 'Group' column is of string type
df['Group'] = df['Group'].astype(str)

# Extract the material from the 'Group' column (e.g., Group_Cu -> Cu)
df['Material'] = df['Group'].str.extract(r'Group_(\w+)')

# Define temperature colors and markers for the materials
temp_colors = {20: 'blue', 40: 'red', 10: 'green'}
materials = ['Mo', 'Zr', 'Cu']
markers = {'Mo': 'o', 'Zr': 's', 'Cu': '^'}

# Plotting the Absolute Shift vs. Ikrum Group with bright colors and filled markers
plt.figure(figsize=(10, 6))

# Custom legend handles for Temperature (color only)
temp_handles = [
    mlines.Line2D([], [], color=color, marker='o', linestyle='None', markersize=8, label=f'{temp}°C')
    for temp, color in temp_colors.items()
]

# Custom legend handles for Material (marker shape only)
material_handles = [
    mlines.Line2D([], [], color='black', marker=marker, linestyle='None', markersize=8, label=material)
    for material, marker in markers.items()
]

# Loop through the materials and plot each one with different markers and colors for temperature
for material in materials:
    for temp in df['Temperature'].unique():
        material_data = df[(df['Material'] == material) & (df['Temperature'] == temp)]

        if not material_data.empty:
            # Plot the data points for Absolute Shift with filled markers and bright colors
            scatter = plt.scatter(
                material_data['Ikrum'], 
                material_data['Absolute_Shift'],  # Use Absolute Shift for the y-axis
                color=temp_colors[temp],  # Bright color for temperature
                marker=markers[material],  # Different shape for material
                edgecolor='black',  # Add black border for better visibility
                facecolors=temp_colors[temp],  # Fill the marker with color
                s=100  # Increase marker size for better visibility
            )

# Adding labels and title
plt.xlabel('Ikrum Group')
plt.ylabel('Absolute Shift (keV)')
plt.title('Absolute Shift vs. Ikrum Group in PC mode')

# Set the x-ticks for Ikrum group names (for readability)
plt.xticks(rotation=45)
plt.grid(True)

# Dynamically adjust the y-axis based on the data range of Absolute Shift
plt.ylim(df['Absolute_Shift'].min() - 2, df['Absolute_Shift'].max() + 2)

# First legend for Temperature (color)
legend1 = plt.legend(handles=temp_handles, title='Temperature', loc='upper right', fontsize=8)
plt.gca().add_artist(legend1)  # Add this legend manually

# Second legend for Material (marker)
plt.legend(handles=material_handles, title='Material', loc='upper center', fontsize=8)

# Show the plot
plt.tight_layout()
plt.show()






# Plotting the Relative Error vs. Ikrum Group with bright colors and filled markers
plt.figure(figsize=(10, 6))

# Custom legend handles for Temperature (color only)
temp_handles = [
    mlines.Line2D([], [], color=color, marker='o', linestyle='None', markersize=8, label=f'{temp}°C')
    for temp, color in temp_colors.items()
]

# Custom legend handles for Material (marker shape only)
material_handles = [
    mlines.Line2D([], [], color='black', marker=marker, linestyle='None', markersize=8, label=material)
    for material, marker in markers.items()
]

# Loop through the materials and plot each one with different markers and colors for temperature
for material in materials:
    for temp in df['Temperature'].unique():
        material_data = df[(df['Material'] == material) & (df['Temperature'] == temp)]

        if not material_data.empty:
            # Plot the data points for Relative Error with filled markers and bright colors
            scatter = plt.scatter(
                material_data['Ikrum'], 
                material_data['Relative_Error'],  # Use Relative Error for the y-axis
                color=temp_colors[temp],  # Bright color for temperature
                marker=markers[material],  # Different shape for material
                edgecolor='black',  # Add black border for better visibility
                facecolors=temp_colors[temp],  # Fill the marker with color
                s=100  # Increase marker size for better visibility
            )

# Adding labels and title
plt.xlabel('Ikrum Group')
plt.ylabel('Relative Error (%)')
plt.title('Relative Error vs. Ikrum Group in PC mode')

# Set the x-ticks for Ikrum group names (for readability)
plt.xticks(rotation=45)
plt.grid(True)

# Dynamically adjust the y-axis based on the data range of Relative Error
plt.ylim(df['Relative_Error'].min() - 2, df['Relative_Error'].max() + 2)

# First legend for Temperature (color)
legend1 = plt.legend(handles=temp_handles, title='Temperature', loc='upper right', fontsize=8)
plt.gca().add_artist(legend1)  # Add this legend manually

# Second legend for Material (marker)
plt.legend(handles=material_handles, title='Material', loc='upper center', fontsize=8)

# Show the plot
plt.tight_layout()
plt.show()




# Plotting the Energy Resolution vs. Ikrum Group with bright colors and filled markers
plt.figure(figsize=(10, 6))

# Custom legend handles for Temperature (color only)
temp_handles = [
    mlines.Line2D([], [], color=color, marker='o', linestyle='None', markersize=8, label=f'{temp}°C')
    for temp, color in temp_colors.items()
]

# Custom legend handles for Material (marker shape only)
material_handles = [
    mlines.Line2D([], [], color='black', marker=marker, linestyle='None', markersize=8, label=material)
    for material, marker in markers.items()
]

# Loop through the materials and plot each one with different markers and colors for temperature
for material in materials:
    for temp in df['Temperature'].unique():
        material_data = df[(df['Material'] == material) & (df['Temperature'] == temp)]

        if not material_data.empty:
            # Plot the data points for Energy Resolution with filled markers and bright colors
            scatter = plt.scatter(
                material_data['Ikrum'], 
                material_data['Energy_Resolution'],  # Use Energy Resolution for the y-axis
                color=temp_colors[temp],  # Bright color for temperature
                marker=markers[material],  # Different shape for material
                edgecolor='black',  # Add black border for better visibility
                facecolors=temp_colors[temp],  # Fill the marker with color
                s=100  # Increase marker size for better visibility
            )

# Adding labels and title
plt.xlabel('Ikrum Group')
plt.ylabel('Energy Resolution (%)')
plt.title('Energy Resolution vs. Ikrum Group in PC mode')

# Set the x-ticks for Ikrum group names (for readability)
plt.xticks(rotation=45)
plt.grid(True)

# Dynamically adjust the y-axis based on the data range of Absolute Shift
plt.ylim(0,5)

# First legend for Temperature (color)
legend1 = plt.legend(handles=temp_handles, title='Temperature', loc='upper right', fontsize=8)
plt.gca().add_artist(legend1)  # Add this legend manually

# Second legend for Material (marker)
plt.legend(handles=material_handles, title='Material', loc='upper center', fontsize=8)

# Show the plot
plt.tight_layout()
plt.show()
