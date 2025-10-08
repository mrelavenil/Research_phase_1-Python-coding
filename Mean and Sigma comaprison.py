import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np

# List of text files to process
file_paths = [
    r'D:\Elavenil\Miun\Phase 6\Text files\Cu spectrum.txt',
    #r'D:\Elavenil\Miun\Phase 6\Text files\Zr spectrum.txt',
     #r'D:\Elavenil\Miun\Phase 6\Text files\Zr threshold scan.txt'
]

# Dictionary to store grouped data by unique identifiers
grouped_data = defaultdict(lambda: {'temperatures': [], 'mu': [], 'sigma': []})

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
                
                # Extract sigma (σ) value
                sigma_match = re.search(r'σ = ([\d\.]+)', line)
                if sigma_match:
                    sigma_value = float(sigma_match.group(1))
                else:
                    continue  # Skip if no σ value found
                
                # Extract group identifier (e.g., _5Ikrum Re)
                group_match = re.search(r'_\d+Ikrum\sRe|_\d+Ikrum\sRT', line)
                if group_match:
                    group_key = group_match.group(0).strip()
                else:
                    continue  # Skip if no group identifier found

                # Append data to the corresponding group
                grouped_data[group_key]['temperatures'].append(temperature)
                grouped_data[group_key]['mu'].append(mu_value)
                grouped_data[group_key]['sigma'].append(sigma_value)

            except (IndexError, ValueError) as e:
                print(f"Skipping line due to error: {e}")
                continue

# Check if data was extracted
if grouped_data:
    plt.figure(figsize=(12, 6))
    
    # Define color map to differentiate temperatures
    unique_temperatures = sorted(set(t for data in grouped_data.values() for t in data['temperatures']))
    colors = plt.cm.viridis(np.linspace(0, 1, len(unique_temperatures)))
    
    # Map Ikrum groups to numeric x-axis values
    ikrum_groups = list(grouped_data.keys())
    ikrum_to_numeric = {ikrum: idx for idx, ikrum in enumerate(ikrum_groups, start=1)}

    # Plotting for each group (Ikrum value)
    for group, data in grouped_data.items():
        group_numeric = ikrum_to_numeric[group]  # Use numeric value for x-axis
        for i, temperature in enumerate(data['temperatures']):
            # Slight offset to separate points at each x (Ikrum group)
            offset = (i - (len(data['temperatures']) - 1) / 2) * 0.2  # Adjust this value for spacing
            
            # Find the color corresponding to this temperature
            temp_color = colors[unique_temperatures.index(temperature)]
            
            # Plot Mu (μ) values as the y-data and Sigma (σ) as error bars centered at Mu
            label = f'Temperature: {temperature}°C'
            plt.errorbar(group_numeric + offset, data['mu'][i], yerr=data['sigma'][i], fmt='o', color=temp_color,
                         label=label, capsize=5, xerr=0, elinewidth=1, markersize=8)

    # Ensure unique labels for the legend
    handles, labels = plt.gca().get_legend_handles_labels()
    unique_labels = {}
    for handle, label in zip(handles, labels):
        unique_labels[label] = handle

    # Plot the legend with all temperatures
    plt.legend(unique_labels.values(), unique_labels.keys(), title="Temperature (°C)")

    # Set title and labels
    plt.title('Cu Spectrum mean and sigma comparison')
    plt.xlabel('Ikrum Group')
    plt.ylabel('TOT')
    plt.xticks(ticks=np.arange(1, len(ikrum_groups) + 1), labels=ikrum_groups)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
else:
    print("No valid data extracted for plotting.")
