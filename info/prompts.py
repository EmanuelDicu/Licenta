generate_solution_direct_prompt = """
You are a C++ programming contest participant. You are given a problem statement and you need to write a C++ program to solve it.
- You MUST NOT use any external libraries or functions. You can only use the standard C++ library.
- You MUST refrain from adding any extraneous text that is not directly part of or relevant to the solution.
- You MUST provide the solution code. Do not include any input/output code or function signature.
- You MUST format the content so that it can be enclosed within a triple-quoted string.
- You MUST provide only one solution, without any alternative variations.
- You MUST wrap the C++ solution code with cpp<<YOUR_SOLUTION_HERE>>cpp tag.
- You MUST deliver a comprehensive solution, detailing all the necessary steps instead of just presenting the final answer.
- You MUST explain the reasoning behind each step, focusing solely on the provided constraints and the problem description.

Here is an example:
Problem:
A train covers a distance of x kilometers in y hours. Determine the train's average speed.
Objective:
Calculate the train's average speed using the given distance and time.
Input:
On the first line there are two numbers, x (distance in kilometers) and y (time in hours)
Output:
Print only one number, the average train's speed.

Example of test cases:
Input: 300 3.5
Output: 85.7

Solution:
Step 1:
Read from the input 300 (distance in kilometers) and 3.5 (time in hours)
Step 2:
To find the average speed, divide the distance by the time: 300 kilometers / 3.5 hours = approximately 85.7 km/h.
Step 3:
Therefore, the train's average speed is approximately 85.7 km/h.

C++ Solution code:
cpp<<
#include <iostream>

int main() {{
  // Given values
  double distance_km;  // distance traveled in kilometers
  double time_hours;   // time taken in hours
  
  std::cin >> distance_km >> time_hours;

  // Calculate the average speed
  double average_speed_kmph = distance_km / time_hours;

  // Output the average speed
  std::cout << average_speed_kmph << std::endl;

  return 0;
}}
>>cpp

This is the problem you need to solve:
Problem:
{Problem}
Input:
{Input}
Output:
{Output}
C++ solution code:
"""


get_objective_and_constraints_prompt = """
Assist me in identifying and examining the primary constraints and the goal of an algorithmic problem.
- You MUST extract the constraints directly from the problem statement without making any assumptions or inferences.
- You MUST NOT provide any solution or answer to the problem.
- You MUST format the constraints as a bullet-point list, with each constraint being formatted using the following format: cns{{YOUR_CONSTRAINT_HERE}}cns
- You MUST identify a single, clear objective that has to be surrounded in the following tag: obj{{YOUR_GOAL_HERE}}obj

Here is an example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
cns{{The train travels a distance of 200 kilometers}}cns
cns{{The train travels for 2 hours}}cns
Objective:
obj{{Calculate the average speed of the train based on the distance traveled and the time taken}}obj

Please identify the main constraints and the objective for the following problem:
{Problem}
"""

get_additional_constraint_prompt = """
Assist me in deriving an additional constraintfrom an algorithmic problem.
- You CAN ONLY use the existing constraints and the problem text to deduce this additional constraint.
- You MUST identify a additional constraint that is logically derived from the problem text and the existing constraints.
- The additional constraint MUST be relevant to achieving the problem's goal.
- Please format the additional constraint in a way that it can be included in a triple-quoted string.
- You MUST provide ONLY the additional constraint.
- You MUST NOT provide any solution or answer to the problem.
- You MUST format the constraint as such: ncns{{YOUR_NEW_CONSTRAINT_HERE}}ncns
- IF no additional constraint can be deduced, please provide a message saying ncns{{NONE}}ncns


Here is an example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Objective:
- Calculate the average speed of the train based on the distance traveled and the time taken
Additional constraint: 
ncns{{The average speed of the car is calculated by dividing the distance traveled by the time taken}}ncns

Please identify an additional constraint for the following problem:
Problem: 
{Problem}
Main constraints: 
{Constraints}
Objective: 
{Objective}
Additional constraint:
"""

