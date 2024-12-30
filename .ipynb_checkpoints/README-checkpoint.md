# Project Name: ***News API with Voice Output***

## Project & Work Product Description: 
### Project Goals 
 - Learn how to apply the iTables package.
 - Create a reusable tool to help me identify the "best" conda environment for a future project.
 - Make sure the voice parts work

**Updated: 2024.12.30**

### Description of Business Problem:
    ***Short Paragraph description of what problem(s) you are trying to solve, things you are learning, or value you want to create.***

I want a tool to visually compare and view the differences between these user-named two enviroments with respect to their packages, their revision histories, and the installation commands used to build them. There was not a single conda command line to do this, so we created a Python program to report on conda environment histories.


### Solution Design (high-level):

- Use Jupyter NB for initial graphical user interface.
- Use iTables package to have interactive Pandas dataframe that sorts, filters and paginates rows.


### Solution Code Description: 
    •	The code (to help users understand it.)
    •	Hyperlinks to actual complete code  

Three primary functions to analyze and display the differences and similarities of two different conda environments.  

## Application Use: ***(Instructions for How to Use The Software)*** 
    If your application applies to multiple use cases, list and briefly describe each major use case. 

## Description of Solution:
    •	Software functions for solving problem(s) step by step.
    •	Workflow diagram of future ("TO-BE") state (improved processes from your solution).
    •	"Minimum Viable Product" (MVP) 1.0 delivered.  (V1.x delivered beyond MVP V1.0?)
    •	Later MVP, i.e., v2, v3, vN+ functionality to be delivered? 
            • additional requirements, GUI, usability, etc. for later versions

### Application Use - ***Tips & Tricks***:    

    If it is not obvious or documentation is not built into the user interface (or written in a Jupyter Notebook), then briefly describe each major use case.  Minor variations can be left out. 
Additional Important Guidelines for Others to Use Your Work Product:

    If there are other important things you learned or know from using, applying, or developing your project code, then please let others know.  This can save people hours or days of time. 
    
    This can include details on any aspect of usage, including installation, dependencies of OS, platform, package dependencies, data source limitations, or simply Tips & Tricks for new users.  
    

## Lessons Learned: [optional here, can be put at the end.]

[ Hyperlinks to more detailed project description information can be linked to documents in subfolders in the github repository. ]:

## Installation:

    Step-by-step instructions for OTHERS to install, set-up, use, re-use, and apply your software:   

    Instructions to get your solution working:

    Installation: 
    Software packages and tools:
        Configuration, Input and output folder structure, 
        data sets, URLs, etc.

# POST YOUR GITHUB HOME PAGE

When finished editing your home page content in Jupyter Notebook: 

    1) GO TO JUPYTER NOTEBOOK `FILE` MENU
    2) Select `Download As...` Menu
    3) Save as `Markdown`
    4) Rename this file to simply `README.md`.
    5) Move this file to your `https://www.github.com/accountname/YOUR_PROJECT_REPOSITORY` repository.
    6) Replace your existing `readme.md` file with this one.  (You may be required to log out and log back in.)
    7) Your new `readme.md` file should appear in your FOR THIS PROJECT.
    8) Verify that all FOLDER OR REMOTE REPOSITORY links correctly open from ***THIS*** PROJECT HOME PAGE.
    
***DELETE THESE INSTRUCTIONS WHEN FINISHED:***

#### Example of how to display Python code properly highlighted.

```python
import yfinance as yf

msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data
hist = msft.history(period="max")
```


