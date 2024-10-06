#-----------------------------------------------------------------------------------------------
# Backloaded horn design program
""" This program generates two types of element in .pts format to be used in woodmeister program
# 1. Speaker chamber
# 2. Exponential Horn (from .bld file and parameter inputs)
# 3. Spiral Exponential Horn (all from parameter inputs)
# History

Creation and 1st revision
May 5, 2021 by Yoon Soo Kim
"""
#To generate basic point use D:\0.Project\backloaded_horn\backloaded_horn.xlsx
import sys
import gui_open_utility
import vector_oper
import math
import parameter
import common
import generate_path
#from generate_path import interpolate
import copy
from tkinter import messagebox, simpledialog
askin = simpledialog.askstring
tool_radius = 1.6

def line_path(code, distance, power, plist_L, plist_R, calflag = True, verbose=False):
    """
    derive horn from line data
    :param code: [[x1, y1], [x2, y2]]
    :param distance: present distance from throat
    :param power:  Out = In*exp(power*distance)
    :param plist_L:
    :param plist_R:
    :param calflag: True to generate horn path, false for simple evaluation
    :return:
    """
    initial_disatance = distance
    break_flag = False
    if verbose:
        print("Line ",code)
    l = vector_oper.length(code[0], code[1])
    ret_distance = initial_disatance + l
    [dir,  norm] = vector_oper.direction_and_normal_vector(code[0], code[1], "L")
    dx = dir[0]*delta
    dy = dir[1]*delta
    if verbose:
        print("[dx, dy] ", dx, dy)
    P1 = copy.deepcopy(code[0])
    if calflag:
        while True:

            PL, PR = horn_points(P1, norm, distance, power)
            if len(code[0])==3 :
                print("BRIDGE ",code[0])
                PL = PL+[0]
                PR = PR +[0]
            plist_L.append(PL)
            plist_R.append(PR)
            #print("appending ", PL, PR, dx, dy, code[0], P1)
            if break_flag:
                break
            P1[0] += dx
            P1[1] += dy
            #print("appending ", PL, PR, dx, dy, code[0], P1, vector_oper.length(code[0], P1), l)
            distance += delta
            if vector_oper.length(code[0], P1) >= l:
                P1 = code[1]
                break_flag=True
    if verbose:
        print("line ", code, "length = ",l)

    return ret_distance

def get_arc_point(point, phi, center):
    """
    get coordinate on an arc
    :param point: [x, y] - one of arc point
    :param phi: angle in radian
    :param center: [cx, cy]
    :return:
    """
    radius = vector_oper.length(point, center)
    #print("point ", point, "phi ", phi*180/math.pi, "center ", center)
    cop = math.cos(phi)
    sip = math.sin(phi)
    x_ret = radius*cop+ center[0]
    y_ret = radius* sip + center[1]
    #print("ret x,y ", x_ret, y_ret)
    return [x_ret, y_ret]

def arc_path(code, distance, power, plist_L, plist_R, calflag = True, verbose = False):
    """
    generate horn data following arc path
    :param code: [[x1, y1], [xm, ym], [x2, y2]]
    :param distance: present distance from throat
    :param power: m in S = S0*exp(m*dist)
    :param plist_L:
    :param plist_R:
    :return:
    """
    initial_distance = distance
    break_flag = False
    if verbose:
        print("Arc ",code)
    center, radius, unit_angle, arc_length, ang1, ang3 =  vector_oper.get_circle_eq(code[0], code[1], code[2])
    print("ARC_PARA", center, radius, "Uangle=", unit_angle, arc_length, ang1, ang3)
    ang_size = abs(ang3-ang1)
    if ang_size >math.pi:
        ang_size = 2*math.pi - ang_size
    if verbose:
        print("idist ", initial_distance, arc_length)
    ret_distance = initial_distance + arc_length

    del_angle = unit_angle*delta
    now_angle = ang1
    ang_total = 0
    if calflag:
        while True:
            point=get_arc_point(code[0], now_angle, center)
            # now derive horn points
            norm = [math.cos(now_angle), math.sin(now_angle)]
            PL, PR = horn_points(point, norm, distance, power)
            if del_angle<0:
                plist_L.append(PL)
                plist_R.append(PR)
            else:
                plist_L.append(PR)
                plist_R.append(PL)
            if break_flag:
                break
            now_angle += del_angle
            ang_total += del_angle
            distance += delta
            if abs(ang_total)>=ang_size:
                break_flag = True
                now_angle = ang3
    return ret_distance

