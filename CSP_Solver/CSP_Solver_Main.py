import datetime
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cpmpy as cp
import numpy as np

from HelperFunc.AuxiliaryFunctions import check_folder_exists, get_filepath_Json, save_impossible_solution_json, printTimestampDiff
from HelperFunc.log_Message import logMessage
from CSP_Solver.save_CSP_result_json import save_CSP_result_json
import CSP_Solver_Variables as cv
from inputMapsLibrary import *
from probecardLibrary import probecardDict

from SerialTestSettings import assembleTestList

def CSP_Solver_Main(inputMap, 
                      probecard,
                      inputMapFilepath,
                      probecardName,
                      objectiveFunction,
                      save_folder, 
                      saveResult = False,
                      debugPrint = False,
                      versionID = None,
                      penalty = 2,
                      name_addition = "",
                      max_time_in_seconds = 86400, # 24h
                      upBound = None,
                      lowBound = None,
                      hints = [],
                      parallelWorkers = 8
                      ):

    start_time = datetime.datetime.now()
    logMessage(f"Start CSP_Solver | {objectiveFunction} | File: {inputMapFilepath.rsplit('/')[-1]} | PC: {probecardName} | {max_time_in_seconds} Max solution Time")

    check_filepath = get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition=name_addition)
    if(check_folder_exists(check_filepath) == False): raise Exception(f"The save folder '{os.path.dirname(check_filepath)}' does not exist.")

    # Define Limits of normal Shape
    num_rows, num_cols = inputMap.shape
    xl, xu = 0, num_rows
    yl, yu = 0, num_cols
    dieCount = sum( (inputMap[i, j] == 1) for i in range(num_rows) for j in range(num_cols))

    probecardPos = cp.IntVar( 0, 1, shape = inputMap.shape, name = "pPos" )
    touchCount = cp.IntVar( 0, len(probecard), shape = inputMap.shape, name = "tCount" )

    touchSum = cp.IntVar( dieCount, dieCount * len(probecard), name = "tSum" )
    
    print("DieCount:", dieCount)

    # Creating Model
    model = cp.Model()
    
    # Condition 1: Only permissible touchdowns - List is 0 for allowed space. 1 for not allowed
    model += [  probecardPos[x, y] == 0
          for x in range(xl, xu) 
          for y in range(yl, yu) 
          if any( x+p[0] > xu - 1 for p in probecard ) or any( x+p[0] < 0 for p in probecard ) or
            any( y+p[1] > yu - 1 for p in probecard ) or any( y+p[1] < 0 for p in probecard ) or 
            any( inputMap[x+p[0], y+p[1]] == 0 for p in probecard )
            ]
                # Bei (2,6)... p[0] = 2 | p[1] = 6 
                # xu - 1 because range (0,6) will exclude the 6. We just want to check until 6 not inclusive
    if(debugPrint): logMessage('Added Condition 1.')

    # Condition 2: for every position, the number of touchdowns has to be calculated 
        # -> Take the sum for every cell of all probecard options that could touch this die
    model += [ touchCount[x, y] == sum( probecardPos[(x-p[0]), (y-p[1])] for p in probecard if x-p[0]>=xl and y-p[1]>=yl and x-p[0]<xu and y-p[1]<yu)
                for x in range(xl, xu) 
                for y in range(yl, yu) 
            ]
    if(debugPrint): logMessage('Added Condition 2.')

    ################ TDC MIN Overall
    # touchMax = cp.sum(touchCount[x][y] for x in range(xl, xu) for y in range(yl, yu))

    # Condition 3: Every must-test die is touched at least once
    model += [ touchCount[x, y] >= 1
                for x in range(0, num_rows) 
                for y in range(0, num_cols)
                if(inputMap[x][y] == 1)
            ]
    if(debugPrint): logMessage('Added Condition 3.')

    # Condition 4: Calculate touchSum
    model += [ touchSum == sum( touchCount[x, y]
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                        if inputMap[x][y] == 1 ) ]

    # Define objective functions
    # Objective function TouchSum: Minimize the sum of all touchdown counts of must-touch dies
    if objectiveFunction == "TouchSum":
        objective = cp.IntVar( dieCount, dieCount * len(probecard), name = "tSum" )
        model += [ touchSum <= objective ]

    #Objective function LexTouch: Transform lexicographic order into a single value for comparison
    #   => in this implementation very ineffective, should be rewritten   
    #       (eg possible with calculating touch max, then number in touch max, then number in touch max -1 , ... with previous results as additional constraints)
    if objectiveFunction == "LexTouch":
        touchList = cp.IntVar(0, dieCount, shape = len(probecard), name = "tList")
        # Condition 3: touchList counts occurrances of different touch counts in lexicographical order
        ############### Max Tdc per Die -> Min
        model += [ [touchList[i] == sum( (touchCount[x, y] == i+1)
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                    if inputMap[x, y] == 1 )]
                for i in range(touchList.shape[0])
            ]
        
        if(debugPrint): logMessage('Added touchList definition.')

        model.minimize( sum(touchList[i] * pow(dieCount, i) for i in range(touchList.shape[0])) ) 

    # currently preferred objective function: multiple touchdowns are penalized with an exponentially growing value
    if objectiveFunction == "PenaltySum":
        """touchPenalty = cp.IntVar( 0, pow(penalty, len(probecard)), shape = inputMap.shape, name = "penalty")
        model += [ ( (touchCount[x, y] != i) or (touchPenalty[x, y] == pow(penalty, i-1)) )
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                    for i in range(1, len(probecard)+1)
                    if inputMap[x, y] == 1  ]

        objective = cp.IntVar( dieCount, pow(penalty, len(probecard)) * dieCount, name = "pSum")
        model += [ objective >= sum( touchPenalty[x, y]
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                    if inputMap[x, y] == 1 ) ]"""

        objective = cp.IntVar( dieCount, pow(penalty, 2) * dieCount, name = "pSum")
        model += [ objective >= sum( (touchCount[x, y] == i) * pow(penalty, i-1)
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                    for i in range(1, len(probecard)+1)
                    if inputMap[x, y] == 1 ) ]

    if objectiveFunction == "TouchMax":
        objective = cp.IntVar(1, len(probecard), name = "tMax")
        # Condition 7: touchMax is an upper bound of all touchCounts 
        model += [ objective >= touchCount[x, y]
                    for x in range(xl, xu) 
                    for y in range(yl, yu) 
                        if inputMap[x][y] == 1 
            ]
        
        if(debugPrint): logMessage('Added TouchMax bound.')

    if not objectiveFunction == "LexTouch":
        model.minimize(objective)

    """# Condition 5: Input Map with Value 0 CANNOT be touched
        # => Condition is implied by Condition 1 & touchCount of don't-Touch is not added into objectives by default
    model += [ touchCount[x, y] == 0  
            for x in range(0, num_rows) 
            for y in range(0, num_cols)
            if(inputMap[x][y] == 0)
        ]
    if(debugPrint): logMessage('Added Condition 5')""" 

    # Add upper / lower limits for objective value, if they are known
    if upBound is not None:
        model += [objective <= upBound]

    if lowBound is not None:
        model += [objective >= lowBound]

    # Add hints for all high values from the heat maps
    solver = cp.solvers.CPM_ortools(model)
    hintVar, hintVal = [], []
    for (h_x, h_y) in hints:
        hintVar.append([probecardPos[h_x, h_y]])
        hintVal.append([1])

    if len(hintVar) > 0: solver.solution_hint(hintVar, hintVal)

    if(debugPrint): logMessage('Solving Model')
    start_solve_time = datetime.datetime.now()
    
    solver.solve(max_time_in_seconds = max_time_in_seconds, log_search_progress=debugPrint, num_search_workers = parallelWorkers) # , num_search_workers = parallelWorkers
    #solver.solve() # No time limit

    if(debugPrint): logMessage('Model Solved')
    ### MODEL DONE
    model_status = solver.status()
    objBound = solver.ort_solver.BestObjectiveBound()

    print("Bound", objBound)

    if(debugPrint): 
        print("Model Status:", model_status, " ID: ", model_status.exitstatus.value)

        """print("Touches:")
        for line in probecardPos:
            line = [l.value() for l in line]
            print(line)

        print("\nCounts")
        tCounts = touchCount.value()
        for line in tCounts:
            print(line)"""

    # ExitStatus: 2 is OPTIMAL | 3 ist FEASIBLE 
    # IF NO SOLUTION WAS FOUND -> Save Impossible Flag
    if not (model_status.exitstatus.value == 2 or model_status.exitstatus.value == 3):
        printTimestampDiff(start_time, f"No solution Possible - is {model_status.exitstatus.name}/n")
        if saveResult:
            save_impossible_solution_json(get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition=name_addition), versionID,
                    message = f"{model_status.exitstatus.name} - Timelimit: {max_time_in_seconds} sec - Best objective value lower bound: {objBound}")
        return None

    # print("Best Objective Value: ", solver.objective_value())
    # print(str(get_TD_count_dict_mandatory(inputMap, touchCount.value())))

    # Always Print Solution Rating?
    result_dict = get_TD_count_dict_mandatory(inputMap, touchCount.value())
    tdLocationsList = list(zip(*np.where(probecardPos.value() >= 1)))

    printTimestampDiff(start_time, f" - Total Time | Result: {result_dict} | TDSum: {touchSum.value()} | td_Count: {tdLocationsList.__len__()}| objective value: {solver.objective_value()}")
    
    # SAVE RESULT TO LOOK AT IT for bigger Matrix if outputSaveLocation is set
    if saveResult:
        inputMapFilepath = inputMapFilepath.replace("\\", "/")
        result_dict = get_TD_count_dict_mandatory(inputMap, touchCount.value())

        save_CSP_result_json(saveFilePath=get_filepath_Json(inputMapFilepath, probecardName, save_folder, name_addition=name_addition),
                             inputMapFilepath = inputMapFilepath,
                             probecardName=probecardName,
                             touchdownMap=touchCount.value(), 
                             site1_map=probecardPos.value(),
                             tdLocationsList = tdLocationsList,
                             td_sum=touchSum.value(),
                             result_dict=result_dict,
                             objectiveFunction = objectiveFunction,
                             save_folder = save_folder,
                             versionID=versionID,
                             totalTime = (datetime.datetime.now() - start_time),
                             solve_time = (datetime.datetime.now() - start_solve_time),
                             is_Optimum = model_status.exitstatus.value == 2,
                             objBound = objBound
                             )
        
    # Linebreak when we are DONE with Function
    print()
     

