import matplotlib.pyplot as plt
import re
from collections import defaultdict
import numpy as np

# List of text files to process
file_paths = [
    r'D:\Elavenil\Miun\Phase 6\Text files\Thresholdscan\Cu threshold scan.txt',
]

# Dictionary to store grouped data
grouped_data = defaultdict(lambda: {'temperatures': [], 'mu': [], 'sigma': [], 'energy': [], 'mu_20': None, 'sigma_20': None, 'energy_shift': [], 'relative_error': [], 'fwhm': [], 'resolution': []})

reference_energy = 8.04  # keV for 20°C μ value
reference_temperature = 20  # °C
pending_entries = []  # Store entries if μ_20 or σ_20 is missing initially

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
                
                # Extract group identifier (e.g., _2Ikrum Re)
                group_match = re.search(r'_\d+Ikrum\sRe|_\d+Ikrum\sRT', line)
                if group_match:
                    group_key = group_match.group(0).strip()
                else:
                    continue  # Skip if no group identifier found
                
                # Capture the 20°C μ and σ values for each group
                if temperature == reference_temperature:
                    grouped_data[group_key]['mu_20'] = mu_value  # Save μ_20 for this group
                    grouped_data[group_key]['sigma_20'] = sigma_value  # Save σ_20 for this group

                # Store 10°C and other entries temporarily if μ_20 or σ_20 is missing
                if grouped_data[group_key]['mu_20'] is None or grouped_data[group_key]['sigma_20'] is None:
                    pending_entries.append((group_key, temperature, mu_value, sigma_value))
                    continue  # Skip calculation until μ_20 and σ_20 are available

                # Compute Equivalent Energy for mu
                mu_20 = grouped_data[group_key]['mu_20']
                sigma_20 = grouped_data[group_key]['sigma_20']
                equivalent_energy_mu = (mu_value / mu_20) * reference_energy
                
                # Compute Equivalent Energy for sigma
                equivalent_energy_sigma = (sigma_value / sigma_20) * reference_energy
                
                # Energy shift for mu and sigma
                energy_shift_mu = equivalent_energy_mu - reference_energy  # Energy shift relative to 20°C
                energy_shift_sigma = equivalent_energy_sigma - reference_energy  # Energy shift relative to 20°C

                # Compute Relative Error (RE) for mu
                relative_error = 100 * (mu_value - mu_20) / mu_20

                # FWHM is approximated as 2.355 * sigma for Gaussian distribution
                fwhm = 2.355 * sigma_value  # FWHM in terms of sigma

                # Energy Resolution calculation
                resolution = (fwhm / mu_value) * 100 if mu_value != 0 else 0

                # Append data to the corresponding group
                grouped_data[group_key]['temperatures'].append(temperature)
                grouped_data[group_key]['mu'].append(mu_value)
                grouped_data[group_key]['sigma'].append(sigma_value)
                grouped_data[group_key]['energy'].append(equivalent_energy_mu)
                grouped_data[group_key]['energy_shift'].append(energy_shift_mu)
                grouped_data[group_key]['relative_error'].append(relative_error)
                grouped_data[group_key]['fwhm'].append(fwhm)
                grouped_data[group_key]['resolution'].append(resolution)

            except (IndexError, ValueError) as e:
                print(f"Skipping line due to error: {e}")
                continue

# Process pending entries after all 20°C values are assigned
for group_key, temperature, mu_value, sigma_value in pending_entries:
    if grouped_data[group_key]['mu_20'] is not None and grouped_data[group_key]['sigma_20'] is not None:
        mu_20 = grouped_data[group_key]['mu_20']
        sigma_20 = grouped_data[group_key]['sigma_20']
        equivalent_energy_mu = (mu_value / mu_20) * reference_energy
        equivalent_energy_sigma = (sigma_value / sigma_20) * reference_energy
        
        # Energy shift for mu and sigma
        energy_shift_mu = equivalent_energy_mu - reference_energy
        energy_shift_sigma = equivalent_energy_sigma - reference_energy

        # Compute Relative Error (RE) for mu
        relative_error = 100 * (mu_value - mu_20) / mu_20

        # FWHM is approximated as 2.355 * sigma for Gaussian distribution
        fwhm = 2.355 * sigma_value

        # Energy Resolution calculation
        resolution = (fwhm / mu_value) * 100 if mu_value != 0 else 0

        grouped_data[group_key]['temperatures'].append(temperature)
        grouped_data[group_key]['mu'].append(mu_value)
        grouped_data[group_key]['sigma'].append(sigma_value)
        grouped_data[group_key]['energy'].append(equivalent_energy_mu)
        grouped_data[group_key]['energy_shift'].append(energy_shift_mu)
        grouped_data[group_key]['relative_error'].append(relative_error)
        grouped_data[group_key]['fwhm'].append(fwhm)
        grouped_data[group_key]['resolution'].append(resolution)

# Print the formatted results for each group
for group_key, data in grouped_data.items():
    # Loop through the temperatures in the group
    for i in range(len(data['temperatures'])):
        temperature = data['temperatures'][i]
        energy_shift_mu = data['energy_shift'][i]
        relative_error = data['relative_error'][i]
        resolution = data['resolution'][i]
        
        # Format the values to the required precision
        energy_shift_mu_formatted = f"{energy_shift_mu:.4f}"  # 4 decimal places for mu energy shift
        resolution_formatted = f"{resolution:.2f}"  # 2 decimal places for resolution
        relative_error_formatted = f"{relative_error:.2f}"  # 2 decimal places for relative error
        
        # Print the formatted line
        print(f"Group_Cu: {group_key}, Temperature: {temperature}°C, Absolute Shift: {energy_shift_mu_formatted} keV, Relative Error: {relative_error_formatted}%, Energy Resolution = {resolution_formatted}%")
