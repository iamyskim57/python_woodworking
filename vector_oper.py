"""
Function: vector operation functions
Programmer : Yoon Soo Kim
Revision History

Rev 1.0 :  2019. 12. 4
"""
from cmath import phase
from math import *
def cal_root(A, B, C):
    """
    find root of 2nd order equation

    Ax^2 + Bx + C
    :param A:
    :param B:
    :param C:
    :return:
    """
    #print(A,B,C)
    broot = sqrt(B*B-4*A*C)
    cand1 = (-B+broot)/2/A
    cand2 = (-B-broot)/2/A
    return cand1.real, cand2.imag

def length(P1, P2):
    """
    :param P1: [x1,y1]
    :param P2: [x2,y2]
    :return: length
    """
    xl = P2[0] - P1[0]
    yl = P2[1] - P1[1]
    return sqrt(xl*xl + yl*yl)

def slope_and_cut(P1, P2):
    """
    get slope and y-axis crossing point of line connecting P1, P2
    :param P1:
    :param P2:
    :return:
    """
    a=(P2[1] - P1[1])/(P2[0]-P1[0])
    b = P1[1]-a*P1[0]
    return [a,b]

def get_norm_line(P1, P2):
    """
    get normal line equation
    :param P1: [x1,y1]
    :param P2: [x2,y2]
    :return: two points defining normal line
    """
    xc = (P1[0]+P2[0])/2
    yc = (P1[1]+P2[1])/2
    [dir_vector, normal_vector] = direction_and_normal_vector(P1, P2, "L")
    if normal_vector[0] !=0:
        slope = normal_vector[1]/normal_vector[0]
        b = -slope * xc + yc
        x = xc+1.0
        y = slope*x+b
        return ([xc,yc], [x,y])
    else:
        return ([xc,yc], [xc,yc+1.0])

def comp_coord(A,B):
    """
    :param A: [ax, ay]
    :param B: [bx,by]
    :return: True if different
    """
    if A[0]==B[0] and A[1]==B[1]:
        return False
    else:
        return True

def angle_0to2pi(P1, center):
    """
    return angle of line connecting center and P1 in a
    value between 0 and 2*pi
    :param P1: [x1,y1]
    :param center: [xc, yc]
    :return: unit-angle - angle to move to generate 1mm of path in circumference
    """
    x = P1[0]-center[0]
    y = P1[1] - center[1]
    ang = atan2(y,x)
    if ang<0:
        ang += 2*pi
    return ang

def get_circle_eq(P1, P2, P3, verbose=False):
    """
    derive circle connecting 3 points
    :param P1: [x1, y1]
    :param P2: [x2, y2]
    :param P3: [x3, y3]
    :return:
    """
    print("Points ",P1, P2, P3)
    [lp1, lp2] = get_norm_line(P1, P2)
    [lp3, lp4] = get_norm_line(P2, P3)
    center = get_cross_point(lp1, lp2, lp3, lp4)
    radius = length(P1, center)
    ang12 = angle_between_vectors_pitompi([P1[0]-center[0],P1[1]-center[1]],[P2[0]-center[0],P2[1]-center[1]])

    ang23 = angle_between_vectors_pitompi([P2[0]-center[0],P2[1]-center[1]],[P3[0]-center[0],P3[1]-center[1]])

    print("ang12 ang23 ",ang12*180/pi,ang23*180/pi)
    ang1 = angle_0to2pi(P1, center)
    ang2 = ang1 + ang12
    ang3 = ang2 + ang23
    print("ARC_ANG ", ang1*180/pi, ang2*180/pi, ang3*180/pi)
    dangle = ang2-ang1
    dang_pol = dangle/abs(dangle)

    unit_angle = 1/radius*dang_pol
    arc_ang = abs(ang3-ang1)
    arc_length = arc_ang*radius
    if verbose:
        print("center :", center, "R: ", radius, "Dir: ", "Arc Length: ", arc_length, "ang1: ",ang1*180/pi, "ang3 ",ang3*180/pi, "unit_angle: ", unit_angle*180/pi)
    return center, radius, unit_angle, arc_length, ang1, ang3

