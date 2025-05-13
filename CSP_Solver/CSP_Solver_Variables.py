import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from inputMapsLibrary import *

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
solverCount = 6

## Maximum calculation time for the cpmpy solver (after preprocessing)
max_time_in_seconds = 86400   # 7200 - 2 hours | 18000 - 5 hours | 28800 - 8 hours | 36000 - 10 hours | 43200 - 12 hours | 64800 - 18 hours | 86400 - 24 hours | 129600 - 36 hours

## flag to enable various debugging output (includes more detailed output of the cpmpy solver)
debugFlag = True

# flag to enable serial testing of all files in SerialTestSettings, otherwise test the instance specified below
serializedTestFlag = True
inputMapFilepath = filepath_51x51_Complete 
SAVE_FOLDER = "Data_CSP_Complete"
probecard_size = "2x16" 
objLimit = 1800
hintList = []