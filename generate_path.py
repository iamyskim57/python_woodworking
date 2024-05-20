"""
generate path in accordance with data given by .pth file
#Path File of tool
#Out point derivation - generate from solidworks design file
#1. Generate path considering the tool radius
#if Plug type : outward offset of tool radius
#if Socket type : inward offset of tool radius
#2. Add points in accordance with the following rule
.pth file format
#Dimension data format
#   DIM w,h    -- Set the size of base material
#line data format
#   LINE sx sy ex ey
#line to
#   LINETO ex ey    -- Line from current position to destination
#bridge data format -- To make un-cut section until the end point [ex,ey]
#   BRGTO ex ey
#   BRGPR height length -- bridge heigt and length
#Arc data format
#   ARC sx sy mx my ex ey
#Arc to
#   ARCTO mx my ex ey
#Interpolation path
    INTER [x1, y1] [x2, y2] ... [xn, yn] - generate interpolation points connecting all the points
#  NEW ex ey  -- Begin new segment
"""
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial
import common
import vector_oper
import parameter
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

def lagrange_interpolation(plist, verbose = False):
    """
    return Lagrange Interpolation Equation
    :param plist: list of [xn,yn]
    :return: coefficients from highest order. Number of coefficients is same as length of plist
    """
    num = len(plist)
    x=[]
    y=[]
    for i in range(num):
        x.append(plist[i][0])
        y.append(plist[i][1])
    if verbose:
        print(x,y)
    poly = lagrange(x,y)
    coeff = Polynomial(poly).coef
    return coeff

def interpolate(plist, dx):
    """
    generate interpolated points from plist
    :param plist: list of points
    :param dx: x increment in generating points
    :return:
    """
    num = len(plist)
    # check if x or y is main axis
    main = 0
    count = 0
    for i in range(num-1):
        if plist[i][0] < plist[i+1][0]:
            count +=1
        elif plist[i][0] > plist[i+1][0]:
            count -= 1
    ycount = 0
    for i in range(num-1):
        if plist[i][1] < plist[i+1][1]:
            ycount +=1
        elif plist[i][1] > plist[i+1][1]:
            ycount -= 1
    if count == num-1 or count == 1-num:
        mainax = 0      # main axis is X axis
    elif ycount == num-1 or ycount == 1-num:
        mainax = 1      # main axis is Y axis
    else:
        mainax = -1     # cannot determine main axis
        print("Error - Cannot apply interpolation! Check point list ",plist)

    if mainax == 0:
        pass
    elif mainax == 1:
        plist = swap_xy(plist)

    coeff = lagrange_interpolation(plist)
    x = plist[0][0]
    xe = plist[num-1][0]
    if xe-x>0:
        pol = 1
    else:
        pol = -1
    dx = pol*dx
    points = []
    n=int(abs((xe-x)/dx))
    for i in range(n):
        y = 0
        for i in range(num):
            y += coeff[i]*x**(num-i-1)
        points.append([x,y])
        x += dx
        #print("x=",x)
    points.append(plist[num-1])

    if mainax == 1:
        points = swap_xy(points)
    return points

def swap_xy(points):
    """
    swap x,y coordinate in point list
    :param points:
    :return:
    """
    count = len(points)
    for i in range(count):
        bu = points[i][0]
        points[i][0] = points[i][1]
        points[i][1] = bu
    return points

tool_radius = 1.6
def parse_data_for_horn(line):
    """
    entry of parsing for horn generation
    :param line:
    :return:
    """
    global x_off, y_off
    x_off  = 0
    y_off = 0
    return parse_data(line)
