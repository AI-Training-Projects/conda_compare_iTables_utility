#!/usr/bin/env python3

"""
File: conda_compare_v7.py
Original From: https://gist.github.com/bt-/7bfd5e7f663cbda909814947c8347d1c

Quicky script that compares two conda environments.
Handy for debugging differences between two environments.

AUTHOR: Christopher H. Barker Chris.Barker@noaa.gov
LICENSE: Public domain -- do with it what you will
(But it would be nice to give me credit if it helps you)

UPDATE: Ben Taylor
I changed the print statements and had to add
a conversion from bytes to string for Python 3.
I just ran this in Python 3.7.3 and seemed to work well.

UPDATE: 2024-11-25
Updated by Rich Lysakowski
- Updated to use pandas and make the output a text file
- Updated to use multi-index DataFrames for better display
- Added proper column headers and formatting
- Simplified the comparison logic
- Enhanced table formatting with clear separators and borders
- Added environment statistics comparison
- Standardized table widths and formatting
"""

import sys
import subprocess
import pandas as pd
from datetime import datetime

def get_env_list(env_name):
    """Get list of packages from conda environment."""
    cmd = "conda list -n " + env_name
    print(cmd)
    pkg_list = subprocess.check_output(cmd, shell=True)
    pkg_list = pkg_list.decode('utf-8')
    
    pkgs = {}
    for line in pkg_list.split('\n'):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        parts = line.split()
        pkg, version, build = parts[:3]
        channel = "pip" if build == '<pip>' else ("defaults" if len(parts) < 4 else parts[3])
        pkgs[pkg] = {'version': version, 'build': build, 'channel': channel}
    
    return pkgs

def get_env_statistics(env_name):
    """Get environment statistics using conda list --revisions."""
    cmd = f"conda list --revisions -n {env_name}"
    try:
        revisions = subprocess.check_output(cmd, shell=True).decode('utf-8').splitlines()
        # First line is header, last line has latest info
        revision_count = len(revisions) - 1  # Subtract header line
        first_revision = revisions[1].split()  # First revision after header
        latest_revision = revisions[-1].split()
        
        # Get current package count
        pkg_count_cmd = f"conda list -n {env_name} | grep -v '^#' | wc -l"
        current_pkg_count = subprocess.check_output(pkg_count_cmd, shell=True).decode('utf-8').strip()
        
        return {
            'Date_First_Created': first_revision[1],
            'Current_Packages_Count': current_pkg_count,
            'Revision_Count': revision_count,
            'Latest_Revision_Date': latest_revision[1]
        }
    except subprocess.CalledProcessError:
        return {
            'Date_First_Created': 'Unknown',
            'Current_Packages_Count': 'Unknown',
            'Revision_Count': 'Unknown',
            'Latest_Revision_Date': 'Unknown'
        }

def create_comparison_dataframes(env1_name, env1, env2_name, env2):
    """Create multi-index DataFrames for package comparison."""
    # Create initial DataFrames
    df1 = pd.DataFrame.from_dict(env1, orient='index').reset_index()
    df2 = pd.DataFrame.from_dict(env2, orient='index').reset_index()
    
    # Rename columns
    df1.columns = ['pkg_name', 'pkg_version', 'pkg_build', 'channel']
    df2.columns = ['pkg_name', 'pkg_version', 'pkg_build', 'channel']
    
    # Create multi-index columns
    top_level = ['Package'] + [env1_name] * 3 + [env2_name] * 3
    bottom_level = ['Name', 'Version', 'Build', 'Channel', 'Version', 'Build', 'Channel']
    column_index = pd.MultiIndex.from_arrays([top_level, bottom_level])
    
    # Merge dataframes
    merged_df = df1.merge(df2, on='pkg_name', how='outer', 
                         suffixes=(f'_{env1_name}', f'_{env2_name}'))
    merged_df = merged_df.sort_values('pkg_name')
    
    # Create three views
    same_versions = merged_df[
        (merged_df[f'pkg_version_{env1_name}'] == merged_df[f'pkg_version_{env2_name}']) &
        (merged_df[f'pkg_build_{env1_name}'] == merged_df[f'pkg_build_{env2_name}']) &
        (merged_df[f'channel_{env1_name}'] == merged_df[f'channel_{env2_name}'])
    ].copy()
    
    diff_versions = merged_df[
        (merged_df[f'pkg_version_{env1_name}'].notna()) & 
        (merged_df[f'pkg_version_{env2_name}'].notna()) &
        ((merged_df[f'pkg_version_{env1_name}'] != merged_df[f'pkg_version_{env2_name}']) |
         (merged_df[f'pkg_build_{env1_name}'] != merged_df[f'pkg_build_{env2_name}']) |
         (merged_df[f'channel_{env1_name}'] != merged_df[f'channel_{env2_name}']))
    ].copy()
    
    unique_pkgs = merged_df[
        merged_df[f'pkg_version_{env1_name}'].isna() | 
        merged_df[f'pkg_version_{env2_name}'].isna()
    ].copy()
    
    # Process each DataFrame
    dataframes = []
    for df in [same_versions, diff_versions, unique_pkgs]:
        df.fillna('~', inplace=True)
        
        # Create the new DataFrame with proper structure
        new_data = {
            ('Package', 'Name'): df['pkg_name'],
            (env1_name, 'Version'): df[f'pkg_version_{env1_name}'],
            (env1_name, 'Build'): df[f'pkg_build_{env1_name}'],
            (env1_name, 'Channel'): df[f'channel_{env1_name}'],
            (env2_name, 'Version'): df[f'pkg_version_{env2_name}'],
            (env2_name, 'Build'): df[f'pkg_build_{env2_name}'],
            (env2_name, 'Channel'): df[f'channel_{env2_name}']
        }
        
        # Create DataFrame with multi-index columns
        df_reshaped = pd.DataFrame(new_data)
        df_reshaped.columns = column_index
        dataframes.append(df_reshaped)
    
    return dataframes[0], dataframes[1], dataframes[2]