def horn_points(P1, norm, distance, power):
    """
    generate horn data
    :param P1: [x1, y1]
    :param norm: [xn, yn]  - unit vector of norm pointing left of the path
    :param distance: distance from throat of horn
    :param power: m for equation S = S1*exp(m*distance)
    :return: PL, PR
        PL - point on left side of horn
        PR - point on the right side of horn

    """
    width = throat*math.exp(distance*power)
    if horn_type == "HOLE":
        width -= tool_radius*2
    elif horn_type == "PLUG":
        width += tool_radius
    else:       # simply show the outline
        pass
    displacement = [norm[0]*width/2, norm[1]*width/2]
    PL = [P1[0]+displacement[0], P1[1]+displacement[1]]
    PR = [P1[0]-displacement[0], P1[1]-displacement[1]]
    return PL, PR

def generate_horn(win, verbose = False):
    """
    Generate exponential horn in .pts format
    :return:
    """
    global throat
    global mouth
    global tool_radius
    global horn_type
    global delta
    global x_off, y_off
    x_off = 0
    y_off = 0
    delta = 1  # increment in path in generating horn data
    horn_type = "HOLE"  # either HOLE, PLUG, CUTSHAPE
    # if HOLE or PLUG represents the tool path
    # CUTSHAPE shows the shape after cutting
    tool_radius = 1.6
    horn_type = "HOLE"
    fp, name = gui_open_utility.open_file_dialog(parameter.DESIGN_FOLDER,[("bld files", "*.bld")], "Select design file")
    print(fp, name)
    base_name = name.replace(".bld",'')
    #fp = open("d:\woodmeister\design_data\horn_200x300mm.txt","r")

    total_length = 0
    plist_R = []
    plist_L = []

    para = askin(title="Horn Parameter", prompt="Throat and Mouth_width? ", parent=win)
    parm = para.split()
    throat = float(parm[0])
    mouth = float(parm[1])
    horn_type = int(askin(title="Fab Parameter", prompt="PLUG (0) or HOLE(1) ", parent=win))

    if horn_type == 0:
        horn_type = "PLUG"
    elif horn_type ==1:
        horn_type = "HOLE"
    else:
        horn_type = "CUTSHAPE"

    tool_radius = float(askin(title="Fab Parameter ", prompt="Tool Radius (Def 1.6mm) ", parent=win))

    trim = askin(title="Fab Parameter ", prompt="Remove points beyond bounding box? (Y-N)", parent=win)
    if trim == "Y" or trim == "y":
        bound = askin(title="Fab Parameter ", prompt="lefttop(x,y), rightbottom(x,y) ", parent=win)
        coord = bound.split()
        xmin = float(coord[0])
        ymax = float(coord[1])
        xmax = float(coord[2])
        ymin = float(coord[3])

    while(True):
        line = fp.readline()
        if verbose:
            print(line)
        if line == '':
            break
        else:
            if line[0] != '#':
                code = generate_path.parse_data_for_horn(line)
                num_ele = len(code)
                if num_ele == 2:
                    #total_length += line_path(code)
                    total_length = line_path(code, total_length, 0, plist_L, plist_R, False, verbose)
                    print("LINE ", end=' ')
                elif num_ele == 3:
                    total_length = arc_path(code, total_length, 0, plist_L, plist_R, False, verbose)
                    print("ARC ", end=' ')
                elif num_ele == 1:
                    print("[Width, Height] ", end='')
                print(code, end=':')
                print("Accumulated distance from throat so far: ",total_length)

    print("Horn length = ", total_length)
    power = math.log(mouth/throat)/total_length
    fp.close()
    print("m in exp(m*dist) is ",power)
    #cutoff freq mc/(4*pi)
    f_cutoff = 340000*power/4/math.pi
    print("cutoff freq = ", f_cutoff)
    t_to_m = math.exp(power*total_length)
    print("cutoff freq = ", f_cutoff, "path length=", total_length, "t_to_m=",t_to_m)
    postscript = "th" + str(int(throat)) + "mo" + str(int(mouth)) + "tool" + \
                 str(tool_radius * 1000)+ "fc"+str(int(f_cutoff)) + "hl"+str(int(total_length))
    base_name += postscript
    fp = open(name,"r")
    total_length = 0
    while(True):
        line = fp.readline()
        #print(line)
        if line == '':
            break
        else:
            if line[0] != '#':
                code = generate_path.parse_data_for_horn(line)
                num_ele = len(code)
                if num_ele == 2:
                    #total_length += line_path(code)
                    total_length = line_path(code, total_length, power, plist_L, plist_R, True, verbose)
                elif num_ele == 3:
                    total_length = arc_path(code, total_length, power, plist_L, plist_R, True, verbose)
                if verbose:
                    print("Accumulated distance from throat so far ",total_length)

    fw = open(base_name + ".pts","w")
    fwl = open(base_name+ "_L.pts","w")
    fwr = open(base_name+ "_R.pts","w")
    fspec = open(base_name + ".prm","w")
    if trim == 'Y' or trim == 'y': # eliminate points beyond bounding box
        pL_L=[]
        pL_R=[]
        for i in range(len(plist_L)):
            if (plist_L[i][0]>=xmin) and (plist_L[i][0]<=xmax) \
                    and (plist_L[i][1]>=ymin) and (plist_L[i][1]<=ymax):
                pL_L.append(plist_L[i])
        for i in range(len(plist_R)):
            if (plist_R[i][0]>=xmin) and (plist_R[i][0]<=xmax) \
                    and (plist_R[i][1]>=ymin) and (plist_R[i][1]<=ymax):
                pL_R.append(plist_R[i])
        plist_L=pL_L
        plist_R = pL_R

    plist =copy.deepcopy(plist_L)
    for i in range(len(plist_R)-1, -1, -1):
        plist.append(plist_R[i])
    plist.append(plist[0])
    fw.write(str(plist))
    fwl.write(str(plist_L))
    fwr.write(str(plist_R))
    msg_info = "Throat: %6.2f mm, Mouth: %6.2f mm, Tool_Radius: %6.2f mm\n\
Cutoff Freq : %7.2f Hz, Path Length : %5.3f meter\n" %(throat, mouth, tool_radius, f_cutoff, total_length/1000)
    #msg_info += "Cutoff Freq : %7.2f Hz, Path Length : %5.3f meter\n" %(f_cutoff, total_length/1000)

    msg_output_file = "Output stored in " + base_name + ".pts\n" + base_name + "_L.pts\n" + \
                      base_name + "_R.pts\n" + base_name + ".prm\n"
    messagebox.showinfo(parameter.sel_text("Horn Data", "Horn Data"), msg_info + msg_output_file)
    fspec.write(msg_info + msg_output_file)
    fp.close()
    fp = open(name,"r")
    lines = fp.readlines()
    fspec.write("\n#---------Horn Data---------------\n")
    for line in lines:
        fspec.write(line)
    fspec.close()
    fp.close()
    fw.close()
    fwl.close()
    fwr.close()

