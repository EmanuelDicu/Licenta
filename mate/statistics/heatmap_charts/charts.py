import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl

# List of folders as seen in the provided image
folders = [
    'output-flow-gemini-1.5-flash',
    'output-flow-gemini-1.5-pro',
    'output-flow-gpt-3.5-turbo',
    'output-flow-gpt-4o',
    'output-flow-meta/llama3-70b-instruct'
]

# Specify the path to the directory containing the folders.
root_directory = "../../"
current_directory = "./"

def check_file(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            true_true, true_false, false_true, false_false = 0, 0, 0, 0
            for problem_data in data.values():
                correctitude = problem_data.get("correctitude", {})
                for model in correctitude.values():
                    cvorum = model.get("Cvorum", False)
                    same_result = model.get("Same result", False)
                    if cvorum and same_result:
                        true_true += 1
                    elif cvorum and not same_result:
                        true_false += 1
                    elif not cvorum and same_result:
                        false_true += 1
                    else:
                        false_false += 1
            return true_true, true_false, false_true, false_false
    except Exception as e:
        print(f"Error reading {json_file_path}: {e}")
        return 0, 0, 0, 0

def compute_pair_value(folder_path):
    total_files = 0
    true_true_count = 0
    true_false_count = 0
    false_true_count = 0
    false_false_count = 0

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                total_files += 1
                file_path = os.path.join(root, file_name)
                t_t, t_f, f_t, f_f = check_file(file_path)
                true_true_count += t_t
                true_false_count += t_f
                false_true_count += f_t
                false_false_count += f_f

    return true_true_count, true_false_count, false_true_count, false_false_count

def list_files_in_specified_folders(root_dir, folder_list):
    fig = plt.figure()
    spec = mpl.gridspec.GridSpec(ncols=6, nrows=2) # 6 columns evenly divides both 2 & 3

    ax1 = fig.add_subplot(spec[0,0:2]) # row 0 with axes spanning 2 cols on evens
    ax2 = fig.add_subplot(spec[0,2:4])
    ax3 = fig.add_subplot(spec[0,4:])
    ax4 = fig.add_subplot(spec[1,1:3]) # row 0 with axes spanning 2 cols on odds
    ax5 = fig.add_subplot(spec[1,3:5])
    
    for idx, folder_name in enumerate(folder_list):
        folder_path = os.path.join(root_dir, folder_name)
        algorithm_name = folder_name.split('/')[-1]
        if algorithm_name.startswith('output-'):
            algorithm_name = algorithm_name[7:]
        else:
            if 'direct' in folder_name:
                algorithm_name = 'direct-llama3-' + algorithm_name[7:]
            else:
                algorithm_name = 'flow-llama3-' + algorithm_name[7:]
        print("Processing folder:", algorithm_name, "...")

        true_true, true_false, false_true, false_false = compute_pair_value(folder_path)

        # Create heatmap data
        heatmap_data = [[true_true, true_false], [false_true, false_false]]

        my_ax = [ax1, ax2, ax3, ax4, ax5][idx]

        # Plot heatmap in the subplot
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['True', 'False'], yticklabels=['True', 'False'], ax=my_ax)
        my_ax.set_title(f"{algorithm_name}")
        my_ax.set_xlabel('Same Result')
        my_ax.set_ylabel('Cvorum')
    
    plt.tight_layout()
    # Save the plot to a file instead of showing it
    plt.savefig('heatmap_plot.png')

# Call the function
list_files_in_specified_folders(root_directory, folders)
