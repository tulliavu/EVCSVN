import math
import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import csv
import time
import matplotlib.pyplot as plt
# Gurobi key
options = {
   "WLSACCESSID": "341449c4-53c6-46fb-a9d2-431c3bbb8aad",
   "WLSSECRET": "037a1264-3f6f-481f-aaf3-b41016561e64",
   "LICENSEID": 2555171,
}
with gp.Env(params=options) as env, gp.Model(env=env) as model:
   # Formulate problem
   model.optimize()
# Step 1: Load data from CSV files
POI_df = pd.read_csv('input_data/POI.csv')  # Columns: ['Lat1', 'Lon1', 'Land_Cost', 'Unit']
People_df = pd.read_csv('input_data/PEOPLE_OLD.csv')  # Columns: ['Lat2', 'Lon2', 'Unit']
Constraint_df = pd.read_csv('input_data/CONSTRAINT.csv')  # Columns: ['Unit', 'Budget', 'Demand', 'Slot']
# Ensure 'Land_Cost', 'Budget', 'Demand', and 'Slot' are numeric
POI_df['Land_Cost'] = pd.to_numeric(POI_df['Land_Cost'], errors='coerce')
Constraint_df['Budget'] = pd.to_numeric(Constraint_df['Budget'], errors='coerce')
Constraint_df['Demand'] = pd.to_numeric(Constraint_df['Demand'], errors='coerce')
Constraint_df['Slot'] = pd.to_numeric(Constraint_df['Slot'], errors='coerce')
# Earth's radius in kilometers for the Haversine formula
R = 6371.0
# Step 2: Define the Haversine function to calculate the distance between POIs and People nodes
def haversine(lat1, lon1, lat2, lon2):
   """
   Calculate the great-circle distance between two points on the Earth
   using the Haversine formula.
   """
   dlat = math.radians(lat2 - lat1)
   dlon = math.radians(lat2 - lon1)
   a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
   return 2 * R * math.asin(math.sqrt(a))
# Filter data for unit

unit_name = "TP Thủ Đức" #changing depending on administrative unit

POI_group = POI_df[POI_df['Unit'] == unit_name]
People_group = People_df[People_df['Unit'] == unit_name]
Constraint_group = Constraint_df[Constraint_df['Unit'] == unit_name]
Budget = Constraint_group['Budget'].values[0]
Demand = Constraint_group['Demand'].values[0]
Slot = Constraint_group['Slot'].values[0]
print(f"Processing unit: {unit_name} with Budget: {Budget}, Demand: {Demand}, and Slot: {Slot}")
# Print the number of columns in POI_group and People_group
print(f"Number of columns in POI_group: {POI_group.shape[0]}")
print(f"Number of columns in People_group: {People_group.shape[0]}")
# Step 3: Initialize the optimization problem as a minimization problem
model = gp.Model("Minimize_Charging_Cost")
# Step 4: Create decision variables as matrices for each POI-People pair (number of chargers: x2 and x3)
x2 = model.addMVar((len(People_group), len(POI_group)), vtype=GRB.INTEGER, lb=0, ub=6, name="x2")
x3 = model.addMVar((len(People_group), len(POI_group)), vtype=GRB.INTEGER, lb=0, ub=6, name="x3")
b = model.addMVar((len(People_group), len(POI_group)), vtype=GRB.BINARY, name="b")
# Step 5: Define the objective function to minimize total cost (including fixed, land, and transportation costs)
total_cost = gp.QuadExpr()  # Initialize a quadratic expression for the total cost
loop_count = 0  # Initialize a counter for loops
for i in range(len(POI_group)):
   # Land cost contribution for POI i (proportional to the sum of chargers across all people)
   land_cost = POI_group.iloc[i]['Land_Cost'] / 14_600 * (x2.sum(axis=0)[i] + x3.sum(axis=0)[i]) * b.sum(axis=0)[i]
   fixed_cost = 439_621 * x2.sum(axis=0)[i] * b.sum(axis=0)[i] + 2_173_018  * x3.sum(axis=0)[i] * b.sum(axis=0)[i]
   transportation_cost = gp.QuadExpr()
   for j in range(len(People_group)):
       dist = haversine(POI_group.iloc[i]['Lat1'], POI_group.iloc[i]['Lon1'], People_group.iloc[j]['Lat2'], People_group.iloc[j]['Lon2'])
       transportation_cost += (38_868 * x2[j, i] + 212_005 * x3[j, i]) * dist * b[j, i]  # Cost depends on distance
       # Increment the loop counter
       loop_count += 1
   # Add the total cost for this POI
   total_cost += land_cost + fixed_cost + transportation_cost
