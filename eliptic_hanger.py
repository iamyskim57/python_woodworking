import math
import matplotlib.pyplot as plt
import vector_oper
def eliptic_perimeter_points(a,b,n,num_division,desired_perimeter_length):
    """
    타원주 상에 등간격으로 배치된 점들의 좌표를 구한다
    :param a: 수평반지름
    :param b: 수직반지름
    :param n: 타원의 원주길이를 계산하기 위하여 나누는 갯수
    :param num_division: 등간격 배치 point 의 갯수
    :param desired_perimeter_length: 목표로하는 타원주의 길이
    :return: 조정된 수평반지름, 수직반지름, 좌표 list
    """
    del_theta = math.pi/n*2
    theta = 0
    peri = []
    peri_length = 0
    x_f = a*math.cos(-del_theta/2)
    y_f = b*math.sin(-del_theta/2)
    for i in range(n):
        x=a*math.cos(theta)
        y = b*math.sin(theta)
        r = math.sqrt(x**2+y**2)
        d_length = vector_oper.length([x_f,y_f],[x,y])
        #peri_length += r*del_theta
        peri_length += d_length
        peri.append(peri_length)
        theta += del_theta
        x_f = x
        y_f = y

    scale_factor = desired_perimeter_length/peri_length
    print("Ellipse %f, %f, circumference length=%f"%(a,b,peri_length))
    a_scale = a*scale_factor
    b_scale = b*scale_factor
    dev_point = []
    target_length = 0
    theta = 0
    del_length = peri_length/num_division
    for i in range(n):
        if target_length<=peri[i]:
            dev_point.append([a_scale*math.cos(theta),b_scale*math.sin(theta)])
            target_length+=del_length
        theta += del_theta
    return(a_scale,b_scale,dev_point)

def point_graph(points):
    """
    좌표 points 로 부터 그림을 그린다.
    :param points:
    :return:
    """
    # 좌표를 각각 x와 y 리스트로 분리
    x = [point[0] for point in points]
    y = [point[1] for point in points]

    # 그래프 그리기
    plt.plot(x, y, marker='o')
    plt.gca().set_aspect('equal')
    # 그래프 제목과 축 레이블 설정
    plt.title('All Points Connected')
    plt.xlabel('X Axis')
    plt.ylabel('Y Axis')

    # 그래프 보여주기
    plt.show()

def generate_eliptic_hanger(points,tool_radius,slot_width,margin):
    depth = 10
    offset_norm = (slot_width+margin)/2-tool_radius
    retpoints=[]
    for point in points:
        print("POINT:",point)
        [dir,norm] = vector_oper.direction_and_normal_vector([0,0],point,"L")
        root_point = vector_oper.linear_sum(point,1,dir,-depth+tool_radius)
        left_root = vector_oper.linear_sum(root_point,1,norm,offset_norm)
        left_root_d= vector_oper.linear_sum(root_point,1,norm,offset_norm+tool_radius)
        right_root = vector_oper.linear_sum(root_point,1,norm,-offset_norm)
        right_root_d = vector_oper.linear_sum(root_point, 1, norm, -(offset_norm+tool_radius))
        left_top = vector_oper.linear_sum(left_root,1,dir,depth)
        right_top = vector_oper.linear_sum(right_root,1,dir,depth)
        retpoints.append(right_top)
        retpoints.append(right_root)
        retpoints.append(right_root_d)
        retpoints.append(right_root)
        retpoints.append(left_root)
        retpoints.append(left_root_d)
        retpoints.append(left_root)
        retpoints.append(left_top)
    retpoints.append(retpoints[0])
    return(retpoints)

if __name__ == '__main__':
    from tkinter import filedialog
    a, b, points = eliptic_perimeter_points(5, 3, 10000, 48, 1440)
    point_graph(points)
    fixpoints=generate_eliptic_hanger(points,2,8,1)
    point_graph(fixpoints)
    file_path = filedialog.asksaveasfilename(defaultextension=".pts",
        filetypes=[("pointlist files", "*.pts")])  # 파일 탐색기를 열고 파일 경로를 얻음.
    fp = open(file_path, "w")
    fp.write(str(fixpoints))
    fp.close()
