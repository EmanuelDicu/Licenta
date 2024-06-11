import os
import json


dataset_directory = 'problems_dataset'
math_directory = 'MATH'

categories = ['Algebra', 'Counting & Probability', 'Geometry', 'Number Theory', 'Intermediate Algebra', 'Prealgebra', 'Precalculus']
levels = ['Level 1', 'Level 2', 'Level 3', 'Level 4', 'Level 5']

# Dictionary to keep track of the number of problems for each category and level
# For level 1: 2 problems
# For level 2: 4 problems
# For level 3: 4 problems
# For level 4: 8 problems
# For level 5: 8 problems
problems_per_level = [2, 4, 4, 8, 8]
number_of_problems = {category: {level: 0 for level in levels} for category in categories}

# Function to parse the math dataset
def parse_math_dataset(base_directory):

    # Walk through all directories and files
    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                problem = data['problem']
                category = data['type']
                level = data['level']
                solution = data['solution']

                if category not in categories:
                    continue
                if level not in levels:
                    continue

                # Check if the number of problems for the category and level is less than the maximum
                if number_of_problems[category][level] < problems_per_level[levels.index(level)]:
                    # Add file to dataset_directory with the problem, category, level, and solution
                    json_data = {
                        'problem': problem,
                        'category': category,
                        'level': level,
                        'solution': solution
                    }

                    # write the json data to a file
                    filename = f'{category}_{level}_{number_of_problems[category][level] + 1}.json'
                    with open(os.path.join(dataset_directory, filename), 'w') as f:
                        json.dump(json_data, f, indent=4)

                    # Increment the number of problems for the category and level
                    number_of_problems[category][level] += 1
            
            if all(number_of_problems[category][level] == problems_per_level[levels.index(level)] for category in categories for level in levels):
                return

# Parse the math dataset
parse_math_dataset(math_directory)


