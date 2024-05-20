#Generate Parts
import geometric_shapes, generate_path
import copy
import json
import math
import parameter
from tkinter import messagebox, simpledialog, Tk
askin = simpledialog.askstring
def make_parts(win):
    """
    main entry for creating new object with curve shape or other methods
    created part is stored in library folder or folder designated by user
    :param win:
    :return:
    """
    import housing
    objtype=int(askin(title=parameter.sel_text("Object Creation (unit:mm, degree)","부품생성 (단위:mm, 도)"),
                      prompt="\n\
                      1.Long Hole\t\t2.Long Post\n\
                      3.Elliptic Hole\t\t4.Elliptic Post\n\
                      5.Fan Hole\t\t6.Fan Post\n\
                      7.Trapezoid Hole\t8.Trapezoid Post\n"))
    tool_radius=float(askin(title=parameter.sel_text("Tool Radius","Tool 반경"), prompt="Tool Radius in mm? \t\t"))
    if objtype == 1 or objtype ==2:
        paras = askin(title=parameter.sel_text("Long Hole Parameters","Long Hole/Post 특성 입력"), prompt="길이와 폭을 입력하십시오 (mm) ")
        paras=paras.replace(',',' ')
        parm=paras.split()
        length = float(parm[0])
        width = float(parm[1])
        if objtype == 1:    #Hole
            make_long_hole_post(win, length/2, width/2, tool_radius)
        else:               #Post
            make_long_hole_post(win, length / 2, width / 2, -tool_radius)

    elif objtype == 3 or objtype == 4:
        paras = askin(title=parameter.sel_text("Elliptic Parameters","타원 Hole 특성"), prompt="장축과 단축을 입력하십시오 (mm)")
        parm=paras.split()
        longaxis = float(parm[0])
        shortaxis = float(parm[1])
        if objtype == 3:    #Hole
            make_ellipse(win, longaxis, shortaxis, tool_radius)
        else:               #Post
            make_ellipse(win, longaxis, shortaxis, -tool_radius)

    elif objtype == 5 or objtype == 6:
        paras = askin(title=parameter.sel_text("Fan Parameters","부채꼴 특성"), prompt="바깥쪽 , 안쪽 반경, 각도, 살두께를 입력하십시오")
        parm=paras.split()
        o_radius = float(parm[0])
        i_radius = float(parm[1])
        fan_angle = float(parm[2])
        thick_radial = float(parm[3])
        if objtype ==5: #Hole
            make_fan(win, o_radius, i_radius, fan_angle, tool_radius, thick_radial)
        else:           #Post
            make_fan(win, o_radius, i_radius, fan_angle, -tool_radius, thick_radial)

    elif objtype == 7 or objtype == 8:
        paras = askin(title=parameter.sel_text("Trapezoid Parameters","사다리꼴 특성"), prompt="바깥쪽 , 안쪽 반경, 각도를 입력하십시오")
        parm=paras.split()
        o_radius = float(parm[0])
        i_radius = float(parm[1])
        fan_angle = float(parm[2])
        if objtype ==7: #Hole
            make_trapezoid(win, o_radius, i_radius, fan_angle, tool_radius)
        else:           #Post
            make_trapezoid(win, o_radius, i_radius, fan_angle, -tool_radius)

def make_trapezoid(win, o_radius, i_radius, fan_angle, tool_radius):
    """
    make fan
    :param win:
    :param o_radius:
    :param i_radius:
    :param fan_angle:
    :param tool_radius:
    :return:
    """
    f_ang = fan_angle*math.pi/180
    outer = o_radius - tool_radius
    inner = i_radius + tool_radius

    inner_dec=tool_radius/inner
    outer_dec = tool_radius/outer
    f_ang_inner = f_ang-2*inner_dec
    f_ang_outer = f_ang-2*outer_dec

    s_ang_outer = f_ang_outer/2
    e_ang_outer = -s_ang_outer
    s_ang_inner = -f_ang_inner/2
    e_ang_inner = -s_ang_inner

    plist=[]
    outer = o_radius - tool_radius
    inner = i_radius + tool_radius

    x=outer*math.cos(s_ang_outer)
    y=outer*math.sin(s_ang_outer)
    plist.append([x,y])
    x=outer*math.cos(e_ang_outer)
    y=outer*math.sin(e_ang_outer)
    plist.append([x,y])
    x=inner*math.cos(s_ang_inner)
    y=inner*math.sin(s_ang_inner)
    plist.append([x,y])
    x=inner*math.cos(e_ang_inner)
    y=inner*math.sin(e_ang_inner)
    plist.append([x,y])
    plist.append(plist[0])

    if tool_radius<0:
        part = "trapz_post"
    else:
        part = "trapz_hole"
    file_name = parameter.LIBRARY_FOLDER+'/'+"%s_O%d_I%d_A%d_T%3.2f.prt" %(part, o_radius, i_radius, fan_angle, abs(tool_radius))
    obj = copy.deepcopy(geometric_shapes.data_curve)

    obj["POINTS"] = plist
    json.dump(obj, open(file_name + ".lib", 'w'))
    messagebox.showinfo(parameter.sel_text("Object Created", "Object 생성"), file_name + parameter.sel_text(" is created", " 가 생성되었습니다."))