def get_circle_eq_0_to_360(P1, P2, P3, verbose=False):
    """
    derive circle connecting 3 points
    :param P1: [x1, y1]
    :param P2: [x2, y2]
    :param P3: [x3, y3]
    :return:
    """
    [lp1, lp2] = get_norm_line(P1, P2)
    [lp3, lp4] = get_norm_line(P2, P3)
    center = get_cross_point(lp1, lp2, lp3, lp4)
    radius = length(P1, center)

    ang1 = angle_0to2pi(P1, center)
    ang2 = angle_0to2pi(P2, center)
    ang3 = angle_0to2pi(P3, center)
    print("ARC_ANG ", ang1, ang2, ang3)
    dangle = ang2-ang1

    unit_angle = 1/radius
    arc_ang = abs(ang3-ang1)
    arc_length = arc_ang*radius
    if verbose:
        print("center :", center, "R: ", radius, "Dir: ", "Arc Length: ", arc_length, "ang1: ",ang1*180/pi, "ang3 ",ang3*180/pi, "unit_angle: ", unit_angle*180/pi)
    return center, radius, unit_angle, arc_length, ang1, ang3


def get_cross_point(P1, P2, P3, P4):
    """
    return cross points of line P1-P2 and P3-P4
    :param P1:
    :param P2:
    :param P3:
    :param P4:
    :return: [cx, cy]
    """
    cross_x = None
    cross_y = None
    if ( P1[0] == P2[0] and P3[0] == P4[0]) or (P1[1] == P2[1] and P3[1] == P4[1]):
        return [None, None]
    if P1[0] == P2[0]: # line 1 is vertical line
        cross_x = P1[0]
        [a,b] = slope_and_cut(P3,P4)
        cross_y = a*cross_x + b
        return [cross_x, cross_y]

    if P3[0] == P4[0]: # line 2 is vertical line
        cross_x = P3[0]
        [a, b] = slope_and_cut(P1, P2)
        cross_y = a * cross_x + b
        return [cross_x, cross_y]

    if P1[1] == P2[1]: # line1 is horizontal line
        cross_y = P1[1]
        [a,b] = slope_and_cut(P3, P4)
        cross_x = (cross_y-b)/a
        return [cross_x, cross_y]

    if P3[1] == P4[1]: # line2 is horizontal line
        cross_y = P3[1]
        [a,b] = slope_and_cut(P1, P2)
        cross_x = (cross_y-b)/a
        return [cross_x, cross_y]

    [a,b] = slope_and_cut(P1, P2)
    [c,d] = slope_and_cut(P3, P4)
    cross_x = (d-b)/(a-c)
    cross_y = a*cross_x + b
    return [cross_x, cross_y]

def symetry_point(point, symetry_line_start, symetry_line_end):
    """
    derive symetry point against line defined by symetry_line_start and symetry_line_end points
    :param point:   [x,y]
    :param symetry_line_start: [xs, ys]
    :param symetry_line_end: [xe,ye]
    :return:
    """
    if symetry_line_start[0] == symetry_line_end[0] and symetry_line_start[1] == symetry_line_end[1]:    # symetry against point
        x_ret = 2*symetry_line_start[0]-point[0]
        y_ret = 2 * symetry_line_start[1] - point[1]
        return [x_ret, y_ret]
    elif symetry_line_start[0] == symetry_line_end[0]:    # symetry against vertical line
        x_ret = 2*symetry_line_start[0]-point[0]
        y_ret = point[1]
        return [x_ret, y_ret]
    elif symetry_line_start[1] == symetry_line_end[1]:  # symetry against horizontal line
        x_ret = point[0]
        y_ret = 2*symetry_line_start[1] - point[1]
        return [x_ret, y_ret]
    else:
        # y = ax+b
        a = (symetry_line_end[1] - symetry_line_start[1])/(symetry_line_end[0]-symetry_line_start[0])
        b = -a*symetry_line_start[0] + symetry_line_start[1]
        #crossing point of two lines
        #print("A,B",a,b)
        x2 = (point[1]+point[0]/a -b) /(a+1/a)
        y2 = a*x2+b
        #print("[x2,y2]",x2,y2)
        [xv, yv] = [x2-point[0], y2-point[1]]
        #symetry point
        [x_ret,y_ret]  = [point[0]+xv*2, point[1]+yv*2]
        return [x_ret, y_ret]

