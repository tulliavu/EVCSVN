import matplotlib.pyplot as plt
from adjustText import adjust_text  # Install using `pip install adjustText`

# Enable LaTeX font rendering
#plt.rcParams['text.usetex'] = True
plt.rcParams['font.family'] = 'serif'  # Use a serif font

# Data
districts = [
    "TD City", "D.1", "D.3", "D.4", "D.5",
    "D.6", "D.7", "D.8", "D.10", "D.11",
    "D.12", "GV D.", "TB D.", "TP D.",
    "BTh D.", "PN D.", "BT D.",
    "CC D.", "HM D.", "BC D.", 
    "NB D.", "CG D."
]

solving_time = [
    14.85552008, 52.46584279, 8.987474, 3.851689875, 3.858634791,
    2.858530791, 68.8448585, 2.301349959, 0.713227417, 134.0417399,
    3.2766065, 34.63314629, 3.087476208, 2.208501708, 29.11266633,
    4.69551075, 1.468915167, 4.00, 38.65662263, 105.0,
    20.02748375, 9.82
]

mip_gap = [
    1e-4, 1e-6, 1e-6, 1e-6, 1e-6,
    1e-4, 1e-4, 1e-4, 1e-6, 1e-5,
    1e-6, 1e-6, 1e-4, 1e-6, 1e-4,
    1e-6, 1e-6, 1e-6, 1e-6, 1e-6,
    1e-6, 1e-6
]

# Color mapping for MIP Gap levels
colors = {1e-4: 'red', 1e-5: 'blue', 1e-6: 'green'}
labels = {1e-4: r"$10^{-4}$", 1e-5: r"$10^{-5}$", 1e-6: r"$10^{-6}$"}

# Create the plot
plt.figure(figsize=(12, 8))
texts = []  # Store text objects for dynamic adjustment

# Scatter plot for each MIP Gap level
for mip_level in colors:
    indices = [i for i, gap in enumerate(mip_gap) if gap == mip_level]
    x = [solving_time[i] for i in indices]
    y = [mip_gap[i] for i in indices]
    district_subset = [districts[i] for i in indices]
    plt.scatter(x, y, color=colors[mip_level], label=labels[mip_level], s=250, alpha=1)
    for i, district in enumerate(district_subset):
        # Increase font size for district names
        texts.append(plt.text(x[i], y[i], district, fontsize=20))  # Adjust fontsize here

# Adjust text to avoid overlaps
adjust_text(texts, arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

# Customize plot
plt.xscale('linear')
plt.yscale('log')

# Adjust axis labels and ticks
plt.xlabel(r"Solving Time (seconds)", fontsize=24)  # LaTeX-style x-axis label
plt.ylabel(r"MIP Gap", fontsize=24)  # LaTeX-style y-axis label
plt.xticks(fontsize=18)  # Larger tick labels for x-axis
plt.yticks(fontsize=18)  # Larger tick labels for y-axis

plt.legend(title=r"MIP Gap Levels", fontsize=20)
plt.grid(which="both", linestyle="--", linewidth=0.5)

# Save and show the plot
plt.tight_layout()
plt.savefig("solving_time_vs_mip_gap_adjusted_latex_font.png", dpi=300)
plt.show()
