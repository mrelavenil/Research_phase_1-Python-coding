import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

# Define the Double Gaussian function
def double_gaussian(E, A1, mu1, sigma1, A2, mu2, sigma2):
    gaussian1 = A1 * np.exp(-((E - mu1) ** 2) / (2 * sigma1 ** 2))
    gaussian2 = A2 * np.exp(-((E - mu2) ** 2) / (2 * sigma2 ** 2))
    return gaussian1 + gaussian2

# Specify the input file path
input_file = r'D:\Elavenil\Miun\Phase 6\Ag data\10_2Ikrum_spectrum.txt'

# Read the data from the file
data = pd.read_csv(input_file, header=None, sep=r'\s+', comment='#')

# Extract the fifth column
fifth_column = data[3]

# Plot histogram with higher bin resolution
counts, bins, _ = plt.hist(fifth_column, bins=150, range=(0, 200), alpha=0.5, label='Nb histogram', color='black', density=False)

# Use midpoints of bins as x data for fitting
bin_centers = (bins[:-1] + bins[1:]) / 2

# Corrected initial guesses (with tighter sigma values)
initial_guess_double = [
    max(counts),  # Amplitude for the first peak
    35,           # Mean for the first peak
    2,            # **Narrower sigma for first peak**
    max(counts) / 2,  # Amplitude for the second peak
    140,          # Mean for the second peak
    2             # **Narrower sigma for second peak**
]

# Print initial guess to verify
print("Initial guess for double Gaussian fit:", initial_guess_double)

# Apply tighter bounds on sigma to prevent excessive width
bounds = (
    [0, 20, 0.1, 0, 80, 0.1],  # Lower bounds: allow more flexibility
    [np.inf, 50, np.inf, np.inf, 160, np.inf]  # Upper bounds: let sigma be any value
)

# Fit the Double Gaussian curve to the histogram data
try:
    popt, _ = curve_fit(double_gaussian, bin_centers, counts, p0=initial_guess_double, bounds=bounds)
except ValueError as e:
    print("Error during curve fitting:", e)

# Generate Double Gaussian curve with fitted parameters if fitting was successful
x = np.linspace(0, 200, 1000)  # Extended range to 200

if 'popt' in locals():  # Check if fitting succeeded
    double_gaussian_curve = double_gaussian(x, *popt)

    # Extract fitted parameters
    A1, mu1, sigma1, A2, mu2, sigma2 = popt
    fit_label = (
        f'Fitted Double Gaussian Curve\n'
        f'Peak 1: A={A1:.2f}, μ={mu1:.2f}, σ={sigma1:.2f}\n'
        f'Peak 2: A={A2:.2f}, μ={mu2:.2f}, σ={sigma2:.2f}'
    )

    # Plot the Double Gaussian curve
    plt.plot(x, double_gaussian_curve, color='red', label=fit_label)

# Plot the histogram and fit
plt.xlabel('TOT')
plt.ylabel('Counts')
plt.title('Nb Histogram at 40°C with its Equ data')
plt.xlim(0, 200)  # Extended x-axis range
plt.legend()
plt.show()

# Print the fitted parameters for both peaks
if 'popt' in locals():
    print("Fitted parameters for Peak 1:")
    print("Amplitude (A1):", A1)
    print("Mean (mu1):", mu1)
    print("Standard Deviation (sigma1):", sigma1)

    print("\nFitted parameters for Peak 2:")
    print("Amplitude (A2):", A2)
    print("Mean (mu2):", mu2)
    print("Standard Deviation (sigma2):", sigma2)