test_constraint_prompt = """
Assist me in determining whether an additional constraint is valid for an algorithmic problem.
- The constraint is wrapped in the following format: ncns{{CONSTRAINT_TO_BE_VALIDATED}}ncns
- You MUST provide a YES or NO as your final answer.
- Please format the response so that it can be included in a triple-quoted string.
- IF the constraint is valid, it MUST be logically derived from the problem text and the existing constraints.
- IF the constraint is true, you MUST respond with YES.
- IF the constraint is false, you MUST respond with NO.


Here is an example:
Problem: 
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Objective:
- Calculate the average speed of the train based on the distance traveled and the time taken
Constraint to be validated:
- The average speed of the car is calculated by dividing the time take by the distance traveled
Answer: 
NO

Here is another example:
Problem: 
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Objective:
- Calculate the average speed of the train based on the distance traveled and the time taken
Constraint to be validated:
- The average speed of the car is calculated by dividing the distance traveled by the time taken
Answer: 
NO

Please test the following constraint for the given problem:
Problem:
{Problem}
Main constraints:
{Constraints}
Objective:
{Objective}
Constraint to be validated:
{NewConstraint}
Answer:
"""

fix_constraint_prompt = """
Help me revise a constraint derived from an algorithmic problem.
- You MUST identify and provide a new constraint that is logically consistent with the problem text.
- Please format your response so that it can be included in a triple-quoted string.
- The revised constraint MUST be essential for achieving the problem's goal.
- The revised constraint MUST not duplicate the meaning of the known main constraints.
- The revised constraint MUST not be the same as the incorrect constraint, the known constraints, or a rephrased version of either.
- You MUST provide ONLY the new, corrected constraint.
- If no other constraint can be deduced, you can respond with NONE.

Here is an example:
Problem:
The product of two numbers is 24. The first number is twice the second number. What are the numbers?
Incorrect constraint:
The product of the two numbers is 30.
Corrected constraint:
The product of the two numbers is 24.

Please fix the following constraint for the given problem:
Problem: 
{Problem}
Main constraints:
{Constraints}
Objective:
{Objective}
Incorrect constraint: 
{Incorrect_constraint}
Fixed constraint:
"""

can_solve_problem_prompt = """
Help me test if the conditions of a math problem are sufficient to achieve the goal.
Please format the text in a such way for it to be able to be included in a triple-quoted string.
You MUST provide a YES or NO as your final answer.
If the conditions are sufficient to achieve the goal, you should answer YES.
If the conditions are not sufficient to achieve the goal, you should answer NO.

Here is an example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
- The average speed of the car is calculated by dividing the distance traveled by the time taken
Objective:
- Calculate the average speed of the train based on the distance traveled and the time taken
Answer:
YES

Here is another example:
Here is an example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Main constraints:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Objective:
Calculate the average speed of the train based on the distance traveled and the time taken
Answer:
NO

Please test if the following conditions are sufficient to achieve the goal of the problem:
Problem:
{Problem}
Main constraints:
{Constraints}
Objective:
{Objective}
Answer:
"""

generate_solution_MACM_prompt = """
You are a C++ programing contest participant. You are given a problem statement and the main key points of the solution 
and also the objective of the problem. Your task is to write a C++ program to solve the problem.
- You MUST NOT use any external libraries or functions. You can only use the standard C++ library.
- You MUST refrain from adding any extraneous text that is not directly part of or relevant to the solution.
- You MUST use the provided constraints and the problem description to derive the solution.
- You MUST provide the solution code. Do not include any input/output code or function signature.
- You MUST use the provided constraints and the problem description to derive the solution.
- You MUST format the content so that it can be enclosed within a triple-quoted string.
- You MUST provide only one solution, without any alternative variations.
- You MUST wrap the C++ solution code with cpp{{...}}cpp tag.
- You MUST deliver a comprehensive solution, detailing all the necessary steps instead of just presenting the final answer.
- You MUST explain the reasoning behind each step, focusing solely on the provided constraints and the problem description.

Here is an example:
Problem:
A train covers a distance of x kilometers in y hours. Determine the train's average speed.
Main constraints:
- The train covers a distance of x kilometers
- The train covers the distance in y hours
- The average speed of the train is calculated by dividing the distance by the time
Objective:
- Calculate the train's average speed using the given distance and time.
Input:
On the first line there are two numbers, x (distance in kilometers) and y (time in hours)
Output:
Print only one number, the average train's speed.

Example of test cases:
Input: 300 3.5
Output: 85.7

Solution:
Step 1:
Read from the input 300 (distance in kilometers) and 3.5 (time in hours)
Step 2:
To find the average speed, divide the distance by the time: 300 kilometers / 3.5 hours = approximately 85.7 km/h.
Step 3:
Therefore, the train's average speed is approximately 85.7 km/h.

Solution code:
cpp{{
#include <iostream>

int main() {
  // Given values
  double distance_km;  // distance traveled in kilometers
  double time_hours;   // time taken in hours
  
  std::cin >> distance_km >> time_hours;

  // Calculate the average speed
  double average_speed_kmph = distance_km / time_hours;

  // Output the average speed
  std::cout << average_speed_kmph << std::endl;

  return 0;
}
}}cpp

This is the problem you need to solve:
Problem:
{Problem}
Main constraints:
{Constraints}
Objective:
{Objective}
Input:
{Input}
Output:
{Output}
C++ solution code:
cpp{{YOUR SOLUTION HERE}}cpp
"""

