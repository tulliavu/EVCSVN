import matplotlib.pyplot as plt
import numpy as np

# Configure matplotlib to use LaTeX-compatible font sizes
plt.rcParams.update({
    'font.size': 24,               # Set default font size, equivalent to LaTeX 12pt
    'axes.titlesize': 24,          # Title font size
    'axes.labelsize': 26,          # x and y label font size
    'xtick.labelsize': 26,         # x tick labels
    'ytick.labelsize': 26,         # y tick labels
    'legend.fontsize': 24,         # Legend font size
    'figure.titlesize': 24         # Overall figure title font size (if used)
})

# Data
units = [
    "District 12", "District 7", "Binh Thanh", "District 3", "Tan Binh", "Tan Phu", 
    "District 8", "District 6", "Binh Chanh", "Cu Chi", "Binh Tan", "Go Vap", 
    "District 11", "Thu Duc City", "Hoc Mon", "Phu Nhuan", "District 5", 
    "District 4", "Nha Be", "District 10", "District 1", "Can Gio"
]
type2_chargers = [55, 57, 48, 57, 37, 34, 37, 49, 18, 29, 6, 10, 37, 0, 22, 33, 26, 21, 8, 1, 5, 2]
type3_chargers = [22, 8, 15, 0, 18, 20, 17, 4, 31, 19, 39, 34, 5, 40, 18, 3, 4, 6, 8, 13, 5, 2]
average_chargers_per_point = [
    7.70, 6.50, 7.88, 5.70, 5.50, 9.00, 7.71, 5.89, 8.17, 9.60, 
    6.43, 7.33, 6.00, 5.71, 10.00, 6.00, 6.00, 6.75, 8.00, 4.67, 
    10.00, 4.00
]

# Calculate total chargers for each district
total_chargers = [t2 + t3 for t2, t3 in zip(type2_chargers, type3_chargers)]

# Create the bar chart
x = np.arange(len(units))
width = 0.35  # width of the bars

fig, ax = plt.subplots(figsize=(15, 8))
bars1 = ax.bar(x - width/2, type2_chargers, width, label='Type 2 Chargers', color='skyblue')
bars2 = ax.bar(x + width/2, type3_chargers, width, label='Type 3 Chargers', color='salmon')

# Add line for average chargers per point
ax.plot(x, average_chargers_per_point, color='green', marker='o', linestyle='--', linewidth=2, label='Average Chargers per Point')

# Add labels, title, and custom x-axis tick labels
ax.set_ylabel('Number of Chargers')
ax.set_xticks(x)
ax.set_xticklabels(units, rotation=90, ha='center')  # Rotate labels 90 degrees

# Add legend
ax.legend()

# Save as PNG
plt.tight_layout()
plt.savefig("charging_stations_chart.png", format="png")
plt.show()
