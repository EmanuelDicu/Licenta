import os
import json
import csv

# List of folders as seen in the provided image
folders = [
    'output-direct-gemini-1.5-flash',
    'output-direct-gemini-1.5-pro',
    'output-direct-gpt-3.5-turbo',
    'output-direct-gpt-4o',
    'output-direct-meta/llama3-70b-instruct',
    'output-flow-gemini-1.5-flash',
    'output-flow-gemini-1.5-pro',
    'output-flow-gpt-3.5-turbo',
    'output-flow-gpt-4o',
    'output-flow-meta/llama3-70b-instruct'
]

# Specify the path to the directory containing the folders.
root_directory = "../../"
current_directory = "./"

output_csv = open("accuracy_table.csv", "w")
csv_writer = csv.writer(output_csv)
csv_writer.writerow(["algorithm name", "total files", "true files", "accuracy"])

def is_true_file(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            for problem_data in data.values():
                correctitude = problem_data.get("correctitude", {})
                for model in correctitude.values():
                    if model.get("Cvorum", False):
                        return True
        return False
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        return False

def compute_accuracy_rate(folder_path):
    total_files = 0
    true_files = 0
    
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                total_files += 1
                file_path = os.path.join(root, file_name)
                if is_true_file(file_path):
                    true_files += 1

    accuracy_rate = true_files / total_files if total_files > 0 else 0
    return total_files, true_files, accuracy_rate

def list_files_in_specified_folders(root_dir, folder_list):
    # Iterate over all specified folders
    for folder_name in folder_list:
        folder_path = os.path.join(root_dir, folder_name)

        algorithm_name = folder_name.split('/')[-1]
        if algorithm_name.startswith('output-'):
            algorithm_name = algorithm_name[7:]

        # Check if the current path is a directory
        if os.path.isdir(folder_path):
            total_files, true_files, accuracy_rate = compute_accuracy_rate(folder_path)
            csv_writer.writerow([algorithm_name, total_files, true_files, accuracy_rate])
        else:
            csv_writer.writerow([algorithm_name, 0, 0, 0])
                    

# Call the function
list_files_in_specified_folders(root_directory, folders)

output_csv.close()