def symetry_angle(angle, symetry_line_start, symetry_line_end):
    """
    derive symetry angle against line defined by symetry_line_start and symetry_line_end points
    symetry angle for symetry against line = 2*alpha-angle, where alpha is angle of line
    in case of point symetry return angle is same as input angle
    :param angle: in degree
    :param symetry_line_start: [xs, ys]
    :param symetry_line_end: [xe,ye]
    :return:
    """
    if symetry_line_start[0] == symetry_line_end[0] and symetry_line_start[1] == symetry_line_end[1]:    # symetry against point
        return angle
    elif symetry_line_start[0] == symetry_line_end[0]:    # symetry against vertical line
        alpha = 90
        return 2*alpha-angle
    elif symetry_line_start[1] == symetry_line_end[1]:  # symetry against horizontal line
        alpha = 0
        return 2*alpha-angle
    else:
        # y = ax+b
        a = (symetry_line_end[1] - symetry_line_start[1])/(symetry_line_end[0]-symetry_line_start[0])
        b = -a*symetry_line_start[0] + symetry_line_start[1]
        alpha = atan2(symetry_line_end[1]-symetry_line_start[1], symetry_line_end[0]-symetry_line_start[0])*180/pi
        print("symetry_line_angle ", alpha)
        ret_angle = 2*alpha - angle
        return ret_angle

def symetry_tool_or_center_side(side, symetry_line_start, symetry_line_end):
    """

    :param side: LEFT or RIGHT
    :param symetry_line_start:
    :param symetry_line_end:
    :return:
    """
    if symetry_line_start[0] == symetry_line_end[0] and symetry_line_start[1] == symetry_line_end[1]:
        # point symetry -- side does not change
        return side
    else:
        if side == "LEFT":
            return "RIGHT"
        elif side == "RIGHT":
            return "LEFT"
        else:
            print("Error in Side")
            return side

def direction_and_normal_vector(P1,P2,side):
    """
    return unit vectors for direction and normal vectors for cutting
    :param P1:
    :param P2:
    :param side : "L" if path is to the left of tool (cutting (cutting right) , "R" for cutting right of tool
    :return:
    """
    line_length = length(P1, P2)
    dir_vector = [(P2[0]-P1[0])/line_length, (P2[1]-P1[1])/line_length]
    if side == 'L' or side == 'LEFT' : # rotate by 90 degree
        normal_vector = [-dir_vector[1], dir_vector[0]]
    elif side == 'R' or side =='RIGHT':   # rotation by -90 degree
        normal_vector = [dir_vector[1], -dir_vector[0]]
    else:
        normal_vector = [0,0]
    return [dir_vector,  normal_vector]

def direction_and_normal_vector_for_line_cutting(P1,P2,side):
    """
    return unit vectors for direction and normal vectors for cutting left of tool path
    :param P1:
    :param P2:
    :param side : "L" if line is to the left of tool (cutting right side of line) , "R" for cutting leftside of tool
                    else if cutting center
    :return:
    """
    line_length = length(P1, P2)
    dir_vector = [(P2[0]-P1[0])/line_length, (P2[1]-P1[1])/line_length]
    if side == 'L' or side == 'LEFT' : # rotate by -90 degree
        normal_vector = [+dir_vector[1], -dir_vector[0]]
    elif side == "R" or side == "RIGHT":   # rotation by 90 degree
        normal_vector = [-dir_vector[1], dir_vector[0]]
    else:
        normal_vector = [0,0]
    return [dir_vector,  normal_vector]

def direction_and_normal_vector_for_arc(P1,P2,side, plane):
    """
    return unit vectors for direction and normal vectors of center for arc
    :param P1:
    :param P2:
    :param side : "L" for cutting left of tool path, "R" for cutting right of tool path, other if cutting center
    :return:
    """
    line_length = length(P1, P2)
    dir_vector = [(P2[0]-P1[0])/line_length, (P2[1]-P1[1])/line_length]
    if side == 'R' or side == 'RIGHT' : # rotate by -90 degree
        normal_vector = [-dir_vector[1], dir_vector[0]]
    elif side == 'L' or side == 'LEFT':   # rotation by -90 degree
        normal_vector = [dir_vector[1], -dir_vector[0]]
    else:
        normal_vector = [0,0]
    # in the following planes, change norm vector deriection for the shake of visual design
    if plane == "BOTTOM" or plane =="LEFT" or plane == "REAR":
        normal_vector = [-normal_vector[0], -normal_vector[1]]
    return [dir_vector,  normal_vector]