def make_fan(win, o_radius, i_radius, fan_angle, tool_radius, thick_radial):
    """
    make fan
    :param win:
    :param o_radius:
    :param i_radius:
    :param fan_angle:
    :param tool_radius:
    :param thick_radial : radial support thickness
    :return:
    """
    #inner angle decreasing amount

    num_ang = int(fan_angle*10)
    f_ang = fan_angle*math.pi/180
    plist=[]
    outer = o_radius - tool_radius
    inner = i_radius + tool_radius

    inner_dec=tool_radius/inner
    outer_dec = tool_radius/outer
    inner_dec=thick_radial/inner
    outer_dec = thick_radial/outer
    f_ang_inner = f_ang-2*inner_dec
    f_ang_outer = f_ang-2*outer_dec
    dang_inner = -f_ang_inner/num_ang
    dang_outer = -f_ang_outer/num_ang
    ang = f_ang_outer/2
    for i in range(num_ang+1):
        x=outer*math.cos(ang)
        y=outer*math.sin(ang)
        plist.append([x,y])
        ang+= dang_outer
    ang = -f_ang_inner/2
    for i in range(num_ang):
        x = inner * math.cos(ang)
        y = inner * math.sin(ang)
        ang -=dang_inner
        plist.append([x,y])
    plist.append(plist[0])

    if tool_radius<0:
        part = "fan_post"
    else:
        part = "fan_hole"
    file_name = parameter.LIBRARY_FOLDER+'/'+"%s_O%d_I%d_A%d_S%d_T%3.2f.prt" %(part, o_radius, i_radius, fan_angle, thick_radial, abs(tool_radius))
    obj = copy.deepcopy(geometric_shapes.data_curve)

    obj["POINTS"] = plist
    json.dump(obj, open(file_name + ".lib", 'w'))
    messagebox.showinfo(parameter.sel_text("Object Created", "Object 생성"), file_name + parameter.sel_text(" is created", " 가 생성되었습니다."))

def make_ellipse(win, longaxis, shortaxis, tool_radius):
    """
    Ellipse
    :param win:
    :param longaxis:
    :param shortaxis:
    :param tool_radius:
    :return:
    """
    import math
    plist=[]
    a = longaxis/2-tool_radius
    b = shortaxis/2-tool_radius
    num = int(2*a)*10
    dx=2*a/num
    for i in range(num+1):
        x=-a + i*dx
        if x>a:
            x=a
        y = b*math.sqrt(1-(x/a)**2)
        plist.append([x,y])
    for i in range(num-1,-1,-1):
        plist.append([plist[i][0],-plist[i][1]])
    if tool_radius<0:
        part = "elliptic_post"
    else:
        part = "elliptic_hole"
    file_name = parameter.LIBRARY_FOLDER+'/'+"%s_L%d_W%d_T%3.2f.prt" %(part, longaxis, shortaxis, abs(tool_radius))
    obj = copy.deepcopy(geometric_shapes.data_curve)
    obj["POINTS"] = plist
    json.dump(obj, open(file_name + ".lib", 'w'))
    messagebox.showinfo(parameter.sel_text("Object Created", "Object 생성"),
                file_name + parameter.sel_text(" is created", " 가 생성되었습니다."))

def make_long_hole_post(win, halflength, halfwidth, tool_radius):
    """
    generate long hole or post with arc shaped ends
    :param win:
    :param halflength: half of length (end-to-end)
    :param halfwidth: half of width
    :param tool_radius: positive if hole, negative if post
    :return:
    """
    hctoc = halflength - halfwidth
    hlength = halflength - tool_radius
    hwidth = halfwidth - tool_radius
    shape=""
    shape += ("LINE " + str(hctoc) + " " + str(-hwidth) + " "+ str(-hctoc) + " "
              + str(-hwidth) +"\n")
    shape += ("ARCTO " + str(-hlength) + " " + str(0) + " " + str(-hctoc) + " "
              + str(hwidth) + "\n")
    shape += "LINETO " + str(hctoc) + " "+ str(hwidth)+"\n"
    shape += ("ARCTO " + str(hlength) + " " + str(0) + " " + str(hctoc) + " "
              + str(-hwidth) + "\n")
    print(shape)
    if tool_radius<0:
        part = "long_post"
    else:
        part = "long_hole"
    file_name = (parameter.LIBRARY_FOLDER+'/'+"%s_L%d_W%d_T%3.2f.prt"
                 %(part, 2*halflength, 2*halfwidth, abs(tool_radius)))
    long_hole_obj = copy.deepcopy(geometric_shapes.data_curve)
    lines = shape.split('\n')
    plist = generate_path.generate_pointlist(lines, verbose=False)
    long_hole_obj["POINTS"] = plist
    json.dump(long_hole_obj, open(file_name + ".lib", 'w'))
    messagebox.showinfo(parameter.sel_text("Object Created","Object 생성"),
        file_name + parameter.sel_text(" is created", " 가 생성되었습니다."))
