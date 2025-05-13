# OVERVIEW
This is the subfolder containing the output files for the problem instances with CSP.

## Organization
This subfolder is organized in 3 layers. In the first layer, the output files are separated by the problem type. In the next layer, the instances are categorized by wafer diameter, and in the last layer, the individual files are separated by probe card shape.

## Encoding
The output log contains various pieces of information about the produced solution. These encompass:
-*is_optimum*: flag whether the CSP solver proved optimality for this solution
-*score*: objective function value for this solution
-*rating*: histogram of the touchdown counts
-*td_count*: total number of touchdowns
-*time*: total time the program was running (in seconds)
-*solveTime*: time the CSP solver was running after preprocessing
-*objective*: chosen objective function
-*Objective value lower bound*: lower bound on the objective value as calculated by the CSP solver