get_solution_ToT_prompt = generate_solution_MACM_prompt

explain_bullet_points_prompt = """
Help me explain the key points of a problem statement.
- You MUST extract the key points directly from the problem statement.
- You MUST NOT provide any solution or answer to the problem.
- You MUST format the key points as a bullet-point list, with each point being preceded by a dash.
- You MUST provide a comprehensive explanation of the key points.
- You MUST NOT include any extraneous text that is not directly part of or relevant to the key points.
- You MUST NOT include any information that is not relevant to the problem.
- You MUST format the explanation in a way that it can be included in a triple-quoted string.

Here is an example:
Problem:
A train covers a distance of x kilometers in y hours. Determine the train's average speed.
Calculate the train's average speed using the given distance and time.

Key points:
- The train covers a distance of x kilometers
- The train covers the distance in y hours
- The average speed of the train is calculated by dividing the distance by the time

Explanation:
The problem statement provides the distance covered by the train and the time taken to cover the distance. 
To calculate the average speed of the train, we divide the distance by the time. This key point is crucial for understanding how to solve the problem.

Please explain the key points of the following problem statement:
Problem:
{Problem}
"""

explain_input_output_prompt = """
Based on your understanding of the problem, explain why for the following input the output is as follows:
- You MUST NOT provide any solution or answer to the problem.
- You MUST explain the reasoning behind the input and output relationship.
- You MUST NOT include any extraneous text that is not directly part of or relevant to the input and output relationship.
- You MUST format the explanation in a way that it can be included in a triple-quoted string.

Here are the input and output values:

Input1: 
{Input1}
Output1:
{Output1}

Input2:
{Input2}
Output2:
{Output2}

Input3:
{Input3}
Output3:
{Output3}

Please explain the relationship between the input and output for each of the provided test cases.
"""

generate_starting_solutions_prompt = """
Based on the key points and the input-output relationship, generate three solutions to the problem in natural language
- You MUST NOT provide any solution code.
- You MUST generate three different solutions based on the key points and the input-output relationship.
- You MUST NOT include any extraneous text that is not directly part of or relevant to the solutions.
- You MUST provide a comprehensive explanation of each solution.
- You MUST format the solutions in a way that they can be included in a triple-quoted string.
- You MUST format the solutions by surrounding them with the following tags: 
sol1{{YOUR_FIRST_SOLUTION_HERE}}sol1
sol2{{YOUR_SECOND_SOLUTION_HERE}}sol2
sol3{{YOUR_THIRD_SOLUTION_HERE}}sol3

Please generate three different solutions based on the key points and the input-output relationship for the problem
"""

