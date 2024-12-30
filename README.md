# **Visually Compare Two Environments Using Interactive Dataframes - PROD VERSION**

## Project & Work Product Description: 

This Jupyter Notebook provides a tool to visually compare two Python environments using interactive dataframes. It leverages the `iTables` package for interactive table displays and the `packaging` module for comparing package versions using Semantic Versioning.

### Features
- **Interactive Dataframes**: Uses `iTables` for interactive grid displays.
- **Pandas Styling**: Enhances the visualization of environment comparisons.
- **Semantic Versioning**: Utilizes the `packaging` module to compare package versions.

### Project Goals 
 - Learn how to apply the iTables package.
 - Create a reusable tool to help me identify the "best" conda environment for a future project.
 - Make sure the voice parts work

**Updated: 2024.12.30**

### Description of Business Problem:

I wanted a tool to visually compare and view the differences between these user-named two enviroments with respect to their packages, their revision histories, and the installation commands used to build them. There was not a single conda command line to do this, so we created a Python program to report on conda environment histories.


### Solution Design (high-level):

This Jupyter Notebook provides a tool to visually compare two Python environments using interactive dataframes. It leverages the `iTables` package for interactive table displays and the `packaging` module for comparing package versions using Semantic Versioning.

### Usage
1. **Import Required Libraries**:
    - Pandas for data manipulation.
    - `iTables` for interactive table displays.
    - `subprocess` for executing shell commands.
    - `packaging` for version comparison.

2. **Set Options for iTables Displays**:
    - Configure `iTables` options such as `maxBytes`, `maxRows`, `pageLength`, and `lengthMenu` to control the display behavior of dataframes.

3. **Enable Automatic Rendering**:
    - Enable automatic rendering of dataframes with `itables.init_notebook_mode(all_interactive=True)` so that all DataFrames are displayed as interactive iTables without needing to call `itables.show(df)` explicitly.

### Future Enhancements
- Convert the notebook into a single script file or a Streamlit app.
- Generate an output report in HTML format.

### Solution Code Description

#### Functions

- **get_environment_packages(env_name)**:
    - **Description**: Retrieves the list of packages and their versions for a given conda environment.
    - **Parameters**: `env_name` (str) - The name of the conda environment.
    - **Returns**: DataFrame containing package names and versions.

- **compare_environments(env1, env2)**:
    - **Description**: Compares the packages between two conda environments and highlights the differences.
    - **Parameters**: `env1` (str) - The name of the first conda environment.
                    `env2` (str) - The name of the second conda environment.
    - **Returns**: DataFrame showing the comparison results.

- **style_comparison(df)**:
    - **Description**: Applies styling to the comparison DataFrame for better visualization.
    - **Parameters**: `df` (DataFrame) - The DataFrame containing the comparison results.
    - **Returns**: Styled DataFrame.

### Hyperlinks to Support Modules and Packages
- **iTables**: [iTables Documentation](https://mwouts.github.io/itables/)
- **Pandas**: [Pandas Documentation](https://pandas.pydata.org/pandas-docs/stable/)
- **Packaging**: [Packaging Documentation](https://packaging.pypa.io/en/latest/)

### Future Enhancements
- TODO: Convert the notebook into a single script file or a Streamlit app.  Initial version can output text only.  
- Generate an output report in HTML format.
- Create another version that embeds the code into a Streamlit (or Gradio) application.
- 
### Example
To use the notebook version, ensure that `iTables` and `packaging` are installed in your runtime environment. 

Then, run the notebook to compare two Python environments and visualize the differences interactively.

---
## Lessons Learned: 
- iTables is AWESOME, but a little deep, so it needs a few hours to learn all the primary features. 
- **iTables**: [iTables Documentation](https://mwouts.github.io/itables/)


