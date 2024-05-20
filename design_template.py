def template_json(file_name, base_length, base_width, base_thickness):
    """

    :param file_name:
    :param base_length:
    :param base_width:
    :param base_thickness:
    :return:
    """
    objects = []
    # 모재의 형태를 지정함
    base_material = geometric_shapes.object_template("BASE")
    base_material["LONG_AXIS"] = base_length
    base_material["SHORT_AXIS"] = base_width
    base_material["HEIGHT"] = base_thickness
    objects.append(base_material)
#-------------------------------------------------------------------------
    #디자인 요소들을 추가함.
    # Center hole
    hole = geometric_shapes.object_template(("CIRCULAR_HOLE"))
    """object_template 의 종류
     "BASE", "POLYGON_HOLE", "POLYGON_POST",  "RECTANGULAR_HOLE", "RECTANGULAR_POST"
     "CIRCULAR_HOLE","CIRCULAR_POST", "DRILL","LINE","ARC"
     "MULTI_TRENCH","SIDE_TRENCH","CURVE"  """
    # CIRCULAY HOLE 을 삽입 -- 삭제하고 다른  object들을 추가함
    hole["RADIUS"] = 50
    hole["TOP_SURFACE"] = 0
    hole["DEPTH"] = base_material["HEIGHT"] + 1
    hole["TOOL_NUMBER"] = 0
    hole["PLANE"] = "TOP"
    hole["Z_home"] = 20
    hole["CENTER"] = [0, 0]
    objects.append(hole)
    #최외곽을 구성 요소 추가. 최외곽은 POST 또는 CURVE 로 지정 -> 삭제하고 필요한 형태로 교체함
    outer_circle = geometric_shapes.object_template("CIRCULAR_POST")
    outer_circle["RADIUS"] = 175
    outer_circle["CENTER"] = [0,0]
    outer_circle["HEIGHT"] = base_material["HEIGHT"] + 1
    outer_circle["TOP_SURFACE"] = 0
    outer_circle["PLANE"] = "TOP"
    outer_circle["Z_home"] = 20
    outer_circle["TOOL_NUMBER"] = 0
    objects.append(outer_circle)
#-------------------------------------------------------------------------
    #생성된 Design file 을 저장함.
    filename, file_extension = os.path.splitext(file_name)
    outfilename = filename + '.json'
    json.dump(objects, open(outfilename, 'w'))
