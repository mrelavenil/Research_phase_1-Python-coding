import pandas as pd

# File paths
spectrum_file_path = r'D:\Elavenil\Miun\Phase 6\Text files\Thresholdscan\Energy for AgMean.txt'
slope_intercept_file_path = r'D:\Elavenil\Miun\Phase 6\Text files\slope_intercept_results_thresholdscan.txt'

# Function to parse the spectrum energy file
def parse_spectrum_file(file_path):
    ikrum_data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Find the relevant parts in the line
            parts = line.split('Actual Energy = ')
            if len(parts) > 1:
                ikrum_info = parts[0].split(',')[0].strip()  # Extract Ikrum info
                temperature = int(parts[0].split(',')[1].strip())  # Extract Temperature
                actual_energy = float(parts[1].split('KeV')[0].strip())  # Extract Actual Energy
                ikrum_data.append((ikrum_info, temperature, actual_energy))
                
    return ikrum_data

# Function to parse the slope-intercept file
def parse_slope_intercept_file(file_path):
    slope_intercept_data = {}
    
    with open(file_path, 'r', encoding='ISO-8859-1') as file:  # Changed encoding
        # Skip the header line
        next(file)
        
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 4:
                ikrum = parts[0].strip()
                temperature = int(parts[1].strip())
                slope = float(parts[2].strip())
                intercept = float(parts[3].strip())  # We will use slope and intercept
                
                # Store slope and intercept by Ikrum and Temperature
                slope_intercept_data[(ikrum, temperature)] = (slope, intercept)
    
    return slope_intercept_data


# Parse the spectrum file
spectrum_data = parse_spectrum_file(spectrum_file_path)

# Parse the slope-intercept file
slope_intercept_data = parse_slope_intercept_file(slope_intercept_file_path)

# Calculate and print the corrected energies
for ikrum_info, temperature, actual_energy in spectrum_data:
    # Check if the (ikrum, temperature) pair exists in the slope-intercept data
    if (ikrum_info, temperature) in slope_intercept_data:
        slope, intercept = slope_intercept_data[(ikrum_info, temperature)]
        
        # Calculate the corrected energy using the formula y = mx + c
        corrected_energy = (slope * actual_energy) + intercept
        
        print(f"Ikrum: {ikrum_info}, Temperature: {temperature}°C, Actual Energy: {actual_energy:.4f} keV, Corrected Energy: {corrected_energy:.4f} keV")
