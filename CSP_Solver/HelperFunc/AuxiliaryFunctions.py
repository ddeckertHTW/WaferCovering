import os
import sys
import datetime
import json
from GlobalConstants import BASE_DATA_FILEPATH, PENALTY_SCORE


scriptFolder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Returns True -> File should not be overwritten, because Version in existing file is higher
# Returns False  -> File should be overwritten, because Version is lower
# If VersionID is None -> Flag to always overwrite -> Ignore and return False 
# Naming Alternative: is_file_versionID_older

#def is_file_versionID_older_Greedy(inputMapFilepath, probecard, new_versionID, save_folder):
def is_file_versionID_older(filepath, new_versionID):
    if(new_versionID == None):
        return False
    
    return check_versionID(filepath, new_versionID)

def check_versionID(json_file_path, new_versionID):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            json_data = json.load(f)

            #If older and has no attribute versionID.
            if 'versionID' not in json_data:
                return False

            versionID = json_data['versionID']
            
            #Edge Case where None is filled OR it is IMPOSSIBLE Flag or something.
            if(versionID == None or isinstance(versionID, str)):
                return False

            # Normal behavior where Value is larger or equal
            if(versionID > new_versionID):
                return True
    
    return False


#Just a helper Func
def get_Version_ID_For_Print(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            json_data = json.load(f)
            
            if 'versionID' not in json_data:
                return ""

            return json_data['versionID']
        

def printTimestampDiff(startTimestamp, meassage):
    timestamp_diff = datetime.datetime.now() - startTimestamp
    hours, remainder = divmod(timestamp_diff.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = timestamp_diff.microseconds // 1000

    # Formatting the difference
    formatted_diff = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}"
    print(formatted_diff + meassage)


def save_impossible_solution_json(saveFilePath, versionID, message = ""):
    data = {
        "versionID": "IMPOSSIBLE"
    }
    
    if (message != ""):
        data = {
            "versionID": "IMPOSSIBLE",
            "message": message
        } 

    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    if(is_file_versionID_older(saveFilePath, versionID)):
        print(f"[NOT saving File] - File {fileName_short} VersionID {get_Version_ID_For_Print(saveFilePath)} is higher than current: {versionID}.")
        return

    #Use custom Encoder for np Array and Timedelta
    jsonString = json.dumps(data, indent=4)

    with open(saveFilePath, 'w') as f:
        f.write(jsonString)

    fileName_short = "/".join(saveFilePath.split("/")[-3:])

    print(f"Saved IMPOSSIBLE SOLUTION FLAG File: - {fileName_short}")


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), '..'))
sys.path.insert(0, parent_dir)


# Kinda Janky, because the middle Save Folder is extracted by the current given InputMap. 
# As Greedy Filepaths are saved in: PythonProgramming/Data_Template/15x15_WaferMap/15x15_100Percent_InputMap.txt - 15x15_WaferMap is extraced as folder
def get_filepath_Json(inputMapFilepath, probecardSize, save_folder, name_addition = ""):
    if name_addition != "":
        name_addition = "_" + name_addition
    
    return os.path.join(BASE_DATA_FILEPATH, save_folder, inputMapFilepath.rsplit('/')[-2], probecardSize + name_addition + ".json").replace("\\", "/")


def check_folder_exists(filepath):
    directory = os.path.dirname(filepath)
    
    # Check if the directory exists
    if os.path.exists(directory) and os.path.isdir(directory):
        return True
    else:
        return False
    

# Zielfunktion ist S^tdc(d). S angenommen 2

#Input dict: {1: 224, 2: 32} -> Result is a int score
def get_result_score(rating_dict):
    score = 0
    for key, key_count in rating_dict.items():
        # KEY - 1 ist INTUITIVER VON DEN WERTEN!!!!
        # Aber Mathematische Def mit oder ohne -1???
        score += pow(PENALTY_SCORE, key-1) * key_count
        #print(f"Key:{key}, Count: {key_count} - Score: {pow(PENALTY_SCORE, key - 1)} * {key_count} = {pow(PENALTY_SCORE, key - 1) * key_count} | currSum = {score}")

    return score