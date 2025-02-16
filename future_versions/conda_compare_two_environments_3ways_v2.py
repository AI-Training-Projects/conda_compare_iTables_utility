"""
Deep Compare Two Conda Environments

Compares two user-named Conda environments to identify differences in their installed packages, revision histories, and installation commands.
The comparison report is saved as a timestamped text file named "conda_diffs_{env1}_{env2}_{datetime}.txt" in the specified output folder.

Dependencies:
- conda

Ensure conda is installed and accessible in your system's PATH.

Usage:
1. Open a terminal or command prompt.
2. Run the script with the two environment names as arguments:
   python conda_diffs_2envs_3ways.py PDF_AI_tools PDF_AI_Tools
3. The comparison report will be saved in "C:/Users/PowerUser/Desktop/Windows_System_Reports" with a timestamped filename.
4. Check the "compare_conda_envs.log" file in the output folder for detailed logs of the operations performed.

Generated by Rich Lysakowski
"""

import os
import subprocess
import datetime
import logging
import sys

def setup_logging(output_folder: str) -> None:
    """
    Sets up logging to both a file and the console.

    Args:
        output_folder (str): The directory where the log file will be saved.
    """
    log_file = os.path.join(output_folder, "compare_conda_envs.log")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    # Generated by Rich Lysakowski

def get_conda_info(env_name: str) -> dict:
    """
    Retrieves Conda environment information including packages and revision history.

    Args:
        env_name (str): The name of the Conda environment.

    Returns:
        dict: A dictionary containing packages and revision history.
    """
    try:
        # Get list of installed packages
        package_list = subprocess.check_output(
            ["conda", "list", "--name", env_name, "--export"],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip().split('\n')

        # Get revision history
        revision_history = subprocess.check_output(
            ["conda", "history", "--name", env_name],
            stderr=subprocess.STDOUT
        ).decode("utf-8").strip()

        return {
            "packages": set(package_list),
            "revision_history": revision_history
        }
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to retrieve information for environment \"{env_name}\". Error: {e.output.decode('utf-8')}")
        return {
            "packages": set(),
            "revision_history": "Unavailable"
        }
    # Generated by Rich Lysakowski

def compare_packages(env1_packages: set, env2_packages: set) -> dict:
    """
    Compares the packages of two Conda environments.

    Args:
        env1_packages (set): Packages from the first environment.
        env2_packages (set): Packages from the second environment.

    Returns:
        dict: A dictionary containing added and removed packages.
    """
    added = env2_packages - env1_packages
    removed = env1_packages - env2_packages
    return {
        "added": added,
        "removed": removed
    }
    # Generated by Rich Lysakowski

def generate_install_commands(env_name: str) -> str:
    """
    Generates the installation commands used to build a Conda environment.

    Args:
        env_name (str): The name of the Conda environment.

    Returns:
        str: The installation commands as a string.
    """
    try:
        env_export = subprocess.check_output(
            ["conda", "env", "export", "--name", env_name],
            stderr=subprocess.STDOUT
        ).decode("utf-8")
        return env_export
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to export environment \"{env_name}\". Error: {e.output.decode('utf-8')}")
        return "Unavailable"
    # Generated by Rich Lysakowski

def main():
    """
    Main function to compare two Conda environments and generate a report.
    """
    if len(sys.argv) != 3:
        print("Usage: python conda_diffs_2envs_3ways.py env1 env2")
        sys.exit(1)

    env1 = sys.argv[1]
    env2 = sys.argv[2]

    output_folder = "C:/Users/PowerUser/Desktop/Windows_System_Reports"
    os.makedirs(output_folder, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"conda_diffs_{env1}_{env2}_{timestamp}.txt"
    report_path = os.path.join(output_folder, report_filename)

    setup_logging(output_folder)
    logging.info(f"Starting comparison between \"{env1}\" and \"{env2}\".")

    env1_info = get_conda_info(env1)
    env2_info = get_conda_info(env2)

    package_comparison = compare_packages(env1_info["packages"], env2_info["packages"])

    env1_install = generate_install_commands(env1)
    env2_install = generate_install_commands(env2)

    try:
        with open(report_path, "w", encoding="utf-8") as report_file:
            report_file.write("Conda Environment Comparison Report\n")
            report_file.write(f"Environments: \"{env1}\" vs \"{env2}\"\n")
            report_file.write(f"Generated on: {datetime.datetime.now()}\n\n")

            report_file.write("=== Package Differences ===\n")
            report_file.write(f"**Packages Added in {env2}:**\n")
            for pkg in sorted(package_comparison["added"]):
                report_file.write(f"- {pkg}\n")
            report_file.write(f"\n**Packages Removed from {env1}:**\n")
            for pkg in sorted(package_comparison["removed"]):
                report_file.write(f"- {pkg}\n")

            report_file.write("\n=== Revision Histories ===\n")
            report_file.write(f"**{env1} Revision History:**\n")
            report_file.write(env1_info["revision_history"] + "\n\n")
            report_file.write(f"**{env2} Revision History:**\n")
            report_file.write(env2_info["revision_history"] + "\n\n")

            report_file.write("=== Installation Commands ===\n")
            report_file.write(f"**{env1} Installation Commands:**\n")
            report_file.write(env1_install + "\n\n")
            report_file.write(f"**{env2} Installation Commands:**\n")
            report_file.write(env2_install + "\n\n")

        logging.info(f"Comparison report generated at \"{report_path}\".")
    except Exception as e:
        logging.error(f"Failed to write the comparison report. Error: {e}")

    print(f"Comparison report available at \"{report_path}\"")
    # Generated by Rich Lysakowski

if __name__ == "__main__":
    main()
    # Generated by Rich Lysakowski