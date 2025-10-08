import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Define the 
# Gaussian function for single peak fitting
def gaussian(E, A, mu, sigma):
    return A * np.exp(-((E - mu) ** 2) / (2 * sigma ** 2))

# Define the Double Gaussian function
def double_gaussian(E, A1, mu1, sigma1, A2, mu2, sigma2):
    gaussian1 = A1 * np.exp(-((E - mu1) ** 2) / (2 * sigma1 ** 2))
    gaussian2 = A2 * np.exp(-((E - mu2) ** 2) / (2 * sigma2 ** 2))
    return gaussian1 + gaussian2

# List of file paths, temperatures for labeling, and colors for each fit
files = [
    (r'D:\Elavenil\Miun\Phase 6\Ag data\10_15Ikrum_spectrum.txt', '15', 'blue'),
    (r'D:\Elavenil\Miun\Phase 6\Ag data\10_5Ikrum_spectrum.txt', '5', 'orange'),
    (r'D:\Elavenil\Miun\Phase 6\Ag data\10_10Ikrum_spectrum.txt', '10', 'green'),
    (r'D:\Elavenil\Miun\Phase 6\Ag data\10_2Ikrum_spectrum.txt', '2', 'red'),
    (r'D:\Elavenil\Miun\Phase 6\Ag data\10_50Ikrum_spectrum.txt', '50', 'black')
]

# Plot all datasets on the same figure
plt.figure(figsize=(10, 6))

for file_path, temperature, color in files:  # Unpack three values: file_path, temperature, color
    # Read the data
    data = pd.read_csv(file_path, header=None, sep=r'\s+', comment='#')
    
    # Extract the fifth column
    fifth_column = data[3]
    
    # Plot histogram without density normalization
    counts, bins, _ = plt.hist(fifth_column, bins=100, range=(0, 100), alpha=0.3, label=f'{temperature} histogram', density=False)
    
    # Find the maximum count in the histogram
    max_count = np.max(counts)
    print(f'Maximum count for temperature {temperature}: {max_count}')
    
    # Use midpoints of bins as x data for fitting
    bin_centers = (bins[:-1] + bins[1:]) / 2

    # Initial guesses based on specified means of 11 and 18, using max count as amplitude
    initial_guess_double = [
        max(counts),  # Amplitude for the first peak
        11,           # Mean for the first peak
        5,            # Standard deviation for the first peak

        max(counts) / 2,  # Amplitude for the second peak
        25,               # Mean for the second peak
        5                 # Standard deviation for the second peak
    ]

    # Apply bounds to ensure peaks remain close to specified means
    bounds = (
        [0, 10, 1, 0, 15, 1],   # Lower bounds (allow some flexibility around means)
        [np.inf, 12, 15, np.inf, 20, 15]  # Upper bounds
    )
    
    # Fit the Double Gaussian curve to the histogram data
    try:
        popt, _ = curve_fit(double_gaussian, bin_centers, counts, p0=initial_guess_double, bounds=bounds)
    except ValueError as e:
        print(f"Error during curve fitting for {file_path}: {e}")
        continue

    # Generate Double Gaussian curve with fitted parameters if fitting was successful
    x = np.linspace(0, 40, 1000)  # Limit x to the range 0 to 40
    double_gaussian_curve = double_gaussian(x, *popt)

    # Extract fitted parameters for the legend
    A1, mu1, sigma1, A2, mu2, sigma2 = popt
    fit_label = (
        f'Nb peak: μ={mu2:.2f}, σ={sigma2:.2f}'
    )

    # Plot the Double Gaussian curve with the specified color and label
    plt.plot(x, double_gaussian_curve, color=color, label=fit_label)

# Set plot labels and title, and limit x-axis from 0 to 40
plt.xlabel('TOT')
plt.ylabel('Counts')
plt.title('Nb Spectrum with Re-Equ.data')
plt.xlim(0, 200)
plt.legend()
plt.show()
