import os
import json
import random
import re

num_problems = 30
file = 'grade-school-math/grade_school_math/data/test.jsonl'
out_folder = 'problem_dataset_gradeschool'


def replace_number_with_boxed(text):
    # This regex matches "#### " followed by one or more digits
    pattern = r"#### (\d+)"
    
    # This function will be used to format the replacement
    def replacement(match):
        number = match.group(1)
        return f"\\boxed{{{number}}}"
    
    # Use re.sub with the pattern, replacement function, and input text
    result = re.sub(pattern, replacement, text)
    
    return result


with open(file, 'r') as f:
    data = f.readlines()

data = [json.loads(x) for x in data]
 
# random shuffle
random.shuffle(data)

# create output folder if it doesn't exist
if not os.path.exists(out_folder):
    os.makedirs(out_folder)

# write the problems to files
for i in range(num_problems):
    problem = data[i]
    
    json_data = {
        'problem': problem['question'],
        'category': 'Grade School Math',
        'level': 'Level 2',
        'solution': replace_number_with_boxed(problem['answer'])
    }

    # write the json data to a file
    filename = f'Grade_School_Math_{i + 1}.json'
    with open(os.path.join(out_folder, filename), 'w') as f:
        json.dump(json_data, f, indent=4)



