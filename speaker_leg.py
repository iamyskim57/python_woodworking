def spkleg_3leg(height, garo, sero, leg_width, tool_radius, thick):
    """

    :param height:
    :param garo:
    :param sero:
    :param leg_width:
    :param tool_radius:
    :param thick:
    :return:
    """
    h = height + tool_radius * 2-2*thick
    jl = leg_width / 2  # joiner length
    fp, fname = gui_open_utility.open_file_to_write(parameter.design_data,
                            [("path files", "*.pth")], ".pth")
    hole_radius = leg_width*0.65
    p1 = [-h / 2, 0]
    p2 = [-h / 4-hole_radius, p1[1]]
    p3 = [p2[0],hole_radius+tool_radius]
    p4 = [p3[0]+hole_radius+tool_radius, p3[1]]
    delta = math.sqrt(0.5)*(hole_radius + tool_radius)
    p5 = [p4[0]+delta, delta]
    p6 = [p4[0]+(hole_radius+tool_radius), 0]
    p7 = [-p6[0], 0]
    p8 = [p7[0], p3[1]]
    p9 = [-p4[0], p4[1]]
    p10 = [p9[0]+delta, delta]
    p11 = [-p2[0], 0]
    p12 = [-p1[0], 0]
    p13 = [p12[0], jl/2-tool_radius]
    p14 = [p13[0]+thick, p13[1]]
    p15 = [p14[0], p14[1]+jl+2*tool_radius]
    p16 = [p13[0], p15[1]]
    p17 = [p16[0], leg_width+2*tool_radius]
    p18 = [-p17[0], p17[1]]
    p19 = [p18[0], p16[1]]
    p20 = [-p15[0], p15[1]]
    p21 = [-p14[0], p14[1]]
    p22 = [-p13[0], p13[1]]

    out = 'LINE '+fstr_point_coordinate(p1) +fstr_point_coordinate(p2) +'\n'
    out += "LINETO"+fstr_point_coordinate((p3))+'\n'
    out += "LINETO"+fstr_point_coordinate((p4))+'\n'
    out += 'ARCTO ' + fstr_point_coordinate(p5) + fstr_point_coordinate(p6) +'\n'
    out += "LINETO" + fstr_point_coordinate((p7)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p8)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p9)) + '\n'
    out += 'ARCTO ' + fstr_point_coordinate(p10) + fstr_point_coordinate(p11) + '\n'
    out += "LINETO" + fstr_point_coordinate((p12)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p13)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p14)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p15)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p16)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p17)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p18)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p19)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p20)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p21)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p22)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p1)) + '\n'

    p1[1] = -p1[1]
    p2[1] = -p2[1]
    p3[1] = -p3[1]
    p4[1] = -p4[1]
    p5[1] = -p5[1]
    p6[1] = -p6[1]
    p7[1] = -p7[1]
    p8[1] = -p8[1]
    p9[1] = -p9[1]
    p10[1] = -p10[1]
    p11[1] = -p11[1]
    p12[1] = -p12[1]
    p13[1] = -p13[1]
    p14[1] = -p14[1]
    p15[1] = -p15[1]
    p16[1] = -p16[1]
    p17[1] = -p17[1]
    p18[1] = -p18[1]
    p19[1] = -p19[1]
    p20[1] = -p20[1]
    p21[1] = -p21[1]
    p22[1] = -p22[1]
    out += 'LINETO ' +fstr_point_coordinate(p2) +'\n'
    out += "LINETO"+fstr_point_coordinate((p3))+'\n'
    out += "LINETO"+fstr_point_coordinate((p4))+'\n'
    out += 'ARCTO ' + fstr_point_coordinate(p5) + fstr_point_coordinate(p6) +'\n'
    out += "LINETO" + fstr_point_coordinate((p7)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p8)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p9)) + '\n'
    out += 'ARCTO ' + fstr_point_coordinate(p10) + fstr_point_coordinate(p11) + '\n'
    out += "LINETO" + fstr_point_coordinate((p12)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p13)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p14)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p15)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p16)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p17)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p18)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p19)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p20)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p21)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p22)) + '\n'
    out += "LINETO" + fstr_point_coordinate((p1)) + '\n'
    joint_hole_center_y = thick*math.tan(30*math.pi/180)/2 + jl
    jh1 = [0,joint_hole_center_y]
    jh2  = vector_oper.rotation_2D(jh1,120)
    jh3 = vector_oper.rotation_2D(jh1,-120)
    header = ('# height(length), base_garo, base_sero ' + fstr(height) +
              ' ' + fstr(garo) + ' ' + fstr(sero) + '\n')
    header += '# material thickness:' + fstr(thick) \
                      + ', tool_radius:' + fstr(tool_radius) + '\n'
    header += '# Top assembly hole : size (' + fstr(thick) + ', ' + fstr(jl)  + ')\n'
    header += '# Top assembly hole centers (' + fstr_point_coordinate(jh1) + ('), '
        '(') + fstr_point_coordinate(jh2)+ '), (' + fstr_point_coordinate(jh3)+')\n'
    out = header + out
    fp.write(out)
    fp.close()
    messagebox.showinfo("Path & Parameter file", "Speaker Leg path data written to " + fname + "\n")
    fp.close()
