#!/usr/bin/env python3

"""
# 
File: conda_compare.py
From: https://gist.github.com/bt-/7bfd5e7f663cbda909814947c8347d1c
Date: Created 3 years ago (back from 12.06.2022)

Quicky script that compares two conda environments.
Handy for debugging differences between two environments.

This could be made much cleaner and more flexible -- but it does the job.
Please let me know if you extend or improve it.

AUTHOR: Christopher H. Barker Chris.Barker@noaa.gov
LICENSE: Public domain -- do with it what you will
(But it would be nice to give me credit if it helps you)

UPDATE: Ben Taylor
I changed the print statements and had to add
a conversion from bytes to string for Python 3.
I just ran this in Python 3.7.3 and seemd to work well.
"""

import sys
import subprocess


def get_env_list(env_name):
    cmd = "conda list -n " + env_name
    print(cmd)
    pkg_list = subprocess.check_output(cmd, shell=True)
    pkg_list = pkg_list.decode('utf-8')
    # process the package list
    pkgs = {}
    for line in pkg_list.split('\n'):
        line = line.strip()
        if not line or line[0] == '#':
            continue
        parts = line.split()
        pkg, version, build = parts[:3]
        if build == '<pip>':
            channel = "pip"
        else:
            channel = "defaults" if len(parts) < 4 else parts[3]
        pkgs[pkg] = (version, build, channel)

    return pkgs


def compare_envs(env1, env2):
    pkgs1 = set(env1)
    pkgs2 = set(env2)

    in_both = pkgs1 & pkgs2
    in_one = (pkgs1 ^ pkgs2) & pkgs1
    in_two = (pkgs1 ^ pkgs2) & pkgs2

    diff_version = []
    same_version = []
    for pkg in in_both:
        if env1[pkg] != env2[pkg]:
            diff_version.append(pkg)
        else:
            same_version.append(pkg)

    return in_one, in_two, diff_version, same_version


def print_report(env, pkgs):
    for pkg in pkgs:
        print("{:25}{:10}{:20}{:20}".format(pkg, *env[pkg]))


def print_diff_version(name1, env1, name2, env2, pkgs):
    print("Packages in both, with differnt versions:")
    #print "     {:15}{:10}{:20}{:20}".format("
    for pkg in pkgs:
        print(pkg, ":")
        print( "    {:15}{:10}{:20}{:20}".format(name1, *env1[pkg]))
        print( "    {:15}{:10}{:20}{:20}".format(name2, *env2[pkg]))


if __name__ == "__main__":
    try:
        env1 = sys.argv[1]
        env2 = sys.argv[2]
    except IndexError:
        print ("you need to pass the name of two environments at the commmand line")

    e1 = get_env_list(env1)
    e2 = get_env_list(env2)
    in_one, in_two, diff_version, same_version = compare_envs(e1, e2)

    print("In only", env1)
    print_report(e1, in_one)

    print("\nIn only", env2)
    print_report(e2, in_two)

    print("\nIn both, same version:")
    print_report(e1, same_version)

    print()
    print_diff_version(env1, e1, env2, e2, diff_version)
    
    # Enhance this script to save the output to a file.
    with open('conda_compare_output.txt', 'w') as file:
        file.write(f"In only {env1}\n")
        print_report(e1, in_one, file=file)
        file.write(f"\nIn only {env2}\n")
        print_report(e2, in_two, file=file)
        file.write(f"\nIn both, same version:\n")
        print_report(e1, same_version, file=file)
        file.write(f"\nPackages in both, with differnt versions:\n")
        print_diff_version(env1, e1, env2, e2, diff_version, file=file)

# Now enhance the script output to be more readable by using a Pandas DataFrame for displaying the data.


# Provide one large table showing all packages in each environment side by side, with each of these column: env_name, package name, version, build, and channel.

# Provide a table showing the packages that are in only one environment, with columns for the package name, version, build, and channel.

# Provide a table showing the packages that are in both environments, but with different versions, with columns for the package name, version, build, and channel for each environment.