def direction_and_normal_vector_complex(P1,P2,side):

    """
    return unit vectors for direction and normal vectors for cutting left of tool path
    :param P1: complex
    :param P2:
    :param side : "L" for cutting left of tool path, "R" for cutting right of tool path
    :return: complex direction and norm
    """
    #old
    line_vec = P2 - P1

    line_length = line_vec.__abs__()
    dir_comp = line_vec/line_length
    """new
    P2 = P2/P2.__abs__()
    P1 = P1/P1.__abs__()
    line_vec = P2-P1
    dir_comp = line_vec"""
    #end_new
    if side == 'L' or side == 'LEFT': # rotate by 90 degree
        norm_comp = complex(-dir_comp.imag, dir_comp.real)
    elif side == 'R' or side == 'RIGHT': # rotation by -90 degree
        norm_comp = complex(dir_comp.imag, -dir_comp.real)
    else:
        norm_comp = complex(0,0)
    return [dir_comp,  norm_comp]

def scale_vec(vector, scale):
    """
    multiply vector with scalar value
    :param vector:
    :param scale:
    :return: [x,y]
    """
    return [vector[0]*scale, vector[1]*scale]

def add(vector1, vector2):
    """
    add vector
    :param vector1:
    :param vector2:
    :return: [x,y]
    """
    return [vector1[0]+vector2[0], vector1[1]+vector2[1]]

def unit_vector(vector):
    """
    return unit vector from vector1
    :param vector:
    :return:
    """
    v_length = sqrt(vector[0]*vector[0] + vector[1]*vector[1])
    if v_length !=0:
        return [vector[0]/v_length, vector[1]/v_length]
    else:
        return [0,0]
def sized_vector(vector, length):
    """
    return length long vector in the direction of input vector
    :param vector: original vector
    :param : length to adjust
    :return:
    """
    vector1 = unit_vector(vector)
    return scale_vec(vector1, length)

def sub(vector1,vector2):
    """
    subtract vector1 from vector2
    :param vector1:
    :param vector2:
    :return:
    """
    return [vector2[0]-vector1[0], vector2[1]-vector1[1]]

def linear_sum(vec1, a, vec2, b):
    """
    return vector = a*vec1 + b*vec2
    :param vec1:
    :param a:
    :param vec2:
    :param b:
    :return:
    """
    x = a*vec1[0] + b*vec2[0]
    y = a*vec1[1] + b*vec2[1]
    return [x,y]

def phase_of(dvec1, dvec2):
    """
    시계방향으로 배치되는 vector 에서 접점에서 외곽으로 향하는 unit vector 와 phase 를 구한다
    :param dvec1:
    :param dvec2:
    :return:
    """
    #print(dvec1, dvec2)
    v1 = complex(dvec1[0], dvec1[1])
    v2 = complex(dvec2[0], dvec2[1])
    v1_l = v1.__abs__()
    v2_l = v2.__abs__()
    v1 = v1/v1_l
    v2 = v2/v2_l
    v = v1-v2
    phase_v = phase(v)
    unit_v = v/v.__abs__()
    #print("in sub", [unit_v.real, unit_v.imag], phase_v*180/pi)
    return [unit_v.real, unit_v.imag], phase_v

def phase_of_complex(dvec1, dvec2, verbose = False):
    """
    시계방향으로 배치되는 vector 에서 접점에서 외곽으로 향하는 unit vector 와 phase 를 구한다
    :param dvec1:
    :param dvec2:
    :return:
    """
    #print(dvec1, dvec2)
    v1 = dvec1
    v2 = dvec2
    v1_l = v1.__abs__()
    v2_l = v2.__abs__()
    if v1_l == 0 or v2_l == 0:
        return None, None

    v1 = v1/v1_l
    v2 = v2/v2_l
    v = v1-v2

    phase_v = phase(v)
    if verbose:
        print("v1,v2,v",v1, v2, v, phase_v)
    try:
        unit_v = v/v.__abs__()
        #print("in sub", [unit_v.real, unit_v.imag], phase_v*180/pi)
        return unit_v, phase_v
    except:
        return None, None

