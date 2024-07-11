def stool_outline(height, base_width, top_diameter, tool_radius, thick, assy_margin = 0.1):
    """
    generate .pth file (for stool outline ) and .json file containg holes (for assembly)
    refer to stool_generation.ppt for p1 to p8 in this module
    :param height: height of stool
    :param base_width: ground_level width
    :param top_diameter: diameter of top plate
    :param tool_radius
    :param thick: material thickness
    :param assy_margin : assembly margin
    :return:
    """

    fp,fname = gui_open_utility.open_file_to_write(parameter.design_data, [("path files", "*.pth")],".pth")
    # points on 1 quadrant
    p1 = [0, base_width/2+tool_radius]
    p3 = [height - thick+tool_radius, top_diameter/2+tool_radius]
    p2 = [(p1[0]+p3[0])/2, (p1[1]+p3[1])/2+10]
    p4 = [p3[0],top_diameter/6*2+top_diameter/12+tool_radius]
    p5 = [p4[0]+thick,p4[1]]
    p6 = [p5[0],top_diameter/6+top_diameter/12-tool_radius]
    top_hole_length = p5[1]-p6[1]-tool_radius*2
    top_hole_center = [(p5[1]+p6[1])/2,0]
    p7=[p4[0],p6[1]]
    p8 = [p4[0],0]
    #
    # base material size :
    long_axis = 2*p5[0] + 2*tool_radius
    short_axis = 2*p1[1] + 2*tool_radius
    p9 = [top_diameter/2+tool_radius*2,0]
    leg_assy_hole_length = (p8[0]-tool_radius-p9[0])/2
    leg_assy_hole_center1 = p9[0] + leg_assy_hole_length/2
    leg_assy_hole_center2 = leg_assy_hole_center1 + leg_assy_hole_length

    out='INTER '+ fstr(p1[0]) + ' '+ fstr(p1[1])+' '\
        + fstr(p2[0]) + ' ' + fstr(p2[1]) + ' '+ fstr(p3[0]) + ' '\
    + fstr(p3[1])+'\n'
    out += 'LINETO '+ fstr(p4[0]) + ' ' + fstr(p4[1]) + '\n'
    out += 'LINETO ' + fstr(p5[0]) + ' ' + fstr(p5[1]) + '\n'
    out += 'LINETO ' + fstr(p6[0]) + ' ' + fstr(p6[1]) + '\n'
    out += 'LINETO ' + fstr(p7[0]) + ' ' + fstr(p7[1]) + '\n'
    out += 'LINETO ' + fstr(p8[0]) + ' ' + fstr(p8[1]) + '\n'

    p1[1] = -p1[1]
    p2[1] = -p2[1]
    p3[1] = -p3[1]
    p4[1] = -p4[1]
    p5[1] = -p5[1]
    p6[1] = -p6[1]
    p7[1] = -p7[1]
    out += 'LINETO ' + fstr(p7[0]) + ' ' + fstr(p7[1]) + '\n'
    out += 'LINETO ' + fstr(p6[0]) + ' ' + fstr(p6[1]) + '\n'
    out += 'LINETO ' + fstr(p5[0]) + ' ' + fstr(p5[1]) + '\n'
    out += 'LINETO ' + fstr(p4[0]) + ' ' + fstr(p4[1]) + '\n'
    out += 'LINETO ' + fstr(p3[0]) + ' ' + fstr(p3[1]) + '\n'
    out += 'INTER '+ fstr(p3[0]) + ' '+ fstr(p3[1])+' '\
        + fstr(p2[0]) + ' ' + fstr(p2[1]) + ' '+ fstr(p1[0]) + ' '\
    + fstr(p1[1])+'\n'

    p1[0] = -p1[0]
    p2[0] = -p2[0]
    p3[0] = -p3[0]
    p4[0] = -p4[0]
    p5[0] = -p5[0]
    p6[0] = -p6[0]
    p7[0] = -p7[0]
    p8[0] = -p8[0]

    out+='INTER '+ fstr(p1[0]) + ' '+ fstr(p1[1])+' '\
        + fstr(p2[0]) + ' ' + fstr(p2[1]) + ' '+ fstr(p3[0]) + ' '\
    + fstr(p3[1])+'\n'
    out += 'LINETO '+ fstr(p4[0]) + ' ' + fstr(p4[1]) + '\n'
    out += 'LINETO ' + fstr(p5[0]) + ' ' + fstr(p5[1]) + '\n'
    out += 'LINETO ' + fstr(p6[0]) + ' ' + fstr(p6[1]) + '\n'
    out += 'LINETO ' + fstr(p7[0]) + ' ' + fstr(p7[1]) + '\n'

    p1[1] = -p1[1]
    p2[1] = -p2[1]
    p3[1] = -p3[1]
    p4[1] = -p4[1]
    p5[1] = -p5[1]
    p6[1] = -p6[1]
    p7[1] = -p7[1]
    out += 'LINETO ' + fstr(p7[0]) + ' ' + fstr(p7[1]) + '\n'
    out += 'LINETO ' + fstr(p6[0]) + ' ' + fstr(p6[1]) + '\n'
    out += 'LINETO ' + fstr(p5[0]) + ' ' + fstr(p5[1]) + '\n'
    out += 'LINETO ' + fstr(p4[0]) + ' ' + fstr(p4[1]) + '\n'
    out += 'LINETO ' + fstr(p3[0]) + ' ' + fstr(p3[1]) + '\n'
    out += 'INTER '+ fstr(p3[0]) + ' '+ fstr(p3[1])+' '\
        + fstr(p2[0]) + ' ' + fstr(p2[1]) + ' '+ fstr(p1[0]) + ' '\
    + fstr(p1[1])+'\n'
    header = '# height base_width, top_diamter ' + fstr(height)
    header += ' ' + fstr(base_width) + ' '+fstr(top_diameter) + '\n'
    header += '# Material Size ' + fstr(long_axis) + ' X ' + fstr(short_axis) + '\n'

    header += '# Material thickness '+ fstr(thick) \
              + ' tool_radius' + fstr(tool_radius) + '\n'
    header += '# Top assembly hole : size ('+fstr(thick+assy_margin) + ', ' + fstr(top_hole_length+assy_margin) + ') center (' \
              + fstr(top_hole_center[0]) + ' ,' + fstr(top_hole_center[1])+'\n'
    header += '# leg assy hole : size (' + fstr(thick+assy_margin) + ' ,' + fstr(leg_assy_hole_length) \
              +') center at ' + fstr(leg_assy_hole_center1) +' ' \
              +fstr(-leg_assy_hole_center2) +'\n'
    out = header+out
    # Prepare design file containing base and holes
    name = fname[:-4]+'.json'
    design_data = []
    base = geometric_shapes.object_template("BASE")
    base["LONG_AXIS"] = long_axis
    base["SHORT_AXIS"] = short_axis
    base["HEIGHT"] = thick
    design_data.append(base)
    leg_assy_hole = geometric_shapes.object_template("RECTANGULAR_HOLE")
    leg_assy_hole["LONG_AXIS"] = leg_assy_hole_length
    leg_assy_hole["SHORT_AXIS"] = thick+assy_margin
    leg_assy_hole["CENTER"] = [leg_assy_hole_center1,0]
    leg_assy_hole["DEPTH"] = thick+1
    design_data.append(leg_assy_hole)
    leg_assy_hole_other = copy.deepcopy(leg_assy_hole)
    leg_assy_hole_other["CENTER"] = [-leg_assy_hole_center2,0]
    design_data.append(leg_assy_hole_other)
    top_assy_hole = copy.deepcopy(leg_assy_hole)
    top_assy_hole["LONG_AXIS"] = top_hole_length+assy_margin
    top_assy_hole["SHORT_AXIS"] = thick+assy_margin
    top_assy_hole["CENTER"] = top_hole_center
    design_data.append(top_assy_hole)
    top_assy_hole1 = copy.deepcopy(top_assy_hole)
    top_assy_hole1["CENTER"] = [-top_hole_center[0], 0]
    design_data.append(top_assy_hole1)
    top_assy_hole2 = copy.deepcopy(top_assy_hole)
    top_assy_hole2["LONG_AXIS"] = top_assy_hole["SHORT_AXIS"]
    top_assy_hole2["SHORT_AXIS"] = top_assy_hole["LONG_AXIS"]
    top_assy_hole2["CENTER"] = [0,top_assy_hole["CENTER"][0]]
    design_data.append(top_assy_hole2)
    top_assy_hole3 = copy.deepcopy(top_assy_hole2)
    top_assy_hole3["CENTER"][1] = -top_assy_hole2["CENTER"][1]
    design_data.append(top_assy_hole3)
    json.dump(design_data, open(name, 'w'))
    out += "# Hole data written on file : " + name + "\n"
    fp.write(out)
    fp.close()
    messagebox.showinfo("Path file", "path data written to" + fname + " hole design file : " + name + "\n")