def save_comparison_to_file(filename, env1_name, env2_name, env1_stats, env2_stats, 
                          same_vers, diff_vers, unique_pkgs):
    """Save comparison results to file."""
    # Calculate maximum width based on content
    max_width = max(120, len(same_vers.to_string(index=False).split('\n')[0]))
    separator = "=" * max_width
    table_line = "-" * max_width
    
    with open(filename, 'w') as file:
        # Environment Statistics table
        file.write(f"{separator}\n")
        file.write("Environment Comparison Statistics:\n")
        file.write(f"{table_line}\n")
        
        # Create statistics DataFrame
        stats_data = {
            'Environment': [env1_name, env2_name],
            'Date_First_Created': [env1_stats['Date_First_Created'], env2_stats['Date_First_Created']],
            'Current_Packages_Count': [env1_stats['Current_Packages_Count'], env2_stats['Current_Packages_Count']],
            'Revision_Count': [env1_stats['Revision_Count'], env2_stats['Revision_Count']],
            'Latest_Revision_Date': [env1_stats['Latest_Revision_Date'], env2_stats['Latest_Revision_Date']]
        }
        stats_df = pd.DataFrame(stats_data)
        file.write(stats_df.to_string(index=False))
        file.write(f"\n{table_line}\n")
        file.write(f"{separator}\n\n")
        
        # Same versions table
        file.write(f"{separator}\n")
        file.write("Packages in Both Environments with SAME versions:\n")
        file.write(f"{table_line}\n")
        file.write(same_vers.to_string(index=False))
        file.write(f"\n{table_line}\n")
        file.write(f"{separator}\n\n")
        
        # Different versions table
        file.write(f"{separator}\n")
        file.write("Packages in Both Environments with DIFFERENT versions:\n")
        file.write(f"{table_line}\n")
        file.write(diff_vers.to_string(index=False))
        file.write(f"\n{table_line}\n")
        file.write(f"{separator}\n\n")
        
        # Unique packages table
        file.write(f"{separator}\n")
        file.write("Packages in only ONE environment (and NOT the other):\n")
        file.write(f"{table_line}\n")
        file.write(unique_pkgs.to_string(index=False))
        file.write(f"\n{table_line}\n")
        file.write(f"{separator}\n")

def main():
    """Main function to run the comparison."""
    try:
        env1 = sys.argv[1]
        env2 = sys.argv[2]
    except IndexError:
        print("You need to pass the name of two environments at the command line")
        sys.exit(1)

    # Get environment package lists and statistics
    e1 = get_env_list(env1)
    e2 = get_env_list(env2)
    env1_stats = get_env_statistics(env1)
    env2_stats = get_env_statistics(env2)
    
    # Set pandas display options
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.multi_sparse', True)
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    
    # Create and display DataFrame comparisons
    same_vers, diff_vers, unique_pkgs = create_comparison_dataframes(env1, e1, env2, e2)
    
    # Calculate consistent width for all tables
    max_width = max(120, len(same_vers.to_string(index=False).split('\n')[0]))
    separator = "=" * max_width
    table_line = "-" * max_width
    
    # Display Environment Statistics
    print(f"\n{separator}")
    print("Environment Comparison Statistics:")
    print(table_line)
    stats_data = {
        'Environment': [env1, env2],
        'Date_First_Created': [env1_stats['Date_First_Created'], env2_stats['Date_First_Created']],
        'Current_Packages_Count': [env1_stats['Current_Packages_Count'], env2_stats['Current_Packages_Count']],
        'Revision_Count': [env1_stats['Revision_Count'], env2_stats['Revision_Count']],
        'Latest_Revision_Date': [env1_stats['Latest_Revision_Date'], env2_stats['Latest_Revision_Date']]
    }
    stats_df = pd.DataFrame(stats_data)
    print(stats_df.to_string(index=False))
    print(table_line)
    print(f"{separator}\n")
    
    # Display package comparison results
    print(f"{separator}")
    print("Packages in Both Environments with SAME versions:")
    print(table_line)
    print(same_vers.to_string(index=False))
    print(table_line)
    print(f"{separator}\n")
    
    print(f"{separator}")
    print("Packages in Both Environments with DIFFERENT versions:")
    print(table_line)
    print(diff_vers.to_string(index=False))
    print(table_line)
    print(f"{separator}\n")
    
    print(f"{separator}")
    print("Packages in only ONE environment (and NOT the other):")
    print(table_line)
    print(unique_pkgs.to_string(index=False))
    print(table_line)
    print(separator)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'conda_compare_envs_{env1}_{env2}_{timestamp}.txt'
    
    # Save results
    save_comparison_to_file(filename, env1, env2, env1_stats, env2_stats, 
                          same_vers, diff_vers, unique_pkgs)
    print(f"\nFile: {filename} created.")
    print("\nDone.")
    sys.exit(0)

if __name__ == "__main__":
    main()