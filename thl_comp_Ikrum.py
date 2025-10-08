import numpy as np
import matplotlib.pyplot as plt

# Temperature range from -40 to +60, step 5
temperature = np.arange(-40, 65, 5)

# Example: threshold values for 5 sets (you will replace these with your actual data)
# thl_set1, thl_set2, thl_set3, thl_set4, thl_set5 should be your input values for each set
# thl_set1 = [1419,1425,1431,1438,1440,1447,1454,1458,1463,1468,1473,1477,1482,1485,1490,1494,1498,1500,1504,1507,1509] #Thl value
# thl_set2 = [1418,1424,1429,1435,1441,1444,1451,1457,1463,1469,1473,1477,1482,1485,1490,1494,1497,1501,1504,1507,1511]#Thl value
# thl_set3 = [1418,1423,1428,1433,1440,1444,1450,1455,1463,1467,1471,1476,1481,1484,1488,1492,1495,1500,1503,1507,1510]#Thl value
# thl_set4 = [1414,1419,1426,1432,1437,1444,1448,1455,1460,1466,1471,1475,1480,1485,1489,1493,1496,1500,1503,1506,1509]#Thl value

thl_set1 = [1450,1450,1453,1458,1469,1475,1482,1488,1493,1497,1501,1503,1507,1511,1515,1520,1524,1527,1531,1535,1538] #Thl mean value
thl_set2 = [1449,1453,1457,1463,1469,1474,1481,1487,1493,1498,1501,1504,1507,1511,1515,1519,1523,1527,1531,1535,1539]#Thl mean value
thl_set3 = [1448,1452,1455,1461,1468,1474,1480,1486,1493,1497,1501,1504,1507,1512,1514,1518,1522,1526,1530,1534,1538]#Thl mean value
thl_set4 = [1447,1448,1453,1459,1465,1474,1480,1486,1491,1497,1501,1505,1508,1511,1515,1519,1523,1527,1531,1534,1537]#Thl mean value

# thl_set2 = [2613,1292,912,580,335,342,139,354,82,65,164,736,612,987,186,480,289,350,275,121,218] #masked pxl
# thl_set3 = [3647,1926,1225,910,507,387,283,161,127,103,60,182,487,258,169,130,106,120,96,107,91]#masked pxl
# thl_set4 = [3432,3678,2345,1459,1072,606,451,346,249,185,128,86,186,195,300,106,85,82,55,96,72]#masked pxl
# thl_set1 = [1990,953,644,328,262,159,97,80,66,45,168,372,234,308,434,608,612,406,289,174,450]#masked pxl
temp_set5 = [-40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60]
#thl_set5 = [1703,447,177,74,108,377,267,102,122,70,143] #Masked pxl
thl_set5 = [1452,1461,1473,1486,1496,1502,1509,1518,1526,1534,1541,] #thl mean value

# Plotting the threshold values for each set
plt.figure(figsize=(10, 6))
plt.plot(temp_set5, thl_set5, label='50Ikrum', marker='o',linestyle='--')
plt.plot(temperature, thl_set1, label='15Ikrum', marker='o',linestyle='--')
plt.plot(temperature, thl_set2, label='10Ikrum', marker='o',linestyle='--')
plt.plot(temperature, thl_set3, label='5Ikrum', marker='o',linestyle='--')
plt.plot(temperature, thl_set4, label='2Ikrum', marker='o',linestyle='--')

# Adding labels and title
plt.xlabel('Temperature (°C)')
plt.ylabel('Thl Value (Equalized peak center)')
plt.title('Comparison of Equalized mean Values with different Ikrum')
#plt.title('Masked pixel count with different Ikrum values')
plt.legend()

# Display the plot
plt.grid(True)
plt.show()
