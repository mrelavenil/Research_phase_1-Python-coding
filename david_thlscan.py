import matplotlib.pyplot as plt
import glob
import numpy as np
import re
from scipy.interpolate import interp1d
from lmfit.models import StepModel, LinearModel

def plot_threshold_vs_pixel_count(file_paths):
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
            if match and 800 <= int(match.group(1)) <= 992:
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
        return
    
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

    mean_energy =22.1

    # Calculate energy resolution based on FWHM and known mean energy (15.7 keV)
    energy_resolution = (fwhm / mean_energy) * 100  # Resolution in percentage

        # Print the results
    print(f" μ = {mean_peak:.2f}, σ = {sigma_peak:.2f}, FWHM = {fwhm:.2f} keV, Energy Resolution = {energy_resolution:.2f}%")

    # Plot: All Data + Step and Linear Fit + Differentiated Data
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.plot(x, y, 'ko', label='Hits (Data)')
    # ax.plot(x, out.best_fit, 'r-', label='Step + Linear Best Fit')
    # ax.plot(x, out.init_fit, 'b--', label='Step + Linear Init Fit')
    ax.plot(fine_x, fine_y_diff, 'g-', label='Cubic Interpolation of Differentiated Data')
    ax.scatter(peak_x, peak_y_diff, color='orange', label=f'Peak Region\nMean: {mean_peak:.2f}, Sigma: {sigma_peak:.2f}, FWHM: {fwhm:.2f}', zorder=5)

    # Customize Plot
    ax.set_xlabel('Threshold')
    ax.set_ylabel('Hits / Differentiated Hits')
    ax.set_title('Threshold Scan With Ag @20°C')
    ax.legend(loc='upper left')
    plt.grid()

    # Show the plot
    plt.show()

# Define file paths
combined_file_paths = glob.glob(r'D:\Elavenil\Miun\Phase 6\Ag data\40_50*.txt')
combined_file_paths.sort()

# Run the function

plot_threshold_vs_pixel_count(combined_file_paths)