def parse_data(line):
    """
    base shape : "DIM"
    line data format
    type, (startx, starty, )endx, endy(, mx, my)
    type : "LINE" "LINETO" "ARC" "ARCTO" "BRGTO", "INTER", "NEW"
    mx, my represents mid point between start and end points to define circular arc
    example format

    LINE [sx, sy] [ex, ey]
    LINETO [ex, ey]
    ARC [sx, sy] [mx, my] [ex, ey]
    ARCTO [mx, my] [ex. ey]
    BRGTO [ex, ey]
    BRGPR height
    NEW [ex, ey]
    INTER [x1, y1] [x2, y2] ... [xn, yn] - generate interpolation points connecting all the points
    :param line:
    :return: coordinate or dimension
    """
    global px, py       # present position
    global x_off, y_off
    elements = line.replace('[',' ')
    elements = elements.replace(']',' ')
    elements = elements.replace(',',' ')
    elements = elements.split()

    if elements[0] == "LINE":
        sx = float(elements[1])-x_off
        sy = float(elements[2])-y_off
        ex = float(elements[3])-x_off
        ey = float(elements[4])-y_off
        px = ex
        py = ey
        return [[sx, sy], [ex, ey]]
    elif elements[0] == 'LINETO':
        sx = px
        sy = py
        ex = float(elements[1])-x_off
        ey = float(elements[2])-y_off
        px = ex
        py = ey
        return [[sx, sy], [ex, ey]]
    elif elements[0] == 'BRGTO':
        sx = px
        sy = py
        ex = float(elements[1])-x_off
        ey = float(elements[2])-y_off
        px = ex
        py = ey
        print("BRIDGE ",[sx, sy, 0], [ex, ey, 0])
        return [[sx, sy, 0], [ex, ey, 0]]
    elif elements[0] == 'BRGPR':
        bridge_height = float(elements[1])
        common.bridge_height = bridge_height
        common.bridge_width = float(elements[2])
        #common.bridge_width = float(elements[2])
    elif elements[0] == 'NEW':  # begin new path
        sx = px
        sy = py
        ex = float(elements[1])-x_off
        ey = float(elements[2])-y_off
        px = ex
        py = ey
        print("NEW ",[sx, sy, -1], [ex, ey, -1])
        return [[sx, sy, -1], [ex, ey, -1]]

    elif elements[0] == "ARC":
        sx = float(elements[1])-x_off
        sy = float(elements[2])-y_off
        mx = float(elements[3])-x_off
        my = float(elements[4])-y_off
        ex = float(elements[5])-x_off
        ey = float(elements[6])-y_off
        px = ex
        py = ey
        return [[sx, sy], [mx, my], [ex, ey]]

    elif elements[0] == "ARCTO":
        sx = px
        sy = py
        mx = float(elements[1])-x_off
        my = float(elements[2])-y_off
        ex = float(elements[3])-x_off
        ey = float(elements[4])-y_off
        px = ex
        py = ey
        return [[sx, sy], [mx, my], [ex, ey]]
    elif elements[0] == "DIM":
        width = float(elements[1])
        height = float(elements[2])
        x_off = width/2
        y_off = height/2
        print("DIMENSION ", width, height)
        return [[width, height]]
    elif elements[0] == "INTER":
        npoints = int((len(elements)-1)/2)
        points = []
        pos = 1
        for i in range(npoints):
            points.append([float(elements[pos])-x_off, float(elements[pos+1])-y_off])
            pos +=2
        plist = interpolate(points, 1)
        px = plist[-1][0]
        py = plist[-1][1]
        return plist

def gen_line_path(code, distance, plist, verbose=False):
    """
    derive point data from line
    :param code: [[x1, y1], [x2, y2]]
    :param distance: present distance from start point
    :param plist: point list
    :return: distance from start point
    """
    if len(plist) ==0:
        plist.append(code[0])
    initial_distance = distance
    break_flag = False
    if verbose:
        print("Line ",code)
    l = vector_oper.length(code[0], code[1])
    ret_distance = initial_distance + l
    if len(code[0]) == 3:       #code is bridge
        plist.append(code[0])
    plist.append(code[1])
    print("Line_added ",code[1] )
    return ret_distance

