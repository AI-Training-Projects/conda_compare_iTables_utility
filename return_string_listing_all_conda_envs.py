"""
Returns a string containing a list of all conda environments, including the active one.
The active environment is marked with a * symbol.
"""

import os

current_env = os.popen("conda env list").read()
print(current_env)