def norm_and_phase(v1, v2, verbose = False):

    """
    2 개의 vector 에서 path 의 왼쪽으로 향하는 unit norm vector 와 phase 를 구한다
    :param v1:
    :param v2:
    :return:
    """
    #print(dvec1, dvec2)
    n1 = norm_vec(v1)
    n2 = norm_vec(v2)
    if n1 != None and n2 !=None:
        nv = (n1+n2)/abs(n1+n2)
        phase_v = phase(nv)
        if verbose:
            print("v1,v2,v",v1, v2, nv, phase_v)
            #print("in sub", [unit_v.real, unit_v.imag], phase_v*180/pi)
        return nv, phase_v
    else:
        return None, None

def get_tool_point_from_corner_point_complex(dvec1, dvec2, corner_point, Radius):
    """
    시계방향으로 베치된 vector 에서 corner 에 상응하는 점을 구한다.
    :param dvec1: complex
    :param dvec2:
    :param corner_point : complex
    :param Radius:
    :return:
    """
    u_v, p_v = phase_of_complex(dvec1, dvec2)
    theta = angle_between_vectors_complex(dvec1, dvec2)
    distance = abs(Radius/cos((pi-theta)/2))
    """if theta>pi/2:
        distance = 2*Radius*sin(pi/2 - theta/2)/sin(pi-theta)
    else:
        distance = 2*Radius*cos(theta/2)/cos(pi/2-theta)
    """
    unit_v = u_v#complex(u_v[0], u_v[1])
    m_v = distance*unit_v
    return corner_point + m_v

def get_tool_point_left_or_right(v1, v2, corner_point, Radius, offset_to_left_or_right, orig_tool_position, verbose = False):
    """
    2 개의 path vector 로 이루어지는 corner 에서 tool 이 path 의 left 또는 Right 에 해당되도록 Tool_point 를 계산한다.
    :param v1: complex
    :param v2:
    :param corner_point : complex
    :param Radius:
    :param offset_to_left_or_right ; R or L
    :param orig_tool_position : tool position on original curve (L,R, C)
    :return: tool_point in complex
    """
    u_v, p_v = norm_and_phase(v1, v2)
    if u_v is None:
        return None
    ang1 = phase(v1)
    ang2 = phase(v2)
    theta = angle_between_vectors_complex(v1,v2)
    distance = abs(Radius/cos((pi-theta)/2))
    #distance = Radius / cos((pi - theta) / 2)
    unit_v = u_v#complex(u_v[0], u_v[1])
    m_v = distance*unit_v
    if orig_tool_position == "C":
        m_v = m_v/2

    if offset_to_left_or_right == "L":
        m_v = -m_v
    elif offset_to_left_or_right == "C":
        m_v = complex(0,0)
    if verbose:
        print(v1,v2, corner_point, ang1*180/pi, ang2*180/pi, theta*180/pi, m_v, distance)
    return corner_point + m_v

def angle_between_vectors(v1, v2):
    """
    :param v1: [x,y]
    :param v2: [x,y]
    :return: angle in radian 0 to 2*pi
    """
    ang1 = phase(-complex(v1[0],v1[1]))
    ang2 = phase(complex(v2[0],v2[1]))
    ang = ang2-ang1
    if ang<0:
        ang = ang+2*pi
    #print("v1, v2, ang== = ",v1,v2,ang*180/pi)
    return ang

def angle_between_vectors_pitompi(v1, v2):
    """

    :param v1: [x,y]
    :param v2: [x,y]
    :return: angle in radian -pi to pi
    """
    ang1 = phase(complex(v1[0],v1[1]))
    ang2 = phase(complex(v2[0],v2[1]))
    ang = ang2-ang1
    if ang>pi:
        ang-=2*pi
    elif ang<-pi:
        ang += 2*pi
    return ang

