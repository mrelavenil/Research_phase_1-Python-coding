import matplotlib.pyplot as plt
import re
from lmfit.models import LinearModel

# Predefined x values (example)
x = [8, 15.7, 17.4]  # x-axis values (e.g., Temperature)

# Function to extract y values and label from file
def extract_all_data(file_name):
    all_data = []
    
    # Read the file
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # Match the line pattern to get the label and y-values (numbers in square brackets)
            match = re.match(r"(.*): \[.*\], \[(.*)\]", line)
            if match:
                label = match.group(1)  # The starting part 
                y_values_str = match.group(2)  # The numbers part (e.g., 51.2, 93.15, 112.19)
                # Convert the string of numbers into a list of floats
                y_values = [float(val) for val in y_values_str.split(',')]
                all_data.append((y_values, label))
    
    return all_data

all_data = extract_all_data(r'D:\Elavenil\Miun\Phase 6\Text files\Mean (TOT) values for Cu Mo Zr.txt')  

# Check if any data was found
if not all_data:
    print("No data found in the file.")
else:
    # Initialize the linear model
    linear_model = LinearModel()

    # Plotting the data (all in black)
    for y, label in all_data:
        # Fit the linear model to the data
        params = linear_model.make_params()  # Initialize parameters
        result = linear_model.fit(y, params, x=x)  # Fit the model to the data

        # Plot the original data points
        plt.plot(x, y, color='black', linestyle='-', marker='o')

        # Plot the fitted line
        plt.plot(x, result.best_fit, color='red', linestyle='--', label=f'Fit for {label}')
        
        # Annotate the label at the end of the line
        plt.text(x[-1], y[-1], label, color='black', verticalalignment='top', horizontalalignment='left', fontsize=8)

    # Add labels and title
    plt.xlabel('Energy')
    plt.ylabel('TOT')
    plt.title('Energy calibration at 40°C(Re Equ) with different Ikrum')

    # Show the plot with the legend
   # plt.legend()
    plt.show()
