import os
import json
import csv
import matplotlib.pyplot as plt
from collections import defaultdict

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

def extract_category_and_level(file_name):
    try:
        category = file_name.split('_Level')[0]
        level = int(file_name.split('_Level')[1].split('_')[0])
        return category, level
    except Exception as e:
        print(f"Error parsing {file_name}: {e}")
        return None, None

def compute_stack_charts(folder_path):
    category_level_counts = defaultdict(lambda: [0, 0, 0, 0, 0])
    
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('_out.json'):
                category, level = extract_category_and_level(file_name)
                if category and 1 <= level <= 5:
                    file_path = os.path.join(root, file_name)
                    if is_true_file(file_path):
                        category_level_counts[category][level-1] += 1
    
    return category_level_counts

def create_stack_bar_chart(data, algorithm_name):
    categories = list(data.keys())
    levels = list(zip(*data.values()))
    
    fig, ax = plt.subplots()
    width = 0.35

    colors = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60']
    
    bottoms = [0] * len(categories)
    for i, level in enumerate(levels):
        ax.bar(categories, level, width, label=f'Level {i+1}', bottom=bottoms, color=colors[i])
        bottoms = [bottoms[j] + level[j] for j in range(len(categories))]
    
    ax.set_xlabel('Categories')
    ax.set_ylabel('Number of Solved Problems')
    ax.set_title(f'{algorithm_name}')
    ax.legend()
    
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{algorithm_name}_stack_bar_chart.png")
    plt.close()

def list_files_in_specified_folders(root_dir, folder_list):
    for folder_name in folder_list:
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path):
            algorithm_name = folder_name.split('/')[-1]
            if algorithm_name.startswith('output-'):
                algorithm_name = algorithm_name[7:]

            data = compute_stack_charts(folder_path)
            create_stack_bar_chart(data, algorithm_name)
        else:
            print(f"Folder {folder_name} not found.")

# Call the function
list_files_in_specified_folders(root_directory, folders)