gen_final_solution_flow_engineering_prompt = """
Based on the key points, the input-output relationship, and the generated solutions, pick the best solution and write the C++ code for it.
- You MUST pick EXACTLY ONE solution from the generated solutions.
- You MUST write the C++ code for the selected solution.
- You MUST NOT use any external libraries or functions. You can only use the standard C++ library.
- You MUST refrain from adding any extraneous text that is not directly part of or relevant to the solution.
- You MUST provide the solution code. Do not include any input/output code or function signature.
- You MUST format the content so that it can be enclosed within a triple-quoted string.
- You MUST provide only one solution, without any alternative variations.
- You MUST wrap the C++ solution code with cpp{{...}}cpp tag.
- You MUST deliver a comprehensive solution, detailing all the necessary steps instead of just presenting the final answer.
- You MUST explain the reasoning behind each step, focusing solely on the provided constraints and the problem description.

Here is an example:
Problem:
A train covers a distance of x kilometers in y hours. Determine the train's average speed.
Calculate the train's average speed using the given distance and time.

Key points:
- The train covers a distance of x kilometers
- The train covers the distance in y hours
- The average speed of the train is calculated by dividing the distance by the time

Solution in natural language:
The problem statement provides the distance covered by the train and the time taken to cover the distance.
To calculate the average speed of the train, we divide the distance by the time. This key point is crucial for understanding how to solve the problem.


Solution code:
cpp{{
#include <iostream>

int main() {
  // Given values
  double distance_km;  // distance traveled in kilometers
  double time_hours;   // time taken in hours

  std::cin >> distance_km >> time_hours;

  // Calculate the average speed
  double average_speed_kmph = distance_km / time_hours;

  // Output the average speed
  std::cout << average_speed_kmph << std::endl;

  return 0;
}
}}cpp

Please write the C++ code for the best solution based on the key points, the input-output relationship, and the generated solutions.
"""

get_problem_objective_prompt = """
Help me identify the primary objective of an algorithmic problem.
- You MUST NOT provide any solution or answer to the problem.
- You MUST extract the primary objective directly from the problem statement.
- You MUST NOT include any extraneous text that is not directly part of or relevant to the primary objective.
- You MUST format the primary objective by surrounding it with the following tags: obj{{YOUR_OBJECTIVE_HERE}}obj
- You MUST write the primary objective in a way that it can be included in a triple-quoted string.

Here is an example:
Problem
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Objective:
obj{{Calculate the average speed of the train based on the distance traveled and the time taken}}obj

Please identify the primary objective for the following problem:
Problem:
{Problem}
Objective:
"""

get_new_key_point_prompt = """
Help me find a new key point for an algorithmic problem. I give you the problem statement and a list of existing key points.
- You MUST NOT give me any key point that is already in the list of existing key points.
- You MUST NOT provide any solution or answer to the problem.
- You MUST identify a new key point that is relevant to the problem.
- You MUST NOT include any extraneous text that is not directly part of or relevant to the new thought.
- You MUST format the new key point by surrounding it with the following tags: key{{YOUR_NEW_KEY_POINT_HERE}}key
- You MUST write the key point in a way that it can be included in a triple-quoted string.

Here is an example:

Problem
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Key points:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
New key point:
key{{The average speed of the train is calculated by dividing the distance traveled by the time taken}}key

Please find a new key point for the following problem:
Problem:
{Problem}
Objective:
{Objective}
Existing key points:
{Key_points}
New key point:
"""

validate_likelihood_of_key_point_prompt = """
Help me evaluate the likelihood of a new key point for an algorithmic problem.
- You MUST provide a SURE/LIKELY/UNLIKELY/NO as your final answer.
- You MUST NOT provide any solution or answer to the problem.
- You MUST format the response so that it can be included in a triple-quoted string.
- IF the key point is certain, you MUST respond with SURE.
- IF the key point is highly probable, you MUST respond with LIKELY.
- IF the key point is improbable, you MUST respond with UNLIKELY.
- IF the key point is false, you MUST respond with NO.

Here is an example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Key points:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Key point to be evaluated:
- The average speed of the train is calculated by dividing the distance traveled by the time taken
Answer:
SURE

Here is another example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Key points:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Key point to be evaluated:
- The average speed of the car is calculated by dividing the time take by the distance traveled
Answer:
NO

Here is another example:
Problem:
A train travels 200 kilometers in 2 hours. What is the average speed of the train?
Key points:
- The train travels a distance of 200 kilometers
- The train travels for 2 hours
Key point to be evaluated:
- The average speed of the car is calculated by dividing one value by the other
Answer:
LIKELY

Please evaluate the likelihood of the following key point for the given problem:
Problem:
{Problem}
Objective:
{Objective}
Key points:
{Key_points}
Key point to be evaluated:
{Eval_key_point}
"""