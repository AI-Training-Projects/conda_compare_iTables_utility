import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell
from difflib import unified_diff
from datetime import datetime  # Add import for datetime
import os  # Add import for os

# Function to compare cells
def compare_cells(cell1, cell2):
    diff = list(unified_diff(cell1.splitlines(), cell2.splitlines(), lineterm=''))
    return '\n'.join(diff)

def compare_notebooks(file1, file2):
    # Load the two notebooks
    with open(file1) as f:
        nb1 = nbformat.read(f, as_version=4)

    with open(file2) as f:
        nb2 = nbformat.read(f, as_version=4)

    # Compare the notebooks cell by cell
    differences = []
    for i, (cell1, cell2) in enumerate(zip(nb1.cells, nb2.cells)):
        if cell1['cell_type'] == cell2['cell_type']:
            if cell1['source'] != cell2['source']:
                diff = compare_cells(cell1['source'], cell2['source'])
                differences.append(f"Cell {i} differences:\n{diff}\n")
        else:
            differences.append(f"Cell {i} type mismatch: {cell1['cell_type']} != {cell2['cell_type']}\n")

    # Create a new notebook with the differences
    new_nb = new_notebook()
    new_nb.cells.append(new_markdown_cell("# Differences between Notebooks"))

    if differences:
        for diff in differences:
            new_nb.cells.append(new_markdown_cell(diff))
    else:
        new_nb.cells.append(new_markdown_cell("No differences found."))

    # Save the new notebook with datetime stamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")  # Generate timestamp
    output_filename = f'Notebook_Diffs_REPORTER_OUTPUT_{timestamp}.ipynb'  # Create filename with timestamp
    with open(output_filename, 'w') as f:
        nbformat.write(new_nb, f)
    
    # Output success message
    output_path = os.path.abspath(output_filename)
    print(f"Comparison successful!\nOutput file: {output_filename}\nLocation: {output_path}")

if __name__ == "__main__":
    file1 = 'Compare Conda Virtual Environments Visually_v2024.12.28 copy.ipynb'
    file2 = 'Compare Conda Virtual Environments Visually_v2024.12.28.ipynb'
    compare_notebooks(file1, file2)

