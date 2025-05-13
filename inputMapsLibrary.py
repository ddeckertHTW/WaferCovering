import os
# Libary/List of all relevant filapths to  InputMaps / USecases. Import this instead of hardcoded Paths

#Only works, because this file is in root / no subfolder
root_dir_path = os.path.dirname(os.path.abspath(__file__))

filepath_15x15_Complete = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_Complete_InputMap.txt"
filepath_31x31_Complete = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_Complete_InputMap.txt"
filepath_51x51_Complete = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_Complete_InputMap.txt"
filepath_101x101_Complete = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_Complete_InputMap.txt"
filepath_151x151_Complete = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_Complete_InputMap.txt"
filepath_201x201_Complete = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_Complete_InputMap.txt"
filepath_251x251_Complete = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_Complete_InputMap.txt"

#Diagonal Errors - 15x15_Contamination_InputMap
filepath_15x15_Contamination = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_Contamination_InputMap.txt"
filepath_31x31_Contamination = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_Contamination_InputMap.txt"
filepath_51x51_Contamination = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_Contamination_InputMap.txt"
filepath_101x101_Contamination = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_Contamination_InputMap.txt"
filepath_151x151_Contamination = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_Contamination_InputMap.txt"
filepath_201x201_Contamination = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_Contamination_InputMap.txt"
filepath_251x251_Contamination = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_Contamination_InputMap.txt"

#Mod 4 Errors
filepath_15x15_TestStructures = root_dir_path + "/Data_Template/15x15_WaferMap/15x15_TestStructures_InputMap.txt"
filepath_31x31_TestStructures = root_dir_path + "/Data_Template/31x31_WaferMap/31x31_TestStructures_InputMap.txt"
filepath_51x51_TestStructures = root_dir_path + "/Data_Template/51x51_WaferMap/51x51_TestStructures_InputMap.txt"
filepath_101x101_TestStructures = root_dir_path + "/Data_Template/101x101_WaferMap/101x101_TestStructures_InputMap.txt"
filepath_151x151_TestStructures = root_dir_path + "/Data_Template/151x151_WaferMap/151x151_TestStructures_InputMap.txt"
filepath_201x201_TestStructures = root_dir_path + "/Data_Template/201x201_WaferMap/201x201_TestStructures_InputMap.txt"
filepath_251x251_TestStructures = root_dir_path + "/Data_Template/251x251_WaferMap/251x251_TestStructures_InputMap.txt"

#Custom Filepath
filepath_bosch_TA660 = root_dir_path + "/Data_Template/TA660/InputMap_TA660.txt"

# ForTesting
filepath_Complete_Dict = {
    '15x15': filepath_15x15_Complete,
    '31x31': filepath_31x31_Complete,
    '51x51': filepath_51x51_Complete,
    '101x101': filepath_101x101_Complete,
    '151x151': filepath_151x151_Complete,
    '201x201': filepath_201x201_Complete,
    #'251x261': filepath_251x251_Complete,
}

filepath_Contamination_Dict = {
    '15x15': filepath_15x15_Contamination,
    '31x31': filepath_31x31_Contamination,
    '51x51': filepath_51x51_Contamination,
    '101x101': filepath_101x101_Contamination,
    '151x151': filepath_151x151_Contamination,
    '201x201': filepath_201x201_Contamination,
    #'251x261': filepath_251x251_Contamination,
}

filepath_TestStructures_Dict = {
    '15x15': filepath_15x15_TestStructures,
    '31x31': filepath_31x31_TestStructures,
    '51x51': filepath_51x51_TestStructures,
    '101x101': filepath_101x101_TestStructures,
    '151x151': filepath_151x151_TestStructures,
    '201x201': filepath_201x201_TestStructures,
    #'251x261': filepath_251x251_TestStructures,
}

#A Smaller Version for CSP
filepath_Complete_Dict_small = {
    '15x15': filepath_15x15_Complete,
    '31x31': filepath_31x31_Complete,
    '51x51': filepath_51x51_Complete,
    '101x101': filepath_101x101_Complete,
    #'151x151': filepath_151x151_Complete,

}

filepath_Contamination_Dict_small = {
    '15x15': filepath_15x15_Contamination,
    '31x31': filepath_31x31_Contamination,
    '51x51': filepath_51x51_Contamination,
    '101x101': filepath_101x101_Contamination,
    #'151x151': filepath_151x151_Contamination,

}

filepath_TestStructures_Dict_small = {
    '15x15': filepath_15x15_TestStructures,
    '31x31': filepath_31x31_TestStructures,
    '51x51': filepath_51x51_TestStructures,
    '101x101': filepath_101x101_TestStructures,
    #'151x151': filepath_151x151_TestStructures,

}


filepaths_Gif_Worthy = [
    filepath_15x15_Complete,
    filepath_15x15_Contamination,
    filepath_15x15_TestStructures,
    filepath_31x31_Complete,
    filepath_31x31_Contamination,
    filepath_31x31_TestStructures,
    filepath_51x51_Complete,
    filepath_51x51_Contamination,
    filepath_51x51_TestStructures,
]

filepaths_Gif_Worthy_extended = [
    filepath_101x101_Complete,
    filepath_101x101_Contamination,
    filepath_101x101_TestStructures,
    filepath_151x151_Complete,
    filepath_151x151_Contamination,
    filepath_151x151_TestStructures,
]