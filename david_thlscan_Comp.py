import matplotlib.pyplot as plt
import glob
import numpy as np
import re
from scipy.interpolate import interp1d
from lmfit.models import StepModel, LinearModel

def process_and_analyze(file_paths, label):
    threshold_values = []
    hits_values = []

    # Loop to read data from files
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
            
            # Extract threshold from the 9th line
            threshold_line = lines[8]
            match = re.search(r'#\s*THL\s*=\s*(\d+)', threshold_line)
            if match and 850<= int(match.group(1)) <=990:
            # if match and 1250<= int(match.group(1)) <=1380:
                threshold = int(match.group(1))
            else:
                continue

            # Process data from the 39th line onward
            data = []
            for line in lines[38:]:
                if line.startswith('#'):  # Stop if line starts with '#'
                    break
                values = line.split()
                if len(values) >= 3:  # Ensure there are at least three columns
                    data.append(float(values[2]))  # Extract third column

            hits = sum(data)  # Summing third column values as hits

            # Append extracted values
            threshold_values.append(threshold)
            hits_values.append(hits)

        except (IndexError, ValueError, IOError) as e:
            print(f"Skipping file with error: {file_path} ({e})")
            continue

    # Convert to numpy arrays for further processing
    threshold_np = np.array(threshold_values)
    hits_np = np.array(hits_values)

    # Check if data was extracted successfully
    if len(threshold_np) == 0 or len(hits_np) == 0:
        print("No data extracted. Please check the file paths or file contents.")
        return None

    # Sorting the data to ensure proper fitting
    sorted_indices = np.argsort(threshold_np)
    x = threshold_np[sorted_indices]
    y = hits_np[sorted_indices]

    # Step and Linear Model
    step_mod = StepModel(form='erf', prefix='step_')
    line_mod = LinearModel(prefix='line_')

    pars = line_mod.make_params(intercept=y.min(), slope=1)
    pars += step_mod.guess(y, x=x)

    mod = step_mod + line_mod
    out = mod.fit(y, pars, x=x)

    # Differentiated data (using the original x and y)
    y_diff = np.diff(y)
    x_diff = x[1:]

    # Remove duplicates in x_diff while keeping corresponding y_diff values
    x_diff, indices = np.unique(x_diff, return_index=True)
    y_diff = y_diff[indices]

    # Perform cubic interpolation on the differentiated data
    cubic_interp = interp1d(x_diff, y_diff, kind='cubic')  # Cubic interpolation
    fine_x = np.linspace(x_diff.min(), x_diff.max(), 1000)  # Generate a finer grid
    fine_y_diff = cubic_interp(fine_x)  # Interpolated values

    # Identify the peak region in interpolated data
    peak_indices = np.where(fine_y_diff > 0.5 * fine_y_diff.max())[0]
    peak_x = fine_x[peak_indices]
    peak_y_diff = fine_y_diff[peak_indices]

    # Calculate mean and sigma for the interpolated peak region
    mean_peak = np.mean(peak_x)
    sigma_peak = np.std(peak_x)

    # Calculate FWHM of the peak
    half_max = fine_y_diff.max() / 2
    indices_above_half_max = np.where(fine_y_diff >= half_max)[0]
    fwhm = fine_x[indices_above_half_max[-1]] - fine_x[indices_above_half_max[0]]

    return fine_x, fine_y_diff, peak_x, peak_y_diff, mean_peak, sigma_peak, fwhm, label


# Define the file paths for three different sets of files
file_paths_set_1 = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\10_2_*.txt')
file_paths_set_2 = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\10_5_*.txt')
file_paths_set_3 = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\10_10_*.txt')
file_paths_set_4 = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\10_15_*.txt')
file_paths_set_5 = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\10_50_*.txt')


# Energy (in keV) corresponding to a threshold range, assuming a linear relationship.
mean_energy =22.1# This is the center energy in keV.

# Process and analyze each dataset as in your existing code
results_set_1 = process_and_analyze(file_paths_set_1, label="2Ikrum")
results_set_2 = process_and_analyze(file_paths_set_2, label="5Ikrum")
results_set_3 = process_and_analyze(file_paths_set_3, label="10Ikrum")
results_set_4 = process_and_analyze(file_paths_set_4, label="15Ikrum")
results_set_5 = process_and_analyze(file_paths_set_5, label="50Ikrum")

# Check if all results are valid
if None in [results_set_1, results_set_2, results_set_3, results_set_4, results_set_5]:
    print("Error: One or more datasets failed to process. Exiting.")
    exit()

# Extract results for plotting
datasets = [results_set_1, results_set_2, results_set_3, results_set_4, results_set_5]

# Print mean, sigma, FWHM, and energy resolution for each dataset
for data in datasets:
    fine_x, fine_y_diff, peak_x, peak_y_diff, mean_peak, sigma_peak, fwhm, label = data

    # Calculate energy resolution based on FWHM and known mean energy (15.7 keV)
    energy_resolution = (fwhm / mean_energy) * 100  # Resolution in percentage

    # Print the results
    print(f"{label}: μ = {mean_peak:.2f}, σ = {sigma_peak:.2f}, FWHM = {fwhm:.2f} keV, Energy Resolution = {energy_resolution:.2f}%")


# Plot the comparison graph (same as in your code)
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
colors = ['blue', 'orange', 'green', 'purple', 'red']

for data, color in zip(datasets, colors):
    fine_x, fine_y_diff, peak_x, peak_y_diff, mean_peak, sigma_peak, fwhm, label = data
    ax.plot(fine_x, fine_y_diff, color=color, label=f'{label}.\nMean: {mean_peak:.2f}, Sigma: {sigma_peak:.2f}, FWHM: {fwhm:.2f}')
    ax.scatter(peak_x, peak_y_diff, color=color, alpha=0.6)

# Customize plot
ax.set_xlabel('Threshold')
ax.set_ylabel('Differentiated Hits')
ax.set_title('Threshold Scans of Cu at 100 degrees Re-Equ with different Ikrums')
ax.legend(loc='upper left')
plt.grid()

# Plot only the interpolated peak areas for comparison
fig, ax = plt.subplots(1, 1, figsize=(10, 8))
colors = ['blue', 'orange', 'green', 'purple', 'red']

for data, color in zip(datasets, colors):
    _, _, peak_x, peak_y_diff, mean_peak, sigma_peak, fwhm, label = data
    ax.plot(peak_x, peak_y_diff, color=color, label=f'{label}.\nMean: {mean_peak:.2f}, Sigma: {sigma_peak:.2f}, FWHM: {fwhm:.2f}')
    ax.scatter(peak_x, peak_y_diff, color=color, alpha=0.6)

# Customize plot
ax.set_xlabel('Threshold')
ax.set_ylabel('Differentiated Hits')
ax.set_title('Interpolated Peak Region Comparison(Mo@ 40 Degree-RT-Equ)')
plt.xlim(800, 1000)
ax.legend(loc='upper left')
plt.grid()

# Show the plot
plt.show()
