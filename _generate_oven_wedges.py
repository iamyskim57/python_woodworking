import math, parameter
import os
from tkinter.filedialog import asksaveasfilename
"""
generate wedges for building pizza oven with bricks
0th layer height is equivalent to length of brick(200mm)
other layer height is equal to height of brick (60mm)
"""
def addoffset(point,offset):
    return [point[0]+offset[0],point[1]+offset[1]]
def wedge_type2(brick_width, brick_height,oven_radius,tool_radius):
    """
    generate wedge for adding 2nd layers and above
    :param brick_width: 100mm
    :param brick_height: 60mm
    :param oven_radius: inner_radius of oven
    :param tool_radius: 1.6
    :return:
    """
    gap = math.tan(((math.atan(brick_height/oven_radius/2)) -
       math.atan(brick_height/(oven_radius+brick_width)/2)))*2*(oven_radius+brick_width)
    point = []
    p0 = [0-tool_radius,tool_radius]
    p1 = [brick_width+tool_radius,gap/2+tool_radius]
    p2 = [p1[0],-p1[1]]
    p3 = [p0[0],-p0[1]]
    for i in range(20):
        y_offset = -(gap+tool_radius*4)*i
        point.append(addoffset(p0,[0,y_offset]))
        point.append(addoffset(p1, [0, y_offset]))
        point.append(addoffset(p2, [0, y_offset]))
        point.append(addoffset(p3, [0, y_offset]))
    filename = asksaveasfilename(initialdir=parameter.DESIGN_FOLDER, title=
      "Type2 Wedge 저장: File을 선택하세요", filetypes=[("PointList file", "*.pts")])
    name, extension = os.path.splitext(filename)
    fw = open(name+'.pts',"w")
    fw.write(str(point))

def wedge_type1(brick_length, brick_width, brick_height,oven_radius,tool_radius):
    """
    generate wedge for adding 1st layer
    :param brick_length: 200mm
    :param brick_width: 100mm
    :param brick_height: 60mm
    :param oven_radius: inner_radius of oven
    :param tool_radius: 1.6
    :return:
    """
    ang = math.tan(brick_length/oven_radius/2) + math.tan(brick_height/oven_radius/2)
    gap = math.tan(ang)*brick_width
    print(gap)
    point = []
    p0 = [0-tool_radius,tool_radius]
    p1 = [brick_width+tool_radius,gap+tool_radius]
    p2 = [p1[0],-p0[1]]
    p3 = [p0[0],-p0[1]]
    for i in range(15):
        y_offset = -(gap+tool_radius*4)*i
        point.append(addoffset(p0,[0,y_offset]))
        point.append(addoffset(p1, [0, y_offset]))
        point.append(addoffset(p2, [0, y_offset]))
        point.append(addoffset(p3, [0, y_offset]))
    filename = asksaveasfilename(initialdir=parameter.DESIGN_FOLDER, title=
      "Type1 Wedge 저장: File 을 선택하세요", filetypes=[("PointList file", "*.pts")])
    name, extension = os.path.splitext(filename)
    fw = open(name+'.pts',"w")
    fw.write(str(point))

if __name__ == "__main__":
    wedge_type2(100, 60, 400, 1.6)
    wedge_type1(200, 100, 60, 400, 1.6)