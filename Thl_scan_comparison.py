import matplotlib.pyplot as plt
import glob
import numpy as np
import re
from scipy.optimize import curve_fit
from scipy.special import erf

# Gaussian function
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Error function (scaled CDF of Gaussian)
def error_function(x, A, mu, sigma):
    return A * (1 + erf((x - mu) / (np.sqrt(2) * sigma))) / 2

def plot_threshold_vs_pixel_count(file_paths_dict, plot_gaussian_only=False):
    # Create a figure for the first plot
    plt.figure(figsize=(10, 6))
    
    for temperature, file_paths in file_paths_dict.items():
        threshold_values = []
        hits_values = []
        
        # Loop to read data from files for each temperature
        for file_path in file_paths:
            try:
                # Open the file and extract the threshold from the 9th line
                with open(file_path, 'r') as file:
                    lines = file.readlines()

                    # Extract threshold from the 9th line
                    threshold_line = lines[8]
                    match = re.search(r'#\s*THL\s*=\s*(\d+)', threshold_line)
                    if match:
                        threshold = int(match.group(1))
                    else:
                        print(f"Could not find threshold in file: {file_path}")
                        continue

                    #     # Process data from the 39th line onward
                    # data = []
                    # for line in lines[38:]:
                    #     if line.startswith('#'):  # Stop if line starts with '#'
                    #         break
                    #     values = line.split()
                    #     if len(values) >= 3:  # Ensure there are at least three columns
                    #         data.append(float(values[2]))  # Extract third column

                    # hits = sum(data)  # Summing third column values as hits
                    # Extract hits from the last line
                    last_line = lines[-1]
                    match_hits = re.search(r'Hits:\s*(\d+)', last_line)
                    if match_hits:
                        hits = int(match_hits.group(1))
                    else:
                        print(f"Could not find hits in file: {file_path}")
                        continue

                    # Append extracted values
                    threshold_values.append(threshold)
                    hits_values.append(hits)

            except (IndexError, ValueError, IOError) as e:
                print(f"Skipping file with error: {file_path} ({e})")
                continue
        
        # Sort the values for better plotting
        sorted_indices = np.argsort(threshold_values)
        threshold_values = np.array(threshold_values)[sorted_indices]
        hits_values = np.array(hits_values)[sorted_indices]

        # Check if data is available
        if len(threshold_values) < 2 or len(hits_values) < 2:
            print(f"Insufficient data for {temperature}°C.")
            continue
        
        if plot_gaussian_only:
            # Fit and plot only the Gaussian fit (second plot)
            try:
                # Compute the derivative of the fitted error function for Gaussian fitting
                p0_err = [max(hits_values), np.mean(threshold_values), 100]  # Initial guess for error function
                popt_err, _ = curve_fit(error_function, threshold_values, hits_values, p0=p0_err, maxfev=10000)
                x_fit = np.linspace(min(threshold_values), max(threshold_values), 1000)
                y_fit_err = error_function(x_fit, *popt_err)

                # Compute the derivative of the error function
                dy_dx = np.gradient(y_fit_err, x_fit)

                # Gaussian fit from the derivative
                peak_index = np.argmax(dy_dx)  # Find where the slope is steepest
                A_init = max(dy_dx)
                mu_init = x_fit[peak_index]
                sigma_init = (max(threshold_values) - min(threshold_values)) / 20  # Narrower guess
                p0_gauss = [A_init, mu_init, sigma_init]

                # Perform Gaussian fitting
                bounds = (
                    [0, min(threshold_values), 1],  # Lower bounds: Amplitude >= 0, sigma > 1
                    [2 * A_init, max(threshold_values), (max(threshold_values) - min(threshold_values)) / 5]  # Upper bounds
                )
                popt_gauss, _ = curve_fit(gaussian, x_fit, dy_dx, p0=p0_gauss, bounds=bounds, maxfev=5000)
                y_fit_gauss = gaussian(x_fit, *popt_gauss)

                # Extract mean and sigma from the fit parameters
                A_gauss, mu_gauss, sigma_gauss = popt_gauss

                # Plot Gaussian fit for this temperature
                plt.plot(x_fit, y_fit_gauss, '-', label=f'{temperature}°C - Gaussian Fit\nμ={mu_gauss:.2f}, σ={sigma_gauss:.2f}')

            except Exception as e:
                print(f"Fitting failed for {temperature}°C: {e}")
        
        else:
            # Plot both raw data and Gaussian fit (first plot)
            plt.plot(threshold_values, hits_values, 'o-', label=f'{temperature}°C - Event Counts (Raw Data)')

            try:
                # Error function fitting
                p0_err = [max(hits_values), np.mean(threshold_values), 100]  # Initial guess
                popt_err, _ = curve_fit(error_function, threshold_values, hits_values, p0=p0_err, maxfev=10000)
                x_fit = np.linspace(min(threshold_values), max(threshold_values), 1000)
                y_fit_err = error_function(x_fit, *popt_err)
                plt.plot(x_fit, y_fit_err, label=f'{temperature}°C - Error Function Fit')

                # Compute the derivative of the fitted error function
                dy_dx = np.gradient(y_fit_err, x_fit)

                # Initial guess for Gaussian fit based on derivative analysis
                peak_index = np.argmax(dy_dx)  # Find where the slope is steepest
                A_init = max(dy_dx)
                mu_init = x_fit[peak_index]
                sigma_init = (max(threshold_values) - min(threshold_values)) / 20  # Narrower guess
                p0_gauss = [A_init, mu_init, sigma_init]

                # Perform Gaussian fitting
                popt_gauss, _ = curve_fit(gaussian, x_fit, dy_dx, p0=p0_gauss, bounds=bounds)
                y_fit_gauss = gaussian(x_fit, *popt_gauss)

                # Extract mean and sigma from the fit parameters
                A_gauss, mu_gauss, sigma_gauss = popt_gauss

                # Plot Gaussian fit on the same graph
                plt.plot(x_fit, y_fit_gauss, '--', label=f'{temperature}°C - Gaussian Fit\nμ={mu_gauss:.2f}, σ={sigma_gauss:.2f}')

            except Exception as e:
                print(f"Fitting failed for {temperature}°C: {e}")

    # Finalize and show the first plot
    plt.xlabel('Threshold Value')
    plt.ylabel('Event Count')
    plt.title('Threshold Scan with Re Equ. data(Zr)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Define file paths for 10°C, 20°C, and 40°C
# Define the file paths for three different sets of files
file_paths_10C = glob.glob(r'D:\Elavenil\Miun\Phase 6\Threshold scan\Cu_10_2_RT_*.txt')
file_paths_20C = glob.glob(r'D:\Elavenil\Miun\Phase 6\Threshold scan\Cu_10_5_RT_*.txt')
file_paths_40C = glob.glob(r'D:\Elavenil\Miun\Phase 6\Threshold scan\Cu_10_10_RT_*.txt')

# Dictionary of file paths for each temperature
file_paths_dict = {
    '10°C': file_paths_10C,
    '20°C': file_paths_20C,
    '45°C': file_paths_40C
}

# Run the function to show both plots
plot_threshold_vs_pixel_count(file_paths_dict, plot_gaussian_only=True)
