
def circular_hanger():
    """
    원주상에 등간격의 Slot 이 배치된 Hanger를 만든다.
    :return:
    """
    import math, vector_oper
    from tkinter import filedialog
    ans = input("Hanger 반경, Slot_갯수, Slot폭, tool반경?")
    ans = ans.replace(',', ' ')
    par = ans.split()
    num_slot = float(par[1])                #Slot 갯수
    slot_width = float(par[2])              #Slot 폭
    tool_radius = float(par[3])
    r_out = float(par[0])+tool_radius   #외곽 반경
    r_in = r_out-10                         #Slot 깊이를 10mm 로 설정
    tt_i = math.asin(slot_width/2/r_in)     #theta_i
    tt_o = math.asin(slot_width/2/r_out)    #theta_o
    del_ang = 2*math.pi/num_slot            #Slot 간 각도
    points=[]
    p1 = [r_in*math.cos(tt_i),slot_width/2-tool_radius]
    p2 = [r_out*math.cos(tt_o),slot_width/2-tool_radius]
    p3 = [p2[0],-p2[1]]
    p4 = [p1[0],-p1[1]]
    for i in range(num_slot):
        p1 = vector_oper.rotate_around_center(p1,-del_ang, [0,0])
        p2 = vector_oper.rotate_around_center(p2,-del_ang, [0,0])
        p3 = vector_oper.rotate_around_center(p3,-del_ang, [0,0])
        p4 = vector_oper.rotate_around_center(p4,-del_ang, [0,0])
        points.append(p2)
        points.append(p1)
        points.append(p4)
        points.append(p3)
    points.append(points[0])
    file_path = filedialog.asksaveasfilename(defaultextension=".pts",
        filetypes=[("pointlist files", "*.pts")])  # 파일 탐색기를 열고 파일 경로를 얻음.
    fp = open(file_path, "w")
    fp.write(str(points))
    fp.close()