def gen_chamber(win):
    """
    generate speaker chamber data in .pts format
    chamber shape

  p4*******BRGD******** p5
    *                 * p6
    *                    *
    *                 *
    B                    *
    R                 *
    G                    *
    D                 *
    *                    *
    *                 *
    *                    *
    *                 *  p1
  p3********BRGD********  p2

    :return:
    """
    tool_radius = 1.6
    points = []
    para = askin(title="Chamber Parameter",
        prompt="Chamber width, height, num_valleys, valley_height ", parent=win)
    parms = para.split()
    cwidth = float(parms[0])
    cheight = float(parms[1])
    n_valley = int(parms[2])
    h_valley = float(parms[3])
    type_chamber = int(askin(title="Cutting Parameter",
        prompt="POST(2) or HOLE(1) ", parent=win))
    if type_chamber == 1:
        type_chamber="HOLE"
    else:
        type_chamber = "POST"
    bridge_width = common.bridge_width
    tool_radius = float(askin(title="Cutting Parameter",
        prompt="Tool_radius? ", parent=win))
    #bridge_width = 10
    side_guard = 5
    w_valley = (cheight-2*side_guard)/n_valley
    ang_valley = math.atan2(h_valley, w_valley/2)
    # move by this factor
    # These are assumed for HOLE type chamber
    tool_move_for_valley = -tool_radius/math.cos(ang_valley)
    tool_move_for_left_side = tool_radius
    tool_move_for_top_side = -tool_radius
    tool_move_for_bottom_side = tool_radius
    if type_chamber == "POST":
        tool_move_for_valley = -tool_move_for_valley
        tool_move_for_left_side = -tool_move_for_left_side
        tool_move_for_top_side = -tool_move_for_top_side
        tool_move_for_bottom_side = -tool_move_for_bottom_side

    #set 4 corners from southwest clockwise
    p1 = [cwidth/2+tool_move_for_valley, -cheight/2+side_guard]
    p2 = [cwidth/2+tool_move_for_valley, -cheight/2 + tool_move_for_bottom_side]
    p3 = [-cwidth/2+ tool_move_for_left_side, -cheight/2 + tool_move_for_bottom_side]
    p4 = [-cwidth/2 + tool_move_for_left_side, cheight/2+tool_move_for_top_side]
    p5 = [cwidth/2+tool_move_for_valley, cheight/2+tool_move_for_top_side]
    p6 = [cwidth/2+tool_move_for_valley, cheight/2-side_guard]

    br_23_x = (p2[0] + p3[0])/2
    br_23x_s = br_23_x + bridge_width/2
    br_23x_e = br_23_x - bridge_width/2
    br_34_y = (p3[1] + p4[1])/2
    br_34y_s = br_34_y - bridge_width/2
    br_34y_e = br_34_y + bridge_width / 2
    points.append(p1)
    points.append(p2)
    #insert bridge
    points.append([br_23x_s,p2[1]])
    points.append([br_23x_s,p2[1],0])
    points.append([br_23x_e,p2[1],0])
    points.append([br_23x_e,p2[1]])
    points.append(p3)
    #insert bridge
    points.append([p3[0], br_34y_s])
    points.append([p3[0], br_34y_s, 0])
    points.append([p3[0], br_34y_e, 0])
    points.append([p3[0], br_34y_e])
    points.append(p4)
    #insert bridge
    points.append([br_23x_e,p4[1]])
    points.append([br_23x_e,p4[1], 0])
    points.append([br_23x_s,p4[1],0])
    points.append([br_23x_s,p4[1]])
    points.append(p5)
    points.append(p6)
    # x coordinate of peak and valley
    high = h_valley+cwidth/2 + tool_move_for_valley
    low = cwidth/2 + tool_move_for_valley
    half_width = w_valley/2
    y = p6[1]
    for i in range(n_valley):
        y -= half_width
        p = [high, y]
        points.append(p)
        y -=half_width
        p = [low, y]
        points.append(p)

    name = (parameter.DESIGN_FOLDER+'/chamber_w'+str(cwidth)
        +'_h'+str(cheight)+'_nv'+str(n_valley)+'_hv'+str(h_valley)+'.pts')
    fp = open(name,'w')
    messagebox.showinfo(parameter.sel_text("Horn Data",
                "Horn Data"), "chamber output to "+ name)
    fp.write(str(points))
    fp.close()

