import re
import matplotlib.pyplot as plt

# Function to extract the data from each file
def extract_data(file_name):
    data = {}
    
    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            # Print the raw line from the file to inspect formatting
            print(f"Raw line: {line.strip()}")  # Debugging: print each line

            # Fix encoding issues by replacing incorrect characters
            line = line.replace('Â°C', '°C').replace('Î¼', 'μ').replace('Ïƒ', 'σ')

            # Print the line after replacements to check if the encoding is fixed
            print(f"Fixed line: {line.strip()}")  # Debugging: print line after replacements

            # Match the pattern: temperature, iKrums type, and μ value, for both 'Re:' and 'RT:'
            match = re.match(r"(\d+°C)_([^:]+)(?::)? μ = ([\d\.]+),", line)

            if match:
                temp = match.group(1)
                ikrum_type = match.group(2)
                mu_value = float(match.group(3))
                
                # Print the extracted data to check the match
                print(f"Matched: {temp}, {ikrum_type}, μ = {mu_value}")  # Debugging: print matched data
                
                # Create a unique key for each temperature + iKrums combination
                label = f"{temp}_{ikrum_type}"
                
                # Add the data to the dictionary
                if label not in data:
                    data[label] = {"temperature": [], "mu_values": []}
                data[label]["temperature"].append(temp)
                data[label]["mu_values"].append(mu_value)
    
    return data


# Read data from all three files
file1_data = extract_data(r'D:\Elavenil\Miun\Phase 6\Text files\Cu spectrum.txt')
file2_data = extract_data(r'D:\Elavenil\Miun\Phase 6\Text files\Zr spectrum.txt')
file3_data = extract_data(r'D:\Elavenil\Miun\Phase 6\Text files\Mo spectrum.txt')

# Combine all data into a single dictionary
all_data = {}
for file_data in [file1_data, file2_data, file3_data]:
    for label, ikrum_data in file_data.items():
        if label not in all_data:
            all_data[label] = {"temperature": [], "mu_values": []}
        all_data[label]["temperature"].extend(ikrum_data["temperature"])
        all_data[label]["mu_values"].extend(ikrum_data["mu_values"])

# Check the data we have collected
print("\nData Collected:")
for label, ikrum_data in all_data.items():
    print(f"{label}: {ikrum_data['temperature']}, {ikrum_data['mu_values']}")

# Plotting the data
plt.figure(figsize=(10, 6))
for label, ikrum_data in all_data.items():
    # We will use the label as the legend (e.g., 10°C_2Ikrum)
    plt.plot(ikrum_data["temperature"], ikrum_data["mu_values"], label=label)

plt.xlabel('Temperature (°C)')
plt.ylabel('μ value')
plt.title('μ vs Temperature for different iKrums')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
