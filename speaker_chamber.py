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
