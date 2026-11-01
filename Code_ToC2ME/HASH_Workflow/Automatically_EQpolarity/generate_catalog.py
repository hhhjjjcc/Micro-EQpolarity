import os

# Define the directory and output file paths
# Here we give a simple example.
input_directory = '../all_data_demo'
output_file = '../all_data_demo/catalog_sorted_ToC2ME.txt'

# Get a sorted list of all event folder names in the directory
# (only directories are listed, so auxiliary files such as stationlist_ToC2ME.txt are skipped)
folder_names = sorted([
    name for name in os.listdir(input_directory)
    if os.path.isdir(os.path.join(input_directory, name))
])

# Write the folder names to the output file
with open(output_file, 'w') as file:
    for folder_name in folder_names:
        file.write(f'{folder_name}\n')

print(f"Catalog written to {output_file}")
