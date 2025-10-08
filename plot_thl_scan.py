import matplotlib.pyplot as plt
import glob
import numpy as np
import re
from scipy.optimize import curve_fit
from scipy.special import erf
from scipy.signal import savgol_filter, find_peaks

# Gaussian function
def gaussian(x, A, mu, sigma):
    return A * np.exp(-(x - mu)**2 / (2 * sigma**2))

# Error function
def error_function(x, A, mu, sigma):
    return A * (1 + erf((x - mu) / (np.sqrt(2) * sigma))) / 2

def plot_threshold_vs_pixel_count(file_paths):
    threshold_values = []
    hits_values = []
    
    # Loop to read data from files
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
        print("Insufficient data to plot or perform Gaussian fitting.")
        return

    # Calculate the difference in event counts
    diff_pixel_counts = np.diff(hits_values)
    
    # Smooth the derivative using Savitzky-Golay filter
    window_length = min(len(diff_pixel_counts) - 1, 51)  # Ensure the window size is appropriate
    if window_length % 2 == 0:
        window_length += 1  # Ensure window_length is odd
    diff_pixel_counts_smooth = savgol_filter(diff_pixel_counts, window_length=window_length, polyorder=2)

    # Plot raw data (Threshold vs Event Counts)
    plt.figure(figsize=(10, 6))
    plt.plot(threshold_values, hits_values, 'o-', color='blue', label='Event Counts')
    plt.xlabel('Threshold Value')
    plt.ylabel('Event Count')
    #plt.xlim(1300,1350)
    plt.title('Threshold Scan')
    
    # Fit the raw data using the error function
    try:
        p0_err = [max(hits_values), np.mean(threshold_values), 100]  # Initial guess
        popt_err, _ = curve_fit(error_function, threshold_values, hits_values, p0=p0_err, maxfev=10000)
        x_fit = np.linspace(min(threshold_values), max(threshold_values), 1000)
        y_fit_err = error_function(x_fit, *popt_err)
        plt.plot(x_fit, y_fit_err, 'r-', label='Error Function Fit')
    except Exception as e:
        print(f"Error function fitting failed: {e}")
    
    plt.legend()
   # plt.xlim(1300,1350)
    plt.grid(True)
    plt.show()

    # Plot smoothed derivative (Increase in Event Counts)
    plt.figure(figsize=(10, 6))
    plt.plot(threshold_values[1:], diff_pixel_counts_smooth, 'o-', color='green', label='Smoothed Increase in Event Counts')
    plt.xlabel('Threshold Value')
    plt.ylabel('Increase in Event Count (Smoothed)')
    #plt.xlim(1300,1350)
    plt.title('Threshold Scan - Derivative')

    # Find peaks in the smoothed derivative
    peaks, _ = find_peaks(diff_pixel_counts_smooth)
    if len(peaks) > 0:
        peak_index = peaks[np.argmax(diff_pixel_counts_smooth[peaks])]
        mu_init = threshold_values[1:][peak_index]  # Use the position of the peak
    else:
        print("No significant peaks detected, using maximum value as initial guess.")
        mu_init = threshold_values[1:][np.argmax(diff_pixel_counts_smooth)]
    
    # Initial guess for Gaussian fit
    A_init = max(diff_pixel_counts_smooth)
    sigma_init = (max(threshold_values) - min(threshold_values)) / 10

    # Set bounds for fitting
    sigma_max = max(10, (max(threshold_values) - min(threshold_values)) / 4)
    bounds = ([0, min(threshold_values), 1], [2 * A_init, max(threshold_values), sigma_max])
    p0_gauss = [A_init, mu_init, sigma_init]

    # Perform Gaussian fitting
    try:
        popt_gauss, _ = curve_fit(
            gaussian, 
            threshold_values[1:], 
            diff_pixel_counts_smooth, 
            p0=p0_gauss, 
            bounds=bounds, 
            maxfev=10000
        )
        
        # Plot Gaussian fit
        x_fit_gauss = np.linspace(min(threshold_values), max(threshold_values), 1000)
        y_fit_gauss = gaussian(x_fit_gauss, *popt_gauss)
        plt.plot(x_fit_gauss, y_fit_gauss, 'r-', label='Gaussian Fit')
        
        # Mark the peak
        mu_mean = popt_gauss[1]
        sigma_mean = popt_gauss[2]
        plt.scatter(mu_mean, gaussian(mu_mean, *popt_gauss), color='gray', zorder=10)
        plt.axvline(mu_mean, color='red', linestyle='--', label=f'Mean: {mu_mean:.2f}')
        plt.text(0.05, 0.9, f'Mean: {mu_mean:.2f}\nSigma: {sigma_mean:.2f}', transform=plt.gca().transAxes)
    
    except Exception as e:
        print(f"Gaussian fitting failed on smoothed derivative data: {e}")

    plt.legend()
    plt.grid(True)
    #plt.xlim(1300,1350)
    plt.show()

# Define file paths
combined_file_paths =  glob.glob(r'D:\Elavenil\Miun\Phase 6\Threshold scan\test\Mo_40_2_RT_*.txt')  # Example file paths
combined_file_paths.sort()

# Run the function
plot_threshold_vs_pixel_count(combined_file_paths)