def gen_arc_path(code, distance, plist, verbose = False):
    """
    generate point data following arc path
    :param code: [[x1, y1], [xm, ym], [x2, y2]]
    :param distance: present distance from throat
    :param plist:
    :return:
    """
    initial_distance = distance
    if verbose:
        print("Arc ",code)
    center, radius, unit_angle, arc_length, ang1, ang3 =  vector_oper.get_circle_eq(code[0], code[1], code[2])
    #print("ARC_PARA", center, radius, "Uangle=", unit_angle, arc_length, ang1, ang3)
    ret_distance = initial_distance + arc_length
    ang_size = ang3-ang1
    del_angle = unit_angle*delta
    now_angle = ang1
    ang_total = 0
    break_flag = False
    P = vector_oper.circle_point(center, radius, now_angle)
    plist.append(P)
    while True:
        now_angle += del_angle
        ang_total += del_angle
        distance += delta
        if abs(ang_total)>=abs(ang_size):
            now_angle = ang3
            break_flag = True
        P = vector_oper.circle_point(center, radius, now_angle)
        plist.append(P)
        if break_flag:
            break
    print("ARC Length: ", arc_length)
    return ret_distance

def gen_interpol_path(code, distance, plist, verbose = False):
    """
    Generate interpolated path
    Interpolation method : multipoint Lagrange
    :param code: [[x1, y1], [x2, y2], ...[xn, yn]]
    :param distance: accumulated distance
    :param plist: point list gerenated so far
    :param verbose:
    :return:
    """
    plist += code
    ret_distance = distance
    del_length = 0
    num_pts = len(code)
    for i in range(num_pts-1):
        d = vector_oper.length(code[i], code[i+1])
        del_length +=d
    ret_distance += del_length
    return distance

def generate_pointlist(lines, verbose = False):
    """
    generate point sequence from script command lines
    :return:
    """
    global tool_radius
    global delta
    global x_off, y_off
    global total_length
    x_off = 0
    y_off = 0
    delta = 1  # increment in path in generating path
    print("PTH Lines : ",lines)
    total_length = 0
    plist = []
    numline = len(lines)
    for i in range(numline):
        line = lines[i]
        print(line)
        if line == '':
            break
        else:
            if line[0] != '#':
                action = line.split()
                try:
                    action = action[0]
                    code = parse_data(line) #Pre-process
                    if action == "LINE" or action =="LINETO" or action == "BRGTO" or action == "NEW":
                        total_length = gen_line_path(code, total_length, plist, verbose)
                        if verbose: print("LINE ", end=' ')
                    elif action == "ARC" or action == "ARCTO":
                        total_length = gen_arc_path(code, total_length, plist, verbose)
                        if verbose: print("ARC ", end=' ')
                    elif action == "DIM":
                        if verbose: print("[Width, Height] ", end='')
                    elif action == "INTER":
                        if verbose: print("Interpolation ")
                        total_length = gen_interpol_path(code, total_length, plist, verbose)
                    if verbose: print("Path length so far : ",total_length)
                except:
                    if verbose: print("Empty Line Detected. Returning")
                    return plist

    print("Total Path length = ", total_length)
    return plist

def generate_path(file = None, verbose = False):
    """
    read .pth file and generate point sequence and write it into a file
    :return:
    """
    global total_length
    if file == None:
        name = askopenfilename(initialdir=parameter.DESIGN_FOLDER,filetypes=[("pth files", "*.pth"),("bld files", ".bld")], title="Select Path file")
        fp = open(name)
    else:
        fp = open(file)
        name = file
    lines = fp.readlines()
    fp.close()
    base_name = name.replace(".pth",'')
    base_name = base_name.replace(".bld",'')
    plist=generate_pointlist(lines, verbose)
    fw = open(base_name + ".pts", "w")
    fw.write(str(plist))
    fw.close()
    outmessage = "Total path length: "+("%5.3f" %total_length)+"mm, Output stored in " + base_name + ".pts\n"
    messagebox.showinfo(parameter.sel_text("Path data", "Path data"), outmessage)

if __name__ == '__main__':
    pass