def angle_between_vectors_complex(v1, v2):
    ang1 = phase(-v1)
    ang2 = phase(v2)
    ang = ang2-ang1
    if ang<0:
        ang = ang+2*pi
    #print("v1, v2, ang== = ",v1,v2,ang*180/pi)
    return ang

def rotation_3D(point, phi, theta, psi):
    """
    rotate vector around axis
    https://stackoverflow.com/questions/23330582/how-to-calculate-rotation-matrix-in-android-from-accelerometer-and-magnetometer
    return rotated vector of point
    :param point: [x,y,z]
    :param phi:     rotation around x axis (degree)
    :param theta:   rotation around y axis
    :param psi:     rotation around z axis
    :return:        rotation result [x,y,z]
    """
    phi = phi*pi/180
    theta = theta*pi/180
    psi = psi*pi/180
    x= point[0]
    y=point[1]
    z=point[2]

    rot_mat = [['' for i in range(3)] for j in range(3)]
    cophi = cos(phi)
    siphi = sin(phi)
    copsi = cos(psi)
    sipsi = sin(psi)
    coth = cos(theta)
    sith = sin(theta)
    rot_mat[0][0] = cophi*copsi - siphi*sipsi*sith
    rot_mat[0][1] = siphi*coth
    rot_mat[0][2] = cophi*sipsi + siphi*copsi*sith

    rot_mat[1][0] = -siphi*copsi - cophi*sipsi*sith
    rot_mat[1][1] = cophi*coth
    rot_mat[1][2] = -siphi*sipsi+cophi*copsi*sith

    rot_mat[2][0] = -sipsi*coth
    rot_mat[2][1] = -sith
    rot_mat[2][2] = copsi*coth
    ret_point = []
    for i in range(3):
        ret_point.append(rot_mat[i][0]*x + rot_mat[i][1]*y + rot_mat[i][2]*z)

    print("input" , point, "return", ret_point)
    return ret_point

def rotation_2D(point, phi):
    phi = phi*pi/180
    x = point[0]
    y = point[1]
    x_ret = cos(phi)*x - sin(phi)*y
    y_ret = sin(phi)*x + cos(phi)*y
    return [x_ret, y_ret]

def rotate_around_center(point, phi, center):
    """
    rotate around center in 2D
    :param point:
    :param phi:
    :param center: [cx, cy]
    :return:
    """
    #phi = phi*pi/180
    x = point[0] - center[0]
    y = point[1] - center[1]
    x_ret = cos(phi)*x - sin(phi)*y + center[0]
    y_ret = sin(phi)*x + cos(phi)*y + center[1]
    return [x_ret, y_ret]

def rotation_2D_complex(v, phi):
    """
    rotate complex vector
    :param v: input vector in complex
    :param phi: angle of rotation, radian
    :return:
    """
    x = v.real
    y = v.imag
    x_ret = cos(phi)*x - sin(phi)*y
    y_ret = sin(phi)*x + cos(phi)*y
    return complex(x_ret, y_ret)

def norm_vec(v):
    """
    get norm vector of input vector
    :param v:
    :return:
    """
    x = v.real
    y = v.imag
    size = abs(v)
    if size !=0:
        x_ret = -y/size
        y_ret = x/size
        return complex(x_ret, y_ret)
    else:
        return None


def swap(P1, P2):
    import copy
    save = copy.deepcopy(P2[1])
    P2[1] = copy.deepcopy(P1[1])
    P1[1] = save
    return P1, P2

def swap_points(P1, P2):
    return P2, P1

def swap_path_vec(path):

    return [path[1], path[0]]

def invert_y(P):
    return [-P[0], P[1]]

def circle_point(center, radius, angle):
    """
    return coordinate from center and angle in degree
    :param center: [cx,cy]
    :param angle: 0~2pi
    :return:
    """
    ang = angle
    x = center[0] + radius*cos(ang)
    y = center[1] + radius*sin(ang)
    return([x,y])

if __name__ == '__main__':
    point = [1,1,1]
    phi = 45
    theta = 0
    psi = 0
    rotation_3D(point, phi, theta, psi)