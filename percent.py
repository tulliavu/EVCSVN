import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Read data from CSV and handle encoding if necessary
data = pd.read_csv('cost.csv', encoding='utf-8')

# Strip any extra spaces in column names
data.columns = data.columns.str.strip()

# List of cost columns
cost_columns = [
    'Chi phí sạc', 'Chi phí vận hành', 'Chi phí đi lại',
    'Chi phí chờ', 'Chi phí lắp đặt', 'Chi phí thuê đất', 'Chi phí bảo dưỡng'
]

# Convert cost columns to numeric, replacing errors with 0
for col in cost_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

# Extract district names and costs
districts = data['Đơn vị hành chính']
charging_cost = data['Chi phí sạc']
operation_cost = data['Chi phí vận hành']
travel_cost = data['Chi phí đi lại']
waiting_cost = data['Chi phí chờ']
installation_cost = data['Chi phí lắp đặt']
land_rent_cost = data['Chi phí thuê đất']
maintenance_cost = data['Chi phí bảo dưỡng']

# Cost data and patterns
costs = [charging_cost, operation_cost, travel_cost, waiting_cost, installation_cost, land_rent_cost, maintenance_cost]
patterns = ['x', 'o', '*', '/', '\\', '|', '.']
labels = [
    "Chi phí sạc", "Chi phí vận hành", "Chi phí đi lại",
    "Chi phí chờ", "Chi phí lắp đặt", "Chi phí thuê đất", "Chi phí bảo dưỡng"
]

# Set up figure and axis
fig, ax = plt.subplots(figsize=(14, 8))

# Define x-axis locations
ind = np.arange(len(districts))
width = 0.8

# Plot each stack bar segment with patterns and border
bottom = np.zeros(len(districts))
for i in range(len(costs)):
    ax.bar(
        ind, costs[i], width, bottom=bottom,
        label=labels[i], hatch=patterns[i], color='white', edgecolor='black', linewidth=1.2
    )
    bottom += costs[i]

# Create legend patches
legend_patches = [
    Patch(facecolor='white', edgecolor='black', hatch=patterns[i], label=labels[i])
    for i in range(len(labels))
]

# Format the plot
ax.set_xlabel('Đơn vị hành chính', fontsize=14)
ax.set_ylabel('Chi phí', fontsize=14)
# ax.set_title('Phân bổ chi phí trên từng đơn vị hành chính', fontsize=14, fontweight='bold')
ax.set_xticks(ind)
ax.set_xticklabels(districts, rotation=45, ha='right', fontsize=14)

# Display legend with adjusted patch size and layout
ax.legend(
    handles=legend_patches,
    loc='upper left',
    bbox_to_anchor=(1, 1),
    fontsize=14,
    title='Loại chi phí',
    title_fontsize=14,
    handleheight=1,         # Reduce icon height
    handlelength=2,         # Reduce icon length
    borderpad=0.05,         # Reduce padding inside the legend box
    labelspacing=0.4,       # Reduce spacing between labels
    handletextpad=0.8       # Space between icon and text
)

plt.tight_layout()

# Save the plot as PNG with desired DPI for high quality
plt.savefig('cost_distribution.png', format='png', dpi=300)

# Show the plot
plt.show()
