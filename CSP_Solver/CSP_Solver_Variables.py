# This file contains the settings of the CSP solver as global variables
## name strings for the output log
OUTPUT_RESULTMAP_NAME = "ResultMap.txt"
OUTPUT_TOUCHDOWNPOS_NAME = "TouchdownPos.txt"
name_addition = "PenaltySum_CSP_Final"

## ID of the current program version to avoid overwriting existing data (currently inactive)
curr_versionID = 5

## objective function for the solver
objFunction = "PenaltySum"  # Solver Options: TouchSum TouchMax PenaltySum LexTouch

## number of parallel workers for the ensemble solver cpmpy
solverCount = 32

## Maximum calculation time for the cpmpy solver (after preprocessing)
max_time_in_seconds = 86400   # 7200 - 2 hours | 18000 - 5 hours | 28800 - 8 hours | 36000 - 10 hours | 43200 - 12 hours | 64800 - 18 hours | 86400 - 24 hours | 129600 - 36 hours

## flag to enable various debugging output (includes more detailed output of the cpmpy solver)
debugFlag = True