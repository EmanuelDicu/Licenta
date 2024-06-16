import os
import json
import csv
import time
from openai import OpenAI
import vertexai
from vertexai.generative_models import GenerativeModel
from google.api_core.exceptions import ResourceExhausted

# List of folders as seen in the provided image
folders = [
    'output-direct-gpt-4o',
    'output-direct-meta/llama3-70b-instruct',
    'output-flow-gemini-1.5-flash',
    'output-flow-gemini-1.5-pro',
    'output-flow-gpt-3.5-turbo',
    'output-flow-gpt-4o',
    'output-flow-meta/llama3-70b-instruct'
]

project_id = "licenta-425710"
vertexai.init(project=project_id)
gemini_model_15_pro = GenerativeModel(model_name="gemini-1.5-pro")

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

# function to call api
def invoke(model, text: str) -> str:
    completed = False
    sleep = 0
    sleep_time = 2
    while not completed:
        try:
            response = model.generate_content(text)
        except ResourceExhausted as re:
            print(f"ResourceExhausted exception occurred while processing property: {re}")
            sleep += 1
            if sleep > 5:
                print(f"ResourceExhausted exception occurred 5 times in a row. Exiting.")
                break
            time.sleep(sleep_time)
            sleep_time *= 2
        except Exception as e:
            print(f"Exception occurred while processing property: {e}")
            return "NONE"
        else:
            completed = True

    return response.text.strip()

# Function to summarize the solution via api call
def summarize_solution(solution):
    prompt = """
    You are given a solution to a math problem. Your task is to summarize the solution in a few sentences.
    YOU MUST remove all unnecessary information and keep only the most important parts of the solution.
    YOU MUST provide only the solution, no other text.
    Example of unnecessary information:
        * "Here is the solution"
        * "The solution is as follows"
        * "The solution to the problem is"
        * "Solution:"
        * "Step 1:", "Step 2:", etc.
    Here is the solution:
    {Solution}
    """

    return invoke(gemini_model_15_pro, prompt.format(Solution=solution))


def compute_similitude_rates(folder_path):
    sim1 = 0
    sim2 = 0
    total = 0
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(root, file_name)
                print("Processing file: ", file_path, f'-  {total + 1}/{len(files)}...')
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
                    if (summarized_generated_solution == "NONE"):
                        continue
                    correct_solution = correct_solution.replace('\n', '')
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
        print("Processing folder: ", algorithm_name, "...")
        if algorithm_name.startswith('output-'):
            algorithm_name = algorithm_name[7:]

        # Check if the current path is a directory
        if os.path.isdir(folder_path):
            sim1, sim2 = compute_similitude_rates(folder_path)
            csv_writer.writerow([algorithm_name, sim1, sim2])
        else:
            csv_writer.writerow([algorithm_name, 0, 0, 0])
                    

# Call the function
list_files_in_specified_folders(root_directory, folders)

output_csv.close()
