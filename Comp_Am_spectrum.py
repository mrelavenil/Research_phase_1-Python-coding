import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Define the Gaussian function for single peak fitting
def gaussian(E, A, mu, sigma):
    return A * np.exp(-((E - mu) ** 2) / (2 * sigma ** 2))

# List of file paths, temperatures for labeling, and colors for each fit
files = [
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\40_50Ikrum_spectrum.txt','15Ikrum @10°C', 'tomato'),

    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\10_2Ik.txt', '2Ikrum @10°C', 'blue'),
    # (r'D:\Elavenil\Miun\Phase 6\Am data\20_2Ik.txt', '2Ikrum @20°C', 'lightblue'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\40_2Ik.txt', '2Ikrum @40°C', 'steelblue'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\10_5Ik.txt', '5Ikrum @10°C', 'green'),
    # (r'D:\Elavenil\Miun\Phase 6\Am data\20_5Ik.txt', '5Ikrum @20°C', 'darkgreen'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\40_5Ik.txt', '5Ikrum @40°C', 'seagreen'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\10_10Ik.txt', '10Ikrum @10°C', 'orange'),
    # (r'D:\Elavenil\Miun\Phase 6\Am data\20_10Ik.txt', '10Ikrum @20°C', 'salmon'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\40_10Ik.txt', '10Ikrum @40°C', 'lightsalmon'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\10_15Ik.txt', '15Ikrum @10°C', 'red'),
    # (r'D:\Elavenil\Miun\Phase 6\Am data\20_15Ik.txt', '15Ikrum @20°C', 'pink'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\40_15Ik.txt', '15Ikrum @40°C', 'tomato'),
     (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\10_50Ik.txt', '50Ikrum @10°C', 'purple'),
    # (r'D:\Elavenil\Miun\Phase 6\Am data\20_50Ik.txt', '50Ikrum @20°C', 'indigo'),
     (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Am data\RT\40_50Ik.txt', '50Ikrum @40°C', 'blueviolet'),
]

# Energy of the material in keV
material_energy = 22.1  # keV

# Plot all datasets on the same figure
plt.figure(figsize=(10, 6))

for file_path, temperature, color in files:
    try:
        # Read the data
        data = pd.read_csv(file_path, header=None, sep=r'\s+', comment='#')
        
        # Extract the fourth column (index 3)
        fourth_column = data[3]
        
        # Plot histogram without density normalization
        counts, bins, _ = plt.hist(fourth_column, bins=50, range=(15,50 ), alpha=0.3, density=False)
        
        # Use midpoints of bins as x data for fitting
        bin_centers = (bins[:-1] + bins[1:]) / 2

        # Ensure counts are non-zero for fitting
        if np.any(counts > 0):
            # Initial guesses for single Gaussian
            initial_guess = [max(counts), np.mean(fourth_column), np.std(fourth_column)]

            # Fit the single Gaussian curve to the histogram data
            popt, _ = curve_fit(gaussian, bin_centers, counts, p0=initial_guess, maxfev=100000)

            # Extract fitted parameters
            A, mu, sigma = popt
            
            # Calculate FWHM
            FWHM = 2.355 * sigma
            
            # Calculate Energy Resolution (%)
            energy_resolution = (FWHM / material_energy) * 100
            
            # Print FWHM and Energy Resolution
            print(f"{temperature}: μ = {mu:.2f}, σ = {sigma:.2f}, FWHM = {FWHM:.2f} keV, Energy Resolution = {energy_resolution:.2f}%")

            # Generate Gaussian curve with fitted parameters
            x = np.linspace(0, 100, 1000)
            gaussian_curve = gaussian(x, *popt)

            # Plot the Gaussian curve
            fit_label = f'{temperature} Fit: μ={mu:.2f}, σ={sigma:.2f}, FWHM={FWHM:.2f} keV'
            plt.plot(x, gaussian_curve, color=color, label=fit_label)
        else:
            print(f"No valid data for fitting in file {file_path}.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Final plot adjustments
plt.xlabel('Channel')
plt.ylabel('Counts')
plt.title('Histogram and Gaussian Fits for Am-241')
plt.legend()
plt.show()
