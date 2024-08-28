"""
Bunker bed part Generator

Generated parts :
narrow_stem (width 200mm)
wide_stem (width 400mm)
staircase_beam1(400+500mm)
staircase_beam(500+100mm)
shelf400 (400mm width)
shelf200 (200mm width)
table_top

"""

"""
Common header for plug in python program of woodmeister
"""
import copy
import parameter
from tkinter import messagebox, simpledialog, Tk
import gui_open_utility
import geometric_shapes
askin = simpledialog.askstring
margin_length = 0.1      #margin in hole length
margin_thickness = 0.1  # margin in hole width

length = 2000
height = 1400
width = 1000
thick = 18
thick_margin = 0.2
tool_radius = 1
hole_margin = 0.5
shelf_span = 300

def make_narrow_stem():
    """
    make narrow stem (width : 200mm)
    :return:
    """
    base_material = geometric_shapes.object_template("BASE")
    base_material["LONG_AXIS"] = height
    base_material["SHORT_AXIS"] = 200
    base_material["HEIGHT"] = thick
    hole_length = 200/2+hole_margin
    hole_width = thick + thick_margin
    hole_for_table_height = 750 - thick/2 - height/2
    bottom_hole = hole_for_table_height - 2*shelf_span
    holes = []
    holes.append([bottom_hole,0])
    holes.append([bottom_hole+shelf_span,0])
    holes.append([bottom_hole+2*shelf_span,0])
    holes.append([bottom_hole+3*shelf_span,0])
    object = []
    object.append(base_material)

    hole100x18 = geometric_shapes.object_template("RECTANGULAR_HOLE")
    hole100x18["LONG_AXIS"] = hole_width
    hole100x18["SHORT_AXIS"] = hole_length
    hole100x18["DEPTH"] = thick+1

    #holes = []
    for i in range(4):
        hole100x18["CENTER"] = holes[i]
        object.append(copy.deepcopy(hole100x18))

    outer = geometric_shapes.object_template("RECTANGULAR_POST")
    outer["LONG_AXIS"] = height
    outer["SHORT_AXIS"] = 200
    outer["CENTER"] = [0,0]
    outer["DEPTH"] = thick+1
    object.append(outer)
    file_to_save = gui_open_utility.save_jason_data(object, parameter.DESIGN_FOLDER,"Save Narrow Stem")
    message = "Narrow_Stem\n"
    message += file_to_save
    message += '\n\n'
    messagebox.showinfo("Output Files","File saved as " + file_to_save)
    return message


def make_wide_stem():
    """
    make wide stem (width : 400mm)
    :return:
    """
    base_material = geometric_shapes.object_template("BASE")
    base_material["LONG_AXIS"] = height
    base_material["SHORT_AXIS"] = 400
    base_material["HEIGHT"] = thick
    hole_length = 200 / 2 + hole_margin
    hole_width = thick + thick_margin
    hole_for_table_height = 750 - thick / 2 - height/2
    bottom_hole = hole_for_table_height - 2 * shelf_span
    holes = []
    holes.append([bottom_hole,-100])
    holes.append([ bottom_hole,100])
    holes.append([ bottom_hole + shelf_span,-100])
    holes.append([ bottom_hole + shelf_span,100])
    holes.append([ bottom_hole + 2 * shelf_span,-100])
    holes.append([ bottom_hole + 2 * shelf_span,100])
    holes.append([ bottom_hole + 3 * shelf_span,-100])
    holes.append([ bottom_hole + 3 * shelf_span,100])
    object = []
    object.append(base_material)

    hole100x18 = geometric_shapes.object_template("RECTANGULAR_HOLE")
    hole100x18["LONG_AXIS"] = hole_width
    hole100x18["SHORT_AXIS"] = hole_length
    hole100x18["DEPTH"] = thick + 1

    # holes = []
    for i in range(8):
        hole100x18["CENTER"] = holes[i]
        object.append(copy.deepcopy(hole100x18))

    outer = geometric_shapes.object_template("RECTANGULAR_POST")
    outer["LONG_AXIS"] = height
    outer["SHORT_AXIS"] = 400
    outer["CENTER"] = [0, 0]
    outer["DEPTH"] = thick + 1
    object.append(outer)
    file_to_save = gui_open_utility.save_jason_data(object, parameter.DESIGN_FOLDER, "Save Wide Stem")
    message = "Wide_Stem\n"
    message += file_to_save
    message += '\n\n'
    messagebox.showinfo("Output Files", "File saved as " + file_to_save)
    return message

def narrow_shelf_outline():
    """
    generate point list for generating narrow shelf

    """
    point = []
    x =-width/2-tool_radius+thick
    y = -200/2-tool_radius
    point.append([x,y])
    y+= 200/4+tool_radius
    point.append([x,y])
    y -= tool_radius
    point.append([x,y])
    x-=thick
    point.append([x,y])
    y+= 200/2+2*tool_radius
    point.append([x,y])
    x+= thick
    point.append([x,y])
    y-= tool_radius
    point.append([x,y])
    y+= 200/4+tool_radius
    point.append([x,y])
    sym_point = copy.deepcopy(point)
    for i in range(len(sym_point)):
        point.append([-sym_point[i][0],-sym_point[i][1]])
    point.append(point[0])
    print(point)
    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("Narrow_shelf pts file", "*.pts")], '.pts',"Save Narrow Shelf pts file")
    fw.write(str(point))
    fw.close()
    message = "Narrow Shelf: "
    message += "Output pointlist file : "+fname+"\n\n"
    messagebox.showinfo("Narrow shelf Generated!",message)
    return message