def polar_to_cart(radius, theta):
    """
    return cartesian coordinate from polar coordinate
    :param radius:
    :param theta: in radian
    :return: [x,y]
    """
    return [radius*math.cos(theta), radius*math.sin(theta)]

def generate_spiral_horn(win, verbose=False):
    """
    Generate spiral path exponential horn in .pts
    Clockwise spiral path
    :return:
    """
    global throat
    global mouth
    global tool_radius
    global horn_type
    global delta
    global x_off, y_off
    x_off = 0
    y_off = 0
    delta = 1  # increment in path in generating horn data
    horn_type = "HOLE"  # either HOLE, PLUG, CUTSHAPE
    # if HOLE or PLUG represents the tool path
    # CUTSHAPE shows the shape after cutting
    tool_radius = 1.6
    horn_type = "HOLE"
    parm = askin(title="Design Parameter", prompt="Speaker_Diameter, Wall_thickness, Horn_length ", parent=win)
    parm = parm.replace(',',' ')
    par=parm.split()
    spk_dia = float(par[0])
    thick_wall = float(par[1])
    horn_length = int(par[2])
    parn = askin(title="Design Parameter", prompt="Throat, Mouth, Horn_type(0:Plug, 1:Hole) ", parent=win)
    parn = parn.replace(',',' ')
    parr=parn.split()
    throat = float(parr[0])
    mouth = float(parr[1])
    horn_type = int(parr[2])

    if horn_type == 0:
        horn_type = "PLUG"
    elif horn_type == 1:
        horn_type = "HOLE"
    else:
        horn_type = "CUTSHAPE"
    pL_R = []  # inner path in cutting
    pL_L = []  # outer path in cutting wall
    tool_radius = float(askin(title="Fab Parameter ", prompt="Tool Radius (Def 1.6mm) ", parent=win))
    # trim = input("Remove points beyond horizontal boundary? (Y-N) :")
    bridge = askin(title="Fab Parameter ", prompt=parameter.sel_text("Prevent Loose Piece? (Y-N)", "떨어짐 방지를 넣을까요? (Y-N)"), parent=win)
    bridge = bridge.upper()

    # generate innermost path
    power = math.log(mouth / throat) / (horn_length - (spk_dia+throat/2)*math.pi)
    #power = math.log(mouth / throat) / horn_length
    f_cutoff = 340000 * power / 4 / math.pi

    r_spk = spk_dia / 2
    r_inner = r_spk - thick_wall / 2 - tool_radius
    r_outer = r_spk + thick_wall / 2 + tool_radius
    ang_now = 0
    del_r = (throat + thick_wall) / 360
    total_length = 0
    for i in range(0, 360):  # path generation for speaker chamber
        ang_rad = ang_now / 180 * math.pi
        i_coord = polar_to_cart(r_inner, ang_rad)
        o_coord = polar_to_cart(r_outer, ang_rad)
        pL_R.append(i_coord)
        pL_L.append(o_coord)
        r_inner += del_r
        r_outer += del_r
        del_L = (r_inner + r_outer) / 2 * (1 * math.pi / 180)
        total_length += del_L
        ang_now -= 1
    chamber_length = total_length
    print("speaker chamber length = ",total_length)
    total_length=0

    i = 0
    while (total_length < horn_length-chamber_length):
        # s_angle_index = s_angle//360
        # s_ang_del = s_angle % 360
        horn_width = throat * math.exp(power * total_length)
        c_width = horn_width + thick_wall
        base_rad_inner = math.sqrt(pL_R[i][0] ** 2 + pL_R[i][1] ** 2)
        base_rad_outer = math.sqrt(pL_L[i][0] ** 2 + pL_L[i][1] ** 2)
        act_rad_inner = base_rad_inner + c_width  # radius to be applied in cutting inner
        act_rad_outer = base_rad_outer + c_width  # radius to be applied in cutting inner
        del_L = (act_rad_inner + act_rad_outer) / 2 * (1 * math.pi / 180)
        total_length += del_L
        # print("i, R-inner, R-outer, total length ", i, base_rad_inner, base_rad_outer, total_length)
        angle = -i / 180 * math.pi
        pL_R.append(polar_to_cart(act_rad_inner, angle))
        pL_L.append(polar_to_cart(act_rad_outer, angle))
        i += 1
        if i % 360 == 0:
            print("T_length", total_length)
    fw, fname = gui_open_utility.open_file_to_write(parameter.DESIGN_FOLDER, [("pts files", "*.pts")], '.pts')
    file = fname.split('.')
    base_name = file[0]
    fwl = open(base_name + "_L.pts", "w")
    fwr = open(base_name + "_R.pts", "w")
    fspec = open(base_name + ".prm","w")
    #Insert Bridge at every 90(180) degree position
    bridge_at_every_angle = 90

    nPL = len(pL_L)
    nPR = len(pL_R)
    for j in range(0,nPL):
        index = j%bridge_at_every_angle
        radius = math.sqrt(pL_L[j][0]**2 + pL_L[j][1]**2)
        del_ANG = 5 / radius * 180 / math.pi  # limit the length of bridge to 5mm
        if index>=0 and index<del_ANG and bridge == 'Y':
            pL_L[j] = pL_L[j]+[0]
    for j in range(0,nPR):
        index = j%bridge_at_every_angle
        radius = math.sqrt(pL_R[j][0]**2 + pL_R[j][1]**2)
        del_ANG = 5 / radius * 180 / math.pi  # limit the length of bridge to 5mm
        if index>=0 and index<del_ANG and bridge == 'Y':
            pL_R[j] = pL_R[j]+[0]
    # make cutting path for entire horn
    plist = copy.deepcopy(pL_R)
    for k in range(0, i):
        p_add = pL_L[-k - 360]      # point to append
        plist.append(p_add)
    plist.append(p_add) # + [0])       # to make bridge
    plist.append(pL_R[0]) #+[0])       #

    fw.write(str(plist))
    fwl.write(str(pL_L))
    fwr.write(str(pL_R))

    fw.close()
    fwl.close()
    fwr.close()
    msg_info = "Cutoff Freq : %7.2f Hz, Total Spiral Path Length : %5.3f meter\n" % (f_cutoff, total_length / 1000)

    msg_output_file = "Output stored in " + base_name + ".pts\n" + base_name + "_L.pts\n" + \
                      base_name + "_R.pts\n"
    messagebox.showinfo(parameter.sel_text("Horn Data", "Horn Data"), msg_info + msg_output_file)
    msg_horn = "Speaker : %7.2f, Wall : %7.2f, Throat : %7.2f, Mouth : %7.2f\n" %(spk_dia, thick_wall, throat, mouth)
    # print("plist_L", plist_L)
    fspec.write(msg_info + msg_horn + msg_output_file)
    fspec.close()

def bld_design(win):
    def command_not_allowed(message="Not allowed for this build"):
        messagebox.showinfo("Previledged Users Only!", message)
    #sel = input("Speaker Chamber Generation (1), Horn Generation (2) : ? ")
    if common.advanced_topic:
        sel = int(askin(title="Backload Horn Element Designer", prompt="Speaker Chamber (1), Normal Horn (2), Spiral Horn (3)", parent=win))
        if sel == 1:
            gen_chamber(win)
        elif sel == 2:
            generate_horn(win)
        else:
            generate_spiral_horn(win)
    else:
        command_not_allowed()
    #shape["NUM_EDGE"] = int(askin(title="Panel Data", prompt="변의 수 ", parent=win))
if __name__ == '__main__':
    sel = input("Speaker Chamber Generation (1), Horn Generation (2) : ? ")
    if sel == "1":
        gen_chamber()
    elif sel == '2':
        generate_horn()
    else:
        generate_spiral_horn()