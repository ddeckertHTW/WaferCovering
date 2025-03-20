import datetime
import json
import numpy as np

from HelperFunc.AuxiliaryFunctions import get_Version_ID_For_Print, is_file_versionID_older, get_result_score

def checkVersionID(versionID):
    if versionID == None:
        return 0
    return versionID

def get_TD_count_percentages_mandatory(count_mandatory_dict):
    total_sum = sum(count_mandatory_dict.values())
    percentage_dict = {key: round((value / total_sum) * 100, 2) for key, value in count_mandatory_dict.items()}
    return percentage_dict
    
def save_CSP_result_json(saveFilePath, inputMapFilepath, probecardName, touchdownMap, site1_map, tdLocationsList, td_sum, result_dict, 
                         objectiveFunction, save_folder, versionID, totalTime, solve_time, is_Optimum = "", objBound = None):
    data = {
        "versionID": checkVersionID(versionID), #"versionID": versionID,
        "is_Optimum": is_Optimum,

        # The final Score
        "score": get_result_score(result_dict),
        "rating": str(result_dict),
        "rating_Percentages": str(get_TD_count_percentages_mandatory(result_dict)), 
        
        "td_Count": tdLocationsList.__len__(),
        "td_Sum": td_sum,

        "time": totalTime,
        "solveTime": solve_time,

        "objective": objectiveFunction,
    }
    if objBound is not None:
        data["Objective value lower bound"] = objBound
    data.update(
        {
            "pcSize": probecardName,
            "inputMap_Name": inputMapFilepath.rsplit('/')[-1], # Just the Name like: 15x15_InputMap.txt OR 15x15_Diagonal_Error_InputMap.txt
            "inputMap_Filepath": (inputMapFilepath.rsplit('/')[-2] + "/" + inputMapFilepath.rsplit('/')[-1]), #Dont include the Base directorys as it changes by device

            "tdMap": touchdownMap,
            "tdLocations": site1_map,
            "tdLocationsList": tdLocationsList,
        })

    #For Printing
    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    #Only save to File, if VersionID is lower. Not if larger or equal. 
    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return
    
    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4, cls=NpEncoder)

    #Make the 2D np Arrays readable in the file by formating
    formatted_json_str = jsonString.replace('[\n            ', '[').replace('\n        ]', ']').replace(',\n            ', ', ')

    # Save file
    with open(saveFilePath, 'w') as f:
        f.write(formatted_json_str)

    print(f"[Saved File] - {save_folder} - {fileName_short}")
    #if(debugPrint): print("Saved File: ", fileName_short)
    


#https://stackoverflow.com/questions/50916422/python-typeerror-object-of-type-int64-is-not-json-serializable
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        #Also the Timestamps or Timedelta
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()  
        if isinstance(obj, datetime.timedelta):
            return obj.total_seconds()  
        return super(NpEncoder, self).default(obj)