# After completing the loops, print the number of loops
print(f"Total number of iterations for loops: {loop_count}")
# Set the objective function to minimize the total cost
model.setObjective(total_cost, GRB.MINIMIZE)
# Step 6: Add constraints
model.addConstr(
   (21_349 * x2.sum() + 90_784 * x3.sum()) <= (Budget / 3650),
   "Total_Charger_Upper_Bound"
)
model.addConstr(
   (52.8 * x2.sum() + 288 * x3.sum()) >= Demand,
   "Total_Charger_Lower_Bound"
)
for i in range(len(POI_group)):
   for j in range(len(People_group)):
       model.addConstr((b[j, i] == 0) >> (x2[j, i] + x3[j, i] == 0), "if else constraint_1")
       model.addConstr((b[j, i] == 1) >> (x2[j, i] + x3[j, i] >= 1), "if else constraint_2")
for i in range(len(POI_group)):
   model.addConstr(x2.sum(axis=0)[i] <= 6)
   model.addConstr(x3.sum(axis=0)[i] <= 6)
# Define the callback function to collect data during optimization
def data_cb(model, where):
   if where == gp.GRB.Callback.MIP:
       cur_obj = model.cbGet(gp.GRB.Callback.MIP_OBJBST)
       cur_bd = model.cbGet(gp.GRB.Callback.MIP_OBJBND)
       # Did objective value or best bound change?
       if model._obj != cur_obj or model._bd != cur_bd:
           model._obj = cur_obj
           model._bd = cur_bd
           model._data.append([time.perf_counter() - model._start, cur_obj, cur_bd])  # Higher precision time capture
# Initialize callback data
model._obj = None
model._bd = None
model._data = []
model._start = time.perf_counter()  # Start with high-precision timer
# Step 7: Solve the problem using Gurobi's solver with the callback function
model.setParam('MIPGap', 0.0001)
model.optimize(callback=data_cb)
# Extract and save results
x2_values = x2.X
x3_values = x3.X
b_values = b.X
optimal_solution = model.ObjVal
# Save results to a single CSV file
with open(f'result_x2_x3/results_unit_{unit_name}.csv', 'w', newline='') as f:
   writer = csv.writer(f)
   # Write x2 values
   writer.writerow(['x2 values'])
   writer.writerows(x2_values)
   # Write x3 values
   writer.writerow([])
   writer.writerow(['x3 values'])
   writer.writerows(x3_values)
   # Write b values
   writer.writerow
   writer.writerow(['b values'])
   writer.writerows(b_values)
   # Write optimal solution
   writer.writerow([])
   writer.writerow(['Optimal Solution'])
   writer.writerow([optimal_solution])
# Save callback data to a CSV file
callback_data_filename = f'data_time/data_{unit_name}.csv'
with open(callback_data_filename, 'w', newline='') as f:
   writer = csv.writer(f)
   writer.writerow(['Time', 'Objective Value', 'Best Bound'])
   writer.writerows(model._data)
# Save callback data to a CSV file
callback_data_filename = f'data_time/data_{unit_name}.csv'
with open(callback_data_filename, 'w', newline='') as f:
   writer = csv.writer(f)
   writer.writerow(['Time', 'Objective Value', 'Best Bound'])
   writer.writerows(model._data)
# Step 8: Plot the results from 'data_{unit_name}.csv'
# Load the saved data
data = pd.read_csv(callback_data_filename)
data = data.iloc[:]  # Exclude the first row
# Verify the first few rows to ensure correct loading
print(data.head())
# Step 2: Plotting Best Bound and Objective Value over Time
plt.figure(figsize=(12, 8))
# Plot the Objective Value with markers for clear visibility
plt.plot(data['Time'], data['Objective Value'], label='Objective Value', color='orange', linewidth=2, marker='o')
# Plot the Best Bound with a dashed line and markers
plt.plot(data['Time'], data['Best Bound'], label='Best Bound', color='gray', linewidth=2, linestyle='--', marker='x')
# Adding labels and title with adjustments for clarity
plt.xlabel('Time (seconds)', fontsize=14)
plt.ylabel('Value', fontsize=14)
plt.title(f'{unit_name}', fontsize=16)
# Use logarithmic scale for the y-axis
plt.yscale('log')
# Adding grid for better readability
plt.grid(True, linestyle='--', alpha=0.7)
# Display the legend to distinguish between the lines
plt.legend()
# Save the plot with a filename associated with the unit name
plot_filename = f'plot_name/plot_{unit_name}.png'
plt.savefig(plot_filename)
# Show the plot
plt.show()
print(f"The plot has been saved as {plot_filename}.")