# OVERVIEW
This is the subfolder containing all programs for the CSP solver. 
To run the solver on the predefined instances (from SerialTestSettings), run **python CSP_Solver_Main**

## Organization
This repository is organized as follows:
-*CSP_Solver_Main*: This file contains the main loop of the solution algorithm and has to be run to produce solutions. It produces the CSP model and handles the output of the cpmpy solver. 
-*CSP_Solver_Variables*: Various parameters for the *CSP_Solver_Main*.
-*SerialTestSettings*: Specifies which problem instances are to be solved.

