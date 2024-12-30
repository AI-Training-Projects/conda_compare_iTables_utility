# Enhancements to conda_compare.py

Updated: 2024.12.27 

## Enhance the selected code to use Pandas Dataframes with iTables and Pandas Styling for highlighting differences.  
Advise whether it will be easiest to implement flawlessly using a Jupyter NB, a Flask web app, or a Streamlit app.    

    Use Pandas Styling Highlighted cells to show same-different packages in the two environments
    Make the grid sortable.  Bring in Dates, Versions, and other columns to compare.
    Make the grid filterable. 
                                      
# Enhance the script output to be more readable by using a Pandas DataFrame for displaying the data.


# DONE: Provide one large table showing all packages in each environment side by side, with each of these column: env_name, package name, version, build, and channel.

# DONE: Provide a table showing the packages that are in only one environment, with columns for the package name, version, build, and channel.

# DONE: Provide a table showing the packages that are in both environments, but with different versions, with columns for the package name, version, build, and channel for each environment.

# PROMPT TO CONSOLIDATE TABLES USING MULTI-INDEX DATAFRAMES

    An even better display would be to use a pandas multi-index dataframes.    
    This could be reduce the total number of dataframes needed from 4 to 3:  

    Update the code to use multi-index dataframe for more efficient table displays so that we reduce the number of tables from 4 to 3.

    [env1]                    ...  [env2]
    [version, build, channel] ...  [version, build, channel], 

# List all packages alphabetically in all three dataframe tables named below.
    1) Packages in both environments with the same versions:
    2) Packages in both environments with different versions:
    3) Packages in only one environment and not the other:  (The rule here is that If a package is not installed in one environment, then show it as "not installed" in that corresponding package column.)

# Install a Better (COOL) Progress Bar: 
    https://github.com/pepelawycliffe/alive-progress

