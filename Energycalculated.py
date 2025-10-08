import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np

# List of text files to process
file_paths = [
    r'D:\Elavenil\Miun\Phase 6\Text files\Am spectrum.txt',
]

# Dictionary to store grouped data
grouped_data = defaultdict(lambda: {'temperatures': [], 'mu': [], 'energy': [], 'mu_20': None, 'energy_shift': [], 'relative_error': []})

reference_energy = 59.4 # keV for 20°C μ value
reference_temperature = 20  # °C
pending_entries = []  # Store entries if μ_20 is missing initially

# Process each file
for file_path in file_paths:
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        
        for line in lines:
            try:
                # Extract temperature
                temp_match = re.search(r'(\d+)[^\d]*C', line)
                if temp_match:
                    temperature = int(temp_match.group(1))
                else:
                    continue  # Skip if no temperature found

                # Extract mu (μ) value
                mu_match = re.search(r'μ = ([\d\.]+)', line)
                if mu_match:
                    mu_value = float(mu_match.group(1))
                else:
                    continue  # Skip if no μ value found
                
                # Extract group identifier (e.g., _2Ikrum Re)
                group_match = re.search(r'_\d+Ikrum\sRe|_\d+Ikrum\sRT', line)
                if group_match:
                    group_key = group_match.group(0).strip()
                else:
                    continue  # Skip if no group identifier found
                
                # Capture the 20°C μ value for each group
                if temperature == reference_temperature:
                    grouped_data[group_key]['mu_20'] = mu_value  # Save μ_20 for this group

                # Store 10°C and other entries temporarily if μ_20 is missing
                if grouped_data[group_key]['mu_20'] is None:
                    pending_entries.append((group_key, temperature, mu_value))
                    continue  # Skip calculation until μ_20 is available

                # Compute Equivalent Energy & Energy Shift
                mu_20 = grouped_data[group_key]['mu_20']
                equivalent_energy = (mu_value / mu_20) * reference_energy
                energy_shift = equivalent_energy - reference_energy  # Energy shift relative to 20°C

                # Compute Relative Error (RE)
                relative_error = 100 * (mu_value - mu_20) / mu_20

                # Append data to the corresponding group
                grouped_data[group_key]['temperatures'].append(temperature)
                grouped_data[group_key]['mu'].append(mu_value)
                grouped_data[group_key]['energy'].append(equivalent_energy)
                grouped_data[group_key]['energy_shift'].append(energy_shift)
                grouped_data[group_key]['relative_error'].append(relative_error)

                # Print the energy for each mean data
                print(f"Group_Am: {group_key}, Temperature: {temperature}°C, Energy: {equivalent_energy:.2f} keV")

            except (IndexError, ValueError) as e:
                print(f"Skipping line due to error: {e}")
                continue

# Process pending entries after all 20°C values are assigned
for group_key, temperature, mu_value in pending_entries:
    if grouped_data[group_key]['mu_20'] is not None:
        mu_20 = grouped_data[group_key]['mu_20']
        equivalent_energy = (mu_value / mu_20) * reference_energy
        energy_shift = equivalent_energy - reference_energy

        # Compute Relative Error (RE)
        relative_error = 100 * (mu_value - mu_20) / mu_20

        grouped_data[group_key]['temperatures'].append(temperature)
        grouped_data[group_key]['mu'].append(mu_value)
        grouped_data[group_key]['energy'].append(equivalent_energy)
        grouped_data[group_key]['energy_shift'].append(energy_shift)
        grouped_data[group_key]['relative_error'].append(relative_error)

        # Print the energy for each mean data
        print(f"Group_Am: {group_key}, Temperature: {temperature}°C, Energy: {equivalent_energy:.2f} keV")

# Plot 1: Actual Energy vs Ikrum Group
plt.figure(figsize=(12, 6))
unique_temperatures = sorted(set(t for data in grouped_data.values() for t in data['temperatures']))
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_temperatures)))
ikrum_groups = list(grouped_data.keys())
ikrum_to_numeric = {ikrum: idx for idx, ikrum in enumerate(ikrum_groups, start=1)}

for group, data in grouped_data.items():
    group_numeric = ikrum_to_numeric[group]
    for i, temperature in enumerate(data['temperatures']):
        offset = (i - (len(data['temperatures']) - 1) / 2) * 0.2  

        temp_color = colors[unique_temperatures.index(temperature)]

        label = f'Temperature: {temperature}°C'
        plt.scatter(group_numeric + offset, data['energy'][i], color=temp_color, label=label, s=80, edgecolors='black')

    # Ensure unique labels for the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = {}
    for handle, label in zip(handles, labels):
        unique_labels[label] = handle

plt.legend(unique_labels.values(), [f'Temperature: {t}°C' for t in unique_temperatures], title="Temperature (°C)")

plt.title('Mean Energy vs Ikrum Group')
plt.xlabel('Ikrum Group')
plt.ylabel('Energy (keV)')
plt.xticks(ticks=np.arange(1, len(ikrum_groups) + 1), labels=ikrum_groups)
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
