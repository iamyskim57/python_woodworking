
"""
Function: Definitions of default setting,
default folders, language
retrieval and update of tool_table
Programmer : Yoon Soo Kim

Revision History

Rev 1.0 :  2019. 12. 4
"""

import sys
sys.path.insert(0,'../main_gui')
import common
import json


tool_table = {}

material_factor = 1     # multiply this number to "del_z" and feed_rate to consider hardness of material
"""LANGUAGE = "KOR"

G_CODE_FOLDER = "D:/CADCAM/g_code_data"
DESIGN_FOLDER = "D:/CADCAM/design_data"
LIBRARY_FOLDER = "D:/CADCAM/lib"
"""
LANGUAGE = ""
G_CODE_FOLDER = ""
DESIGN_FOLDER = ""
LIBRARY_FOLDER = ""
PROGRAM_FOLDER = ""
tool_table_name = ''
design_data = []
g_code_data = "#GCODE DATA OUTPUT\n"
arc_style = 'chord'
CONTROLLER = 'linuxcnc'

def retrieve_defaults(verbose = True):
    """
    retrieve defaults from config/config.json
    :return:
    """
    global defaults
    global LANGUAGE, G_CODE_FOLDER, DESIGN_FOLDER, LIBRARY_FOLDER, PROGRAM_FOLDER, arc_style, tool_table_name, CONTROLLER
    defaults = json.load(open("../config/config.json"))
    if verbose: print("defaults=",defaults)
    #print("defaults=", defaults)
    LANGUAGE = defaults["LANGUAGE"]
    G_CODE_FOLDER = defaults["G_CODE_FOLDER"]
    DESIGN_FOLDER = defaults["DESIGN_FOLDER"]
    LIBRARY_FOLDER = defaults["LIBRARY_FOLDER"]
    try:
        PROGRAM_FOLDER = defaults["PROGRAM_FOLDER"]
    except:
        pass
    tool_table_name = defaults["TOOL_TABLE_NAME"]

    arc_style = defaults["ARC_STYLE"]
    common.arc_style = arc_style

    CONTROLLER = defaults["CONTROLLER"]
    common.controller = CONTROLLER

    print("CONTROLLER = ", CONTROLLER)
    return LANGUAGE, G_CODE_FOLDER, DESIGN_FOLDER, LIBRARY_FOLDER, arc_style, CONTROLLER

def write_defaults():
    global defaults
    global LANGUAGE, G_CODE_FOLDER, DESIGN_FOLDER, LIBRARY_FOLDER, tool_table_name, CONTROLLER
    defaults["LANGUAGE"] = LANGUAGE
    defaults["G_CODE_FOLDER"] = G_CODE_FOLDER
    defaults["DESIGN_FOLDER"] = DESIGN_FOLDER
    defaults["LIBRARY_FOLDER"] = LIBRARY_FOLDER
    defaults["TOOL_TABLE_NAME"] = tool_table_name
    defaults["ARC_STYLE"] = arc_style
    defaults["CONTROLLER"] = CONTROLLER
    with open("../config/config.json", "w") as fw:
        json.dump(defaults, fw)

def retrieve_tool_table(verbose = False):
    global tool_table_name
    if tool_table_name != '':
        print("Read tool table from ", tool_table_name)
        common.tool_table = json.load(open(tool_table_name))
    else:
        print("Tool Table 초기화")
        common.tool_table = json.load(open("../tool/tool_table/tool_default.json"))
        tool_table_name = "../tool/tool_table/tool_default.json"
    spindle = json.load(open("../tool/spindle.json"))
    common.spindle_diameter = spindle["diameter"]
    common.spindle_length = spindle["length"]
    common.feed_speed = spindle["feedrate"]
    if verbose:
        print("Tools ",common.tool_table)
        print("Spindle ", spindle)

def write_tool_table():
    json.dump(open(open(tool_table_name = ''),common.tool_table))
    spindle = {"diameter":common.spindle_diameter, "length":common.spindle_length}
    json.dump(open("../tool/spindle.json",'w'),spindle)

def sel_text(eng_text,kor_text):
    """
    select text for label, button....
    :param eng_text:
    :param kor_text:
    :return:
    """
    global LANGUAGE
    if LANGUAGE == "ENG":
        return eng_text
    else:
        return kor_text
