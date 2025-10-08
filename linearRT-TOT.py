import numpy as np
import matplotlib.pyplot as plt
from lmfit.models import LinearModel

# Given data points
x = np.array([ 4.5, 8, 15.7, 17.5,22.1,24.9])
y = np.array([ 1397,1320, 1119, 1062, 953, 880])

# Define multiple ta
# rget y values for interpolation
target_y_values = [669,834,996,1150,1315]

# Fit a linear model using lmfit
model = LinearModel()
params = model.make_params(slope=1, intercept=0)
result = model.fit(y, params, x=x)

# Extract fitted parameters
slope = result.params['slope'].value
intercept = result.params['intercept'].value

# Compute interpolated x values for given target_y_values
x_interpolated = [(y_target - intercept) / slope for y_target in target_y_values]

# Plot the original data and the fitted line
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color='blue', label='Data Points')
plt.plot(x, result.best_fit, color='black', linestyle='--', label='Linear Fit')

# Plot interpolated points
for i, y_target in enumerate(target_y_values):
    plt.plot(x_interpolated[i], y_target, 'ro', label=f'Interpolated: ({x_interpolated[i]:.2f}, {y_target})')
    plt.annotate(f'({x_interpolated[i]:.2f}, {y_target})', (x_interpolated[i], y_target),
                 textcoords="offset points", xytext=(10, -10), ha='center', color='red')

# Labels and title
plt.xlabel('Energy (KeV)')
plt.ylabel('Thl')
plt.title('Linear Fit with ThlScan value')
plt.legend()
plt.grid(True)
plt.show()

# Output the interpolated values
for y_target, x_val in zip(target_y_values, x_interpolated):
    print(f"The estimated x value for y = {y_target} is {x_val:.2f}")
