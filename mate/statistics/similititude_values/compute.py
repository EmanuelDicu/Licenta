import os
import json
import csv
from openai import OpenAI

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

output_csv = open("similitude_table.csv", "w")
csv_writer = csv.writer(output_csv)
csv_writer.writerow(["algorithm name", "Avg similitude 1", "Avg similitude 2"])

# Function to compute levenstein distance
def ld(s1, s2):
    m = len(s1)
    n = len(s2)
    dist = [0] * (n + 1)
    new_dist = [0] * (n + 1)
    for i in range(n + 1):
        dist[i] = i

    for i in range(m):
        new_dist[0] = i + 1
        for j in range(n):
            deletion_cost = dist[j + 1] + 1
            insertion_cost = new_dist[j] + 1
            if s1[i] == s2[j]:
                substitution_cost = dist[j]
            else:
                substitution_cost = dist[j] + 1
            new_dist[j + 1] = min(deletion_cost, insertion_cost, substitution_cost)
        dist, new_dist = new_dist, dist

    return dist[n]

# Function to compute LCS (Longest Common Subsequence)
def lcs(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


# Function to summarize the solution via api call
def summarize_solution(solution):
    client_nvidia = OpenAI(base_url='https://integrate.api.nvidia.com/v1', 
                       api_key='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')
    prompt = """
    You are given a solution to a math problem. Your task is to summarize the solution in a few sentences.
    YOU MUST remove all unnecessary information and keep only the most important parts of the solution.
    Example of unnecessary information:
        * "Here is the solution"
        * "The solution is as follows"
        * "The solution to the problem is"
        * "Solution:"
        * "Step 1:", "Step 2:", etc.
    Here is the solution:
    {Solution}
    """
    message = {
        "role": "user",
        "prompt": prompt.format(Solution=solution),
    }

    response = client_nvidia.chat.completions.create(model ='meta/llama3-70b-instruct', 
                                                    messages=[message])
    return response.choices[0].text.strip()


def compute_similitude_rates(folder_path):
    sim1 = 0
    sim2 = 0
    total = 0
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as json_file:
                    data = json.load(json_file)
                    # remove _out from file name from string
                    problem = file_name.replace("_out", "")
                    problem_data = data[f'{problem}']
                    correct_solution = problem_data["correct_solution"]
                    generated_solutions = problem_data["generated_solutions"]
                    # extract first solution
                    #get keys of generated_solutions
                    keys = generated_solutions.keys()
                    generated_solution = generated_solutions[list(keys)[0]]
                    # remove '\n' from string
                    summarized_generated_solution = summarize_solution(generated_solution).replace('\n', '')
                    correct_solution = correct_solution.replace('\n', '')

                    print(summarized_generated_solution)
                    return
                    # compute similitude rates
                    sim1 += 1 - ld(correct_solution, summarized_generated_solution) / max(len(correct_solution), len(summarized_generated_solution))
                    sim2 += 1 - ld(correct_solution, generated_solution) / (ld(correct_solution, generated_solution) + lcs(correct_solution, generated_solution))
                    total += 1
    return sim1 / total, sim2 / total
                


def list_files_in_specified_folders(root_dir, folder_list):
    # Iterate over all specified folders
    for folder_name in folder_list:
        folder_path = os.path.join(root_dir, folder_name)

        algorithm_name = folder_name.split('/')[-1]
        if algorithm_name.startswith('output-'):
            algorithm_name = algorithm_name[7:]

        # Check if the current path is a directory
        if os.path.isdir(folder_path):
            sim1, sim2 = compute_similitude_rates(folder_path)
            return
            csv_writer.writerow([algorithm_name, sim1, sim2])
        else:
            csv_writer.writerow([algorithm_name, 0, 0, 0])
                    

# Call the function
list_files_in_specified_folders(root_directory, folders)

output_csv.close()
