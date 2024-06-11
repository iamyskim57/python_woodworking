"""
Generate Star shape Hole or Post
"""
import math, copy
from tkinter import filedialog
from tkinter import messagebox, simpledialog

def message_ans(title, msg):
    ans = simpledialog.askstring(title = title, prompt = msg)
    return ans

def rotate(point, phi):
    """
    rotate point around origin
    :param point: [x,y]
    :param phi: rotation angle in radian
    :return:
    """
    x = point[0]
    y = point[1]
    x_ret = math.cos(phi)*x - math.sin(phi)*y
    y_ret = math.sin(phi)*x + math.cos(phi)*y
    return [x_ret, y_ret]

def gen_star(R,num_edge,tool_radius,hole_or_post):
    """

    :param R: radius of star
    :param num_edge: 꼭지점 갯수
    :param tool_radius:
    :param hole_or_post: "H" or "P"
    :return: point list
    """
    theta = 2*math.pi/num_edge  #
    delta = math.pi*(1-4/num_edge)  #꼭지 각도
    phi = math.pi-theta #다각형 꼭지 각도
    r = R*math.sin(delta/2)     #다각별 내부 다각형 내접원 반경
    r1 = r/math.cos(theta/2)    #다각별 내부 다각형 외접원 반경
    eta = (math.pi-theta)/2
    tb = tool_radius/math.sin(phi/2)
    ta = tool_radius/math.sin(delta/2)
    rp = r1+tb      #post 내부 다각형 꼭지점 반경
    rh = r1-tb      #hole 내부 다각형 꼭지점 반경
    Rp = R+ta       #post 별 꼭지점 반경
    Rh = R-ta       #hole 별 꼭지점 반경
    if hole_or_post == "P":
        Rs = Rp
        rs = rp
    else:
        Rs = Rh
        rs = rh
    P1 = [rs*math.cos(eta), rs*math.sin(eta)]
    P2 = [0,Rs]
    points = []
    for i in range(num_edge):
        p1 = copy.deepcopy(P1)
        p2 = copy.deepcopy(P2)
        ang = theta*i
        p1 = rotate(p1,ang)
        p2 = rotate(p2,ang)
        points.append(p1)
        points.append(p2)
    points.append(points[0])
    file_path = filedialog.asksaveasfilename(defaultextension=".pts",
        filetypes=[("pointlist files", "*.pts")])  # 파일 탐색기를 열고 파일 경로를 얻음.
    fp = open(file_path, "w")
    fp.write(str(points))
    print("r1 = ",r1)
    fp.close()

if __name__ == '__main__':
    ans = simpledialog.askstring(title="Star Generator", prompt="Type:Hole('H')/Post('P'), Radius, 꼭지점수, Tool반경")
    ans = ans.replace(',',' ')
    parm =ans.split()
    post_or_hole=parm[0]
    radius = float(parm[1])
    num_edge = int(parm[2])
    tool_radius = float(parm[3])
    gen_star(radius,num_edge, tool_radius
             ,post_or_hole)