def get_TD_count_dict_mandatory(inputMap, touchdown_map):
    filtered_values = touchdown_map[np.where(touchdown_map != 0) and np.where(inputMap == 1)]
    unique_values, counts = np.unique(filtered_values, return_counts=True)
    return dict(zip(unique_values, counts))
    

if __name__ == '__main__':
    testList = assembleTestList() 

    if cv.serializedTestFlag:
        for (inputMapFilepath, SAVE_FOLDER, probecard_size, objLimit, hintList) in testList:
            filepath = get_filepath_Json(inputMapFilepath, probecard_size, SAVE_FOLDER, name_addition=cv.name_addition)
            if(check_folder_exists(filepath) == False): raise Exception(f"The save folder '{os.path.dirname(filepath)}' does not exist.")

            curr_inputMap =  np.loadtxt(inputMapFilepath, dtype=int)  #2D np Array of InputMap
            # probecard must be flipped: probecards are presented in x-y fashion, but wafer is loaded as a y-x matrix
            curr_probecard = np.array([(x[1], x[0]) for x in probecardDict[probecard_size]])
            

            # Solver Options: TouchSum TouchMax PenaltySum LexTouch
            CSP_Solver_Main(curr_inputMap, curr_probecard, inputMapFilepath, probecard_size, cv.objFunction, 
                            SAVE_FOLDER, saveResult=True, debugPrint=cv.debugFlag, versionID=cv.curr_versionID, name_addition=cv.name_addition, 
                            max_time_in_seconds=cv.max_time_in_seconds, upBound = objLimit, hints = hintList, parallelWorkers = cv.solverCount) 

    else:
        filepath = get_filepath_Json(cv.inputMapFilepath, cv.probecard_size, cv.SAVE_FOLDER, name_addition=cv.name_addition)
        if(check_folder_exists(filepath) == False): raise Exception(f"The save folder '{os.path.dirname(filepath)}' does not exist.")

        curr_inputMap =  np.loadtxt(cv.inputMapFilepath, dtype=int)  #2D np Array of InputMap
        # probecard must be flipped: probecards are presented in x-y fashion, but wafer is loaded as a y-x matrix
        curr_probecard = np.array([(x[1], x[0]) for x in probecardDict[cv.probecard_size]])
        CSP_Solver_Main(curr_inputMap, curr_probecard, cv.inputMapFilepath, cv.probecard_size, cv.objFunction, 
                            cv.SAVE_FOLDER, saveResult=True, debugPrint=cv.debugFlag, versionID=cv.curr_versionID, name_addition=cv.name_addition, 
                            max_time_in_seconds=cv.max_time_in_seconds, upBound = cv.objLimit, hints = cv.hintList, parallelWorkers = cv.solverCount) 