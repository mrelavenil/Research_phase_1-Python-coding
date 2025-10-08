import matplotlib.pyplot as plt
import re
from lmfit.models import LinearModel
import numpy as np

# Given x-values (Energy) for Cu, Zr, Mo
x = [8.04, 15.7, 17.5]  # Energy values corresponding to Cu, Zr, Mo

# Function to extract TOT values
def extract_data(file_name):
    extracted_data = []

    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # Extract the label (IKrum group) and numerical values
            match = re.match(r"([\w°C_\- ]+): \[.*\], \[([\d\.,\s]+)\]", line)
            
            if match:
                label = match.group(1).strip()  # Extract IKrumm group
                values = [float(val.strip()) for val in match.group(2).split(',') if val.strip()]
                
                if len(values) == 4:  # Adjusted to handle lines with 4 values
                    extracted_data.append((label, values[:3], values[3]))  # Store label, first 3 values, and fourth TOT
                else:
                    print(f"Skipping line: {line.strip()} (Found {len(values)} values instead of 4)")  # Debugging
    
    return extracted_data

# Extract TOT values from file
file_path = r'D:\Elavenil\Miun\Phase 6\Text files\Thresholdscan\Mean (Threshold) values for [Cu, Zr Mo Ag].txt'
data = extract_data(file_path)

# Check if data was found
if not data:
    print("No valid data found in the file. Please check the file format or encoding.")
else:
    plt.figure(figsize=(8, 6))  # Set figure size
    
    for idx, (label, y_values, unknown_tot) in enumerate(data):
        # Fit a linear model
        linear_model = LinearModel()
        params = linear_model.make_params()
        result = linear_model.fit(y_values, params, x=x)

        # Predict energy for the unknown TOT value
        slope = result.best_values['slope']
        intercept = result.best_values['intercept']
        predicted_energy = (unknown_tot - intercept) / slope

        print(f"{label}: Mean TOT = {unknown_tot:.2f}, Predicted Energy = {predicted_energy:.2f} eV")

        # Plot the original data
        plt.plot(x, y_values, 'ko-', label=f'{label}')

        # Plot the fitted line
        extended_x = np.linspace(min(x), max(x) + 10, 100)  # Smooth extension
        extended_y = result.eval(x=extended_x)
        plt.plot(extended_x, extended_y, 'r--', label=f'Fit {idx+1}')

        # Plot the predicted point for the unknown TOT value
        plt.scatter(predicted_energy, unknown_tot, color='blue', marker='x', s=100, label=f'Predicted Energy {idx+1}')

    # Labels and title
    plt.xlabel('Energy')
    plt.ylabel('TOT')
    plt.title('Energy Calibration with Linear Fit')
    plt.legend()
    plt.grid(True)

    # Show the plot
    plt.show()
