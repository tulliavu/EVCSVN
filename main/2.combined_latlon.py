import pandas as pd
import os

# Load the Unit.csv file to get the list of units
unit_file_path = 'Unit.csv'  # Update this with the correct path to your Unit.csv file
unit_data = pd.read_csv(unit_file_path)
units = unit_data['Unit']

# Initialize an empty list to hold all DataFrames
all_dataframes = []

# Function to process each unit's CSV file
def process_unit_csv(unit):
    file_path = f'input_visualize/{unit}.csv'  # Construct the file path for the unit
    try:
        data = pd.read_csv(file_path, header=None, sep=",", on_bad_lines='skip')

        # Locate the row where "x2 values" and "x3 values" are found
        x2_row_idx = data[data[1] == 'x2 values'].index[0]
        x3_row_idx = data[data[1] == 'x3 values'].index[0]

        # Extract the 'x2' matrix: rows between x2_row_idx + 1 and x3_row_idx - 1
        x2_matrix = data.iloc[x2_row_idx + 1:x3_row_idx, 2:]  # Skipping first 2 columns to match description

        # Extract the 'x3' matrix: rows between x3_row_idx + 1 and the end of the file
        x3_matrix = data.iloc[x3_row_idx + 1:, 2:]

        # Extract x and y coordinates from the first and second rows of the matrix
        x_coordinates = data.iloc[0, 2:]
        y_coordinates = data.iloc[1, 2:]

        # Convert the extracted matrices to numeric, forcing non-numeric values to NaN
        x2_matrix_numeric = x2_matrix.apply(pd.to_numeric, errors='coerce')
        x3_matrix_numeric = x3_matrix.apply(pd.to_numeric, errors='coerce')

        # Filter for values between 1 and 6 in both matrices
        x2_matrix_filtered_range = x2_matrix_numeric[(x2_matrix_numeric >= 1) & (x2_matrix_numeric <= 6)]
        x3_matrix_filtered_range = x3_matrix_numeric[(x3_matrix_numeric >= 1) & (x3_matrix_numeric <= 6)]

        # Calculate the total number of rows in the x2 matrix
        total_x2_rows = x2_matrix_filtered_range.shape[0]

        # Initialize an empty list to hold the data rows
        output_data = []

        # Function to collect values and coordinates into the output data
        def collect_values_and_coordinates(matrix, label, row_offset=0):
            for row_index, row in matrix.iterrows():
                for col_index, value in row.items():  # Use 'items()' to iterate over columns
                    if pd.notna(value):  # If the value is not NaN
                        x_coord = x_coordinates.iloc[col_index-2]
                        y_coord = y_coordinates.iloc[col_index-2]
                        if label == 'x3 value':
                            # Calculate row coordinate for x3 value
                            adjusted_row_index = row_index - total_x2_rows
                            output_data.append([label, value, col_index-2, adjusted_row_index-3, x_coord, y_coord])
                        else:
                            output_data.append([label, value, col_index-2, row_index-2, x_coord, y_coord])

        # Collect values and coordinates for x2 matrix
        collect_values_and_coordinates(x2_matrix_filtered_range, 'x2 value')

        # Collect values and coordinates for x3 matrix, adjusting row index by subtracting total_x2_rows
        collect_values_and_coordinates(x3_matrix_filtered_range, 'x3 value')

        # Convert the output data to a DataFrame
        output_df = pd.DataFrame(output_data, columns=['Type', 'Value', 'Column', 'Row', 'x coordinate', 'y coordinate'])

        # Add the 'Unit' column to the DataFrame as the first column
        output_df.insert(0, 'Unit', unit)

        # Sort the DataFrame by the 'Column' column
        output_df = output_df.sort_values(by='Column')

        # Append the DataFrame to the list of all DataFrames
        all_dataframes.append(output_df)

        # Create output file path by replacing .csv with '_output.csv'
        output_file_path = f"output_visualize/Output_{unit}.csv"

        # Save the result to a CSV file
        output_df.to_csv(output_file_path, index=False)

        print(f"Results saved to {output_file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Iterate over each unit and process the corresponding CSV file
for unit in units:
    process_unit_csv(unit)

# Concatenate all DataFrames into a single DataFrame
combined_df = pd.concat(all_dataframes, ignore_index=True)

# Save the combined DataFrame to a single CSV file
combined_output_file_path = 'output_visualize/Combined_Output.csv'
combined_df.to_csv(combined_output_file_path, index=False)

print(f"Combined results saved to {combined_output_file_path}")