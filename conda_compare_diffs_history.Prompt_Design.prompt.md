# Conda Comparison Tools Prompt

- Created_On: 2024.11.24
- Created_By: Rich Lysakowski

## Conda tools 

I want to compare and see the differences between these user-named two enviroments with respect to their packages, their revision histories, and the installation commands used to build them . If there is no a single conda command line to do this then give me a Python program to report on these things.

## Copilot Clarifying Questions

- Q1. Environment Names: Are "PDF_AI_tools" and "PDF_AI_Tools" the exact names of the two conda environments you wish to compare?

- Q1-Answer. No they are not the exact same.  When I run the command  "conda env list", they show up as separate environments.

- Q2. Comparison Scope: Do you want the comparison to include both the list of installed packages with their versions and the installation commands used to build each environment?

- Q2-Answer.  Yes I want this comparison report as a text file with a timestamped name like this "conda_diffs_{env1}_{env2}_{datetime}.txt

- Q3. Revision History: Do you want the comparison to include the revision history of the packages in each environment?

- Q3-Answer. Yes I want this comparison report to include the revision history of the packages in each environment.

- Q4. Python Program: Do you want the comparison to be done using a Python program?

# PROMPT: 
Modify the entire code just generated to use the command line syntax python "conda_diffs_2envs_3ways.py env1 env2".  Set the default output_folder in the main clause to equal this folder "C:/Users/PowerUser/Desktop/Windows_System_Reports" and then use output_folder in the main() function call in the main clause.   

# PROMPT: Fix garbled generated code ouput formatting.
Your code output is garbled formatting that is unusable !!
You have not been formatting your generated code correctly lately, and this makes a lot of unecessaray work for me.

Make the final result a downloadable Python file.  

