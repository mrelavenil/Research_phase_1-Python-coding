import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Define the Gaussian function for single peak fitting
def gaussian(E, A, mu, sigma):
    return A * np.exp(-((E - mu) ** 2) / (2 * sigma ** 2))

# List of file paths, temperatures for labeling, and colors for each fit
files = [
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_2_Re.txt', '10°C_2Ikrum Re', 'blue','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_2_RT.txt', '10°C_2Ikrum RT', 'lightblue','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_20_2.txt', '20°C_2Ikrum Re', 'black','-'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_2_Re.txt', '40°C_2Ikrum Re', 'blue','-.'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_2_RT.txt', '40°C_2Ikrum RT', 'lightblue','-.'),

    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_5_Re.txt', '10°C_5Ikrum Re', 'green','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_5_RT.txt', '10°C_5Ikrum RT', 'lightgreen','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_20_5.txt', '20°C_5Ikrum Re', 'black','-' ),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_5_Re.txt', '40°C_5Ikrum Re', 'green','-.'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_5_RT.txt', '40°C_5Ikrum RT', 'lightgreen','-.'),

    (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Zr_10_10.txt', '10°C_10Ikrum Re', 'orange','-'),
    (r'D:\Elavenil\Miun\Phase 6\Spectrum data\RT\Zr_10_10.txt', '10°C_10Ikrum RT', 'peachpuff','-'),
    (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Zr_20_10.txt', '20°C_10Ikrum Re', 'black','-'),
    (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Zr_40_10.txt', '40°C_10Ikrum Re', 'blue','-'),
    (r'D:\Elavenil\Miun\Phase 6\Spectrum data\RT\Zr_40_10.txt', '40°C_10Ikrum RT', 'green','-'),

    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Ag data\10_10Ikrum_spectrum.txt', '10°C_15Ikrum Re', 'red','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Ag data\RT\10_10Ikrum_spectrum.txt', '10°C_15Ikrum RT', 'blue','--'),
    # #(r'D:\Elavenil\Miun\Phase 6\Spectrum data\Ag data\Zr_20_15.txt', '20°C_15Ikrum Re', 'black','-'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Ag data\40_10Ikrum_spectrum.txt', '40°C_15Ikrum Re', 'green','-.'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Ag data\RT\40_10Ikrum_spectrum.txt', '40°C_15Ikrum RT', 'orange','-.'),

    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_50_Re.txt', '10°C_50Ikrum Re', 'purple','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_10_50_RT.txt', '10°C_50Ikrum RT', 'violet','--'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_20_50.txt', '20°C_50Ikrum Re', 'black','-'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_50_Re.txt', '40°C_50Ikrum Re', 'purple','-.'),
    # (r'D:\Elavenil\Miun\Phase 6\Spectrum data\Cu_40_50_RT.txt', '40°C_50Ikrum RT', 'violet','-.'),
 
]


# Energy of the material in keV
material_energy = 8.04 # keV

# Plot all datasets on the same figure
plt.figure(figsize=(10, 6))

for file_path, temperature, color, linestyle in files:
    try:
        # Read the data
        data = pd.read_csv(file_path, header=None, sep=r'\s+', comment='#')
        
        # Extract the fourth column (index 3)
        fourth_column = data[3]
        
        # Plot histogram without density normalization
        counts, bins, _ = plt.hist(fourth_column, bins=100, range=(0, 200), alpha=0.3, density=False)
        
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
            x = np.linspace(0, 200, 1000)
            gaussian_curve = gaussian(x, *popt)

            # Plot the Gaussian curve
            fit_label = f'{temperature} Fit: μ={mu:.2f}, σ={sigma:.2f}, FWHM={FWHM:.2f} keV, R(E) = {energy_resolution:.2f}%'
            plt.plot(x, gaussian_curve, color=color, linestyle=linestyle,  label=fit_label)
        else:
            print(f"No valid data for fitting in file {file_path}.")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Final plot adjustments
plt.xlabel('TOT')
plt.ylabel('Counts')
plt.title('Cu spectrum with different Ikrum and Temperatures')
plt.legend()
plt.xlim(0, 200) 
plt.legend(fontsize=8)
plt.show()