def wide_shelf_outline():
    """
    generate point list for generating wide shelf

    """
    point = []
    x =-width/2-tool_radius+thick
    y = -200/2-tool_radius
    point.append([x,y])
    y+= 200/4+tool_radius
    point.append([x,y])
    y -= tool_radius
    point.append([x,y])
    x-=thick
    point.append([x,y])
    y+= 200/2+2*tool_radius
    point.append([x,y])
    x+= thick
    point.append([x,y])
    y-= tool_radius
    point.append([x,y])
    y+= 200/4+tool_radius
    point.append([x,y])
    lower_point=copy.deepcopy(point)
    upper_point = copy.deepcopy(point)
    for i in range(len(point)):
        lower_point[i][1] -=100
        upper_point[i][1] +=100
    all_point = lower_point+upper_point
    sym_point = copy.deepcopy(all_point)
    for i in range(len(sym_point)):
        all_point.append([-sym_point[i][0],-sym_point[i][1]])
    all_point.append(all_point[0])
    print(all_point)
    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("Wide_shelf pts file", "*.pts")], '.pts',"Save Wide Shelf pts file")
    fw.write(str(all_point))
    fw.close()
    message = "Wide Shelf: "
    message += "Output pointlist file : "+fname+"\n\n"
    messagebox.showinfo("Wide shelf Generated!",message)
    return message

def table_top_outline():
    """
    generate point list for generating table top

    """
    point = []
    x =-length/2-tool_radius
    y = width/2 - thick +tool_radius
    point.append([x,y])
    x += 200/4+tool_radius
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    y+= thick
    point.append([x,y])
    x += 200/2+tool_radius*2
    point.append([x,y])
    y -= thick
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    x+=200/4
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    y += thick
    point.append([x,y])

    x= length/2-400+tool_radius
    point.append([x,y])
    y -= thick
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    x += 200/4
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    y += thick
    point.append([x,y])
    x += 200/2+2*tool_radius
    point.append([x,y])
    y -= thick
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    x += 200/2
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    y += thick
    point.append([x,y])
    x += 200/2+2*tool_radius
    point.append([x,y])
    y -= thick
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    x += 200/4+tool_radius
    point.append([x,y])

    bottom = []
    npoint = len(point)
    for i in range(npoint):
        nn = npoint-i-1
        bottom.append([point[nn][0],-point[nn][1]])
    all_point = point + bottom
    all_point.append(point[0])

    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("Table pts file", "*.pts")], '.pts',"Save Table pts file")
    fw.write(str(all_point))
    fw.close()
    message = "Table: "
    message += "Output pointlist file : "+fname+"\n\n"
    messagebox.showinfo("Table Generated!",message)
    return message

def staircase_outline():
    """
    generate point list for generating staircase

    """
    point = []
    x =-height/2-tool_radius
    y = 400/2+tool_radius
    point.append([x,y])
    x = -x
    point.append([x, y])
    y = -y
    point.append([x, y])
    x += 240
    point.append([x,y])
    y -= 50
    point.append([x,y])

    x = -height/2 - tool_radius
    y -=450
    point.append([x,y])
    point.append(point[0])

    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("Staircase_main pts file", "*.pts")], '.pts',"Staircase_main pts file")
    fw.write(str(point))
    fw.close()
    message = "Staircase_main: "
    message += "Output pointlist file : "+fname+"\n\n"

    point[0][1]-=300
    point[1][1] -=300
    point[-1] = point[0]
    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("Staircase_sub pts file", "*.pts")], '.pts',"Save Staircase_sub pts file")
    fw.write(str(point))
    fw.close()
    message = "Staircase_sub: "
    message += "Output pointlist file : "+fname+"\n\n"
    messagebox.showinfo("Staircase Generated!",message)

    return message

def one_plug__(center, w, l, tool_radius):
    """
    generate point list for generating one plug located on top
    :param center: center of plug root
    :param w : plug width
    :param l: plug length
    :param tool_radius:
    :return:
    """
    xs = center[0]-w/2-tool_radius
    xd = xs+tool_radius
    delx = w+tool_radius*2
    yb = center[1] + tool_radius
    yt = yb + l
    point=[]
    x = xd
    y  = yb
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    y = yt
    point.append([x,y])
    x += delx
    point.append([x,y])
    y = yb
    point.append([x,y])
    x -= tool_radius
    point.append([x,y])
    return point

def bunker_bed():
    istring = askin("Table/Shelf/Bed Dimension Data ", "Bed_Length, Width, Height ?")
    parm = istring.split()
    length = float(parm[0])
    width  = float(parm[1])
    height = float(parm[2])

    istring = askin("재료", "재료두께 공차 ?")
    parm = istring.split()
    thick = float(parm[0])
    thick_margin = float(parm[1])
    istring = askin("Tool & 공차", "Tool_radius 가공공차?")
    parm = istring.split()
    tool_radius = float(parm[0])
    hole_margin = float(parm[1])
    print("사양 ", length, height, width)
    print("재료 ", thick, thick_margin)
    print("Tool ", tool_radius, hole_margin)
    message = make_narrow_stem()
    message += make_wide_stem()
    message += narrow_shelf_outline()
    message += wide_shelf_outline()
    message += table_top_outline()
    message += staircase_outline()
    return message


if __name__ == '__main__':
    result = bunker_bed()
    messagebox.showinfo("Output Written to", result)