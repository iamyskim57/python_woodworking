"""
Function: definition of geometric shapes
Programmer : Yoon Soo Kim

Revision History

Rev 1.0 :  2019. 12. 4
"""
import copy
data_polygon_hole = {"SHAPE": "POLYGON_HOLE", "NUM_CORNER":5, "RADIUS":50,
    "TILT":0, "TOP_SURFACE": 0, "DEPTH":20, "CENTER":[350,150],"CORNER_CUT":False,
    "TOOL_NUMBER":0, "PLANE":"TOP", "Z_home":20, "PUNCH":True}
data_rectangular_hole = {"SHAPE": "RECT_HOLE", "LONG_AXIS":100, "SHORT_AXIS":50,
    "TILT":0, "TOP_SURFACE": 0, "DEPTH":20, "CENTER":[350,150],
    "CORNER_CUT":False, "TOOL_NUMBER":0, "PLANE":"TOP", "Z_home":20, "PUNCH":True}
data_circular_hole = {"SHAPE":"CIRCULAR_HOLE", "RADIUS":50, "TOP_SURFACE": 0,
    "DEPTH":20, "CENTER":[250,100], "TOOL_NUMBER":0, "PLANE":"TOP",
    "Z_home":20, "PUNCH":False }
data_drill = {"SHAPE":"DRILL", "TOP_SURFACE": 0, "DEPTH":20, "CENTER":[0,0],
    "TOOL_NUMBER":0, "PLANE":"TOP", "Z_home":20, "PUNCH":False}
data_polygon_post = {"SHAPE":"POLYGON_POST","NUM_CORNER":6, "RADIUS":100,
    "TILT":0, "CORNER_CUT_LENGTH":5, "CORNER_ROUNDING_RADIUS":5,
    "CORNER_RADIUS_MATING_HOLE":5, "TOP_SURFACE": 0, "HEIGHT":2,
     "CENTER":[0,0], "TOOL_NUMBER":0,  "PLANE":"TOP","Z_home":20}
data_rectangular_post = {"SHAPE":"RECT_POST", "LONG_AXIS":100, "SHORT_AXIS":50,
     "TILT":0, "CORNER_CUT_LENGTH":1, "CORNER_ROUNDING_RADIUS":1,
     "CORNER_RADIUS_MATING_HOLE":5, "TOP_SURFACE": 0, "HEIGHT":2,
     "CENTER":[0,0], "TOOL_NUMBER":0,  "PLANE":"TOP","Z_home":20}
data_circular_post = {"SHAPE":"CIRCULAR_POST", "RADIUS":30, "TOP_SURFACE": 0,
     "HEIGHT":2, "CENTER":[250,190],"TOOL_NUMBER":0, "PLANE":"TOP",
    "Z_home":20 }
data_line = {"SHAPE":"LINE", "TOP_SURFACE": 0, "DEPTH":10, "START":[0,0],
      "END":[100,0], "POSITION":"RIGHT", "TOOL_POS_VEC":[0.7071, 0.7071],
      "TOOL_NUMBER":0, "PLANE":"TOP", "Z_home":20, "CENTER":[0,0]}
data_arc = {"SHAPE":"ARC", "TOP_SURFACE": 0, "DEPTH":10, "RADIUS":10,
     "CENTER":[0,0],"POSITION":"RIGHT", "CENTER_POSITION":"RIGHT",
     "START_ANGLE":0, "EXT_ANGLE":90, "TOOL_POS_VEC":[0.7071, 0.7071],
     "P1":[0,45], "P2":[400,240], "TOOL_NUMBER":0, "PLANE":"TOP",
     "Z_home":20} #, "PUNCH":False}
data_base = {"SHAPE":"BASE", "LONG_AXIS": 500, "SHORT_AXIS": 100, "HEIGHT": 100,
     "Z_home":20}
data_multi_trench = {"SHAPE":"MULTI_TRENCH", "TOP_SURFACE": 0, "DEPTH_START":10,
     "DEPTH_END":10, "INTERVAL": 10, "NUM_COPY":2,
     "START":[0,0], "END":[100,0],"TOOL_NUMBER":0, "PLANE":"TOP",
      "Z_home":20, "PUNCH":False, "CENTER":[0,0]}
data_side_trench = {"SHAPE":"SIDE_TRENCH", "TOP_SURFACE": 0, "DEPTH":50,
     "INTERVAL": 10, "NUM_COPY":2,  "START":[0,0], "END":[100,0],
     "TOOL_NUMBER":11, "PLANE":"TOP", "POSITION":"RIGHT",
     "TOOL_POS_VEC":[0.7071, 0.7071], "Z_home":20,
     "PUNCH":False, "CENTER":[0,0]}
data_ref_line = {"PLANE":"TOP", "SHAPE": "REF_LINE", "CENTER":[0,0],
      "INTERVAL": 100, "TOOL_NUMBER":0}
data_curve = {"PLANE":"TOP", "SHAPE":"CURVE", "CENTER":[0,0], "TOP_SURFACE": 0,
      "DEPTH":10, "TOOL_NUMBER":0,"POSITION":"CENTER",
      "Z_home":20,"POINTS":[],"MESSAGE":''}# "PUNCH":False}
data_trench = {"SHAPE":"TRENCH", "TOP_SURFACE": 0, "DEPTH":10,"WIDTH":10,
     "START":[0,0], "END":[100,0], "TOOL_NUMBER":0, "PLANE":"TOP",
     "Z_home":20, "PUNCH":False, "CENTER":[0,0]}
data_ridge = {"SHAPE":"RIDGE", "TOP_SURFACE": 0, "HEIGHT":10, "WIDTH":10,
     "START":[0,0], "END":[100,0], "TOOL_NUMBER":0, "PLANE":"TOP",
     "Z_home":20, "CENTER":[0,0]}
data_edge = {"SHAPE":"EDGE", "TOP_SURFACE": 0, "HEIGHT":10, "RETRACT":10,
     "START":[0,0], "END":[100,0], "POSITION":"RIGHT", "TOOL_NUMBER":0,
     "PLANE":"TOP", "Z_home":20, "CENTER":[0,0]}
data_planar_surface = {"SHAPE":"PLANAR_SURFACE", "TOP_SURFACE": -5,
      "P1":[0,45], "P2":[400,240], "TOOL_NUMBER":0, "PLANE":"TOP",
      "Z_home":20, "CENTER":[0,0]}
shape_map = {"BASE":data_base, "LINE":data_line, "PLANAR_SURFACE":data_planar_surface,
             "EDGE":data_edge, "RIDGE":data_ridge, "TRENCH":data_trench,
             "CIRCULAR_POST":data_circular_post, "POLYGON_POST":data_polygon_post,
             "CIRCULAR_HOLE":data_circular_hole, "POLYGON_HOLE":data_polygon_hole, "RECT_POST":data_rectangular_post, "RECT_HOLE":data_rectangular_hole,
             "ARC":data_arc, "MULTI_TRENCH":data_multi_trench, "SIDE_TRENCH":data_side_trench, "DRILL": data_drill, "REF_LINE": data_ref_line, "CURVE":data_curve}
def object_template(shape):
    """
    return template of object
    :param shape: object shape which corresponds to SHAPE:"---"
    :return:
    """
    if shape == "BASE":
        object = copy.deepcopy(data_base)
    elif shape == "POLYGON_HOLE":
        object = copy.deepcopy(data_polygon_hole)
    elif shape == "POLYGON_POST":
        object = copy.deepcopy(data_polygon_post)
    elif shape == "RECTANGULAR_HOLE":
        object = copy.deepcopy(data_rectangular_hole)
    elif shape == "RECTANGULAR_POST":
        object = copy.deepcopy(data_rectangular_post)
    elif shape == "CIRCULAR_HOLE":
        object = copy.deepcopy(data_circular_hole)
    elif shape == "CIRCULAR_POST":
        object = copy.deepcopy(data_circular_post)
    elif shape == "DRILL":
        object = copy.deepcopy(data_drill)
    elif shape == "LINE":
        object = copy.deepcopy(data_line)
    elif shape == "TRENCH":
        object = copy.deepcopy(data_trench)
    elif shape == "RIDGE":
        object = copy.deepcopy(data_ridge)
    elif shape == "PLANAR_SURFACE":
        object = copy.deepcopy(data_planar_surface)
    elif shape == "ARC":
        object = copy.deepcopy(data_arc)
    elif shape == "MULTI_TRENCH":
        object = copy.deepcopy(data_multi_trench)
    elif shape == "SIDE_TRENCH":
        object = copy.deepcopy(data_side_trench)
    elif shape == "CURVE":
        object = copy.deepcopy(data_curve)
    return object
def get_center(object):
    """
    return center (x,y,z) from object
    :param object:
    :return: center [x,y,z]
    """
    import draw_modules
    center_z = 0
    shape = object["SHAPE"]
    object = draw_modules.object_data_to_number(object)
    if shape == "LINE"  or shape == "EDGE" or shape == "RIDGE" or shape == "TRENCH":
        center_x = (object["START"][0] + object["END"][0])/2
        center_y = (object["START"][1] + object["END"][1]) / 2
    elif shape == "PLANAR_SURFACE":
        center_x = (object["P1"][0] + object["P2"][0])/2
        center_y = (object["P1"][1] + object["P2"][1]) / 2
    elif shape != "BASE":
        [center_x, center_y] = object["CENTER"]
    else:
        [center_x, center_y] = [None, None]

    if shape == "POLYGON_POST" or shape == "CIRCULAR_POST" or \
            shape == "POLYGON_POST" or shape == "RIDGE" or \
            shape == "PLANAR_SURFACE" or shape == "EDGE" or shape == "RECT_POST":
        center_z = float(object["TOP_SURFACE"])
    elif shape == "MULTI_TRENCH":
        center_z = float(object["TOP_SURFACE"]) - (float(object["DEPTH_START"]) + float(object["DEPTH_END"] ))/2
    elif shape == "CURVE":
        center_x = object["CENTER"][0]
        center_y= object["CENTER"][1]
        center_z = float(object["TOP_SURFACE"]) - float(object["DEPTH"])
    elif shape != 'BASE' and shape != "REF_LINE":
        center_z = float(object["TOP_SURFACE"]) - float(object["DEPTH"])
    else:
        center_z = None
    return [center_x, center_y, center_z]

# sorting priority in generating tool path
sorting_priority = ["BASE", "REF_LINE", "PLANAR_SURFACE", "DRILL", "CIRCULAR_HOLE", "POLYGON_HOLE", "RECT_HOLE", "TRENCH", "MULTI_TRENCH", "ARC", "EDGE", "CURVE", "RIDGE", "LINE", "CIRCULAR_POST", "POLYGON_POST","RECT_POST"]

