import os
import pandas as pd
import matplotlib.pyplot as plt

# Folder path containing the datasets
folder_path = 'data_time'  # Replace with your actual path

# Get list of all CSV files in the folder
files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Sort files by name (assuming 'data_time' sequence is based on file names)
files.sort()

# Number of datasets
n_files = len(files)

# Number of plots per figure: First two figures with 7 plots, third figure with 8
plots_per_fig = [7, 7, 8]

# Initialize index for starting plot in each figure
start_idx = 0

# Loop through each figure and plot datasets in the specified order
for fig_idx, num_plots in enumerate(plots_per_fig):
    # Calculate rows and columns for a grid layout (2 plots per row)
    n_cols = 2
    n_rows = (num_plots + 1) // n_cols  # Divide the number of plots over 2 columns
    
    # Create a grid of subplots (2 columns per figure)
    fig, axs = plt.subplots(n_rows, n_cols, figsize=(16, n_rows * 4))
    axs = axs.flatten()  # Flatten axes for easy indexing

    # Plot each dataset, ordered top-to-bottom
    for i in range(num_plots):
        file_idx = start_idx + i
        if file_idx >= n_files:
            break

        # Load the dataset and skip the first two data rows (but not the header)
        file_path = os.path.join(folder_path, files[file_idx])
        data = pd.read_csv(file_path, skiprows=[1, 2])  # Skipping the first 2 data rows after the header

        # Check if required columns exist
        if 'Time' in data.columns and 'Objective Value' in data.columns and 'Best Bound' in data.columns:
            # Plot Objective Value vs Time
            axs[i].plot(data['Time'], data['Objective Value'], label='Objective Value', color='blue')
            # Optionally, plot Best Bound on the same plot
            axs[i].plot(data['Time'], data['Best Bound'], label='Best Bound', color='orange', linestyle='--')

            # Set titles and labels
            axs[i].set_title(f'Plot {file_idx+1}: {files[file_idx]}', fontsize=16)
            axs[i].set_xlabel('Time')
            axs[i].set_ylabel('Value')
            axs[i].legend()
        else:
            print(f"Skipping dataset {file_idx+1}: required columns not found.")
            continue

    # Remove any unused axes
    for j in range(i+1, len(axs)):
        fig.delaxes(axs[j])

    # Adjust layout to avoid overlap
    plt.tight_layout()

    # Save the figure as an image
    plt.savefig(f'figure_{fig_idx+1}.png', dpi=300)  # Save at high resolution

    # Increment starting index for next figure
    start_idx += num_plots

# Show the plots (optional)
plt.show()
