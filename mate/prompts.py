# Prompt to extract the main constraints and goal of the problem
extract_constraints_goal_prompt = """
Help me extract and analyze the main constraints and the goal of a math problem.
You MUST provide only one goal.
You MUST derive the constraints from the problem text; deductions and assumptions are not allowed.
You MUST NOT provide any solution or answer to the problem.
You MUST put the constraints in a bullet-point list format, where each constraint starts with an asterisk (*) followed by a hash (#) and a space.

Here is an example:
Problem: 
A car travels 120 miles in 2 hours. What is the average speed of the car?
Main constraints: 
*# The car travels a distance of 120 miles
*# The car travels for 2 hours
Goal:
Calculate the average speed of the car based on the distance traveled and the time taken.

Please provide the main constraints and the goal for the following problem:
{Problem}
"""

# Prompt to correct erros in constraints extracted from a math problem
correct_constraints_prompt = """
Help me correct a constraint extracted from a math problem.
You MUST provide a new constraint that is logically derived from the problem text.
The corrected constraint should be relevant to achieving the goal of the problem.
The corrected constraint should not imply the same as the knwon main constraints.
The corrected constraint should not be the same as the incorrect constraint or known constraints or rephrased version of the same.
You MUST provide ONLY the new corrected constraint.
You can answer with NONE if no other constraint can be deduced.

Here is an example:
Problem: 
The sum of two numbers is 10. The first number is greater than the second number by 2. What are the numbers?
Incorrect constraint: 
The sum of the two numbers is 15
Corrected constraint: 
The sum of the two numbers is 10

Please correct the following constraint for the given problem:
Problem: 
{Problem}
Main constraints:
{Constraints}
Goal:
{Goal}
Incorrect constraint: 
{Incorrect_constraint}
Corrected constraint:
"""

# Prompt to dedcute new constraint from a math problem
deduce_constraint_prompt = """
Help me deduce/formulate a new constraint from a math problem.
You CAN ONLY use the already provided constraints and the problem text to deduce the new constraint.
You MUST provide a new constraint that is logically derived from the problem text and the already provided constraints.
The new contraint should be relevant to achieving the goal of the problem.
You MUST provide ONLY the new constraint.
You MUST NOT provide any solution or answer to the problem.
IF no new constraint can be deduced, please just provide a message saying NONE.
The new constraint should not start with an asterisk (*) followed by a hash (#) and a space.

Here is an example:
Problem: 
A car travels 120 miles in 2 hours. What is the average speed of the car?
Main constraints:
*# The car travels a distance of 120 miles
*# The car travels for 2 hours
Goal:
Calculate the average speed of the car based on the distance traveled and the time taken.
New constraint: 
The average speed of the car is calculated by dividing the distance traveled by the time taken.

Please deduce a new constraint for the following problem:
Problem: 
{Problem}
Main constraints: 
{Constraints}
Goal: 
{Goal}
New constraint:
"""

#Prompt to test if a constrait is valid for a math problem
test_constraint_prompt = """
Help me test if a constraint is valid for a math problem.
You MUST provide a YES or NO as your finale answer.
If a constraint is valid, it should be logically derived from the problem text and the already provided constraints.
If a constraint is true, you should answer YES.
If a constraint is false, you should answer NO.

Here is an example:
Problem: 
A car travels 120 miles in 2 hours. What is the average speed of the car?
Main constraints:
*# The car travels a distance of 120 miles
*# The car travels for 2 hours
Goal:
Calculate the average speed of the car based on the distance traveled and the time taken.
Constraint: 
The average speed of the car is calculated by dividing the time taken by the distance traveled.
Answer: 
NO

Here is another example:
Problem: 
A rectangle has a length of 10 cm and a width of 5 cm. What is the area of the rectangle?
Main constraints:
*# The rectangle has a length of 10 cm
*# The rectangle has a width of 5 cm
Goal:
Calculate the area of the rectangle based on its length and width.
Constraint to be validated: 
The area of the rectangle is calculated by multiplying the length by the width.
Answer: 
YES

Please test the following constraint for the given problem:
Problem:
{Problem}
Main constraints:
{Constraints}
Goal:
{Goal}
Constraint to be validated:
{Constraint}
Answer:
"""

# Prompt to test if the conditions of a math problem are sufficient to achieve the goal
test_sufficiency_prompt = """
Help me test if the conditions of a math problem are sufficient to achieve the goal.
You MUST provide a YES or NO as your final answer.
If the conditions are sufficient to achieve the goal, you should answer YES.
If the conditions are not sufficient to achieve the goal, you should answer NO.

Please test if the following conditions are sufficient to achieve the goal of the problem:
Problem:
{Problem}
Main constraints:
{Constraints}
Goal:
{Goal}
Answer:
"""

# Prompt to generate a step-by-step solution for a math problem
generate_solution_prompt = """
Help me generate a step-by-step solution for a math problem.
You MUST provide a detailed solution with all the necessary steps.
You MUST provide the final answer of the problem with \\boxed tag, if it exists.

Here is the probelma and all the constraints needed to solve it:
Problem:
{Problem}
Main constraints:
{Constraints}
Goal:
{Goal}
Solution:
"""
