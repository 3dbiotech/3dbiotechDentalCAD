import bpy

##### FUNCIONES COLORES
def asignarcolor(a):
    if bpy.context.selected_objects != []:
        for x in bpy.context.object.material_slots:  # For all of the materials in the selected object:
            bpy.context.object.active_material_index = 0  # select the top material
            bpy.ops.object.material_slot_remove()  # delete it
        b = str(a)
        activeObject = bpy.context.active_object
        mat = bpy.data.materials[b]
        activeObject.data.materials.append(mat)
        b = (a)


def color():
    bpy.data.materials.new(name="Transparente")  # set new material to variable
    bpy.data.materials['Transparente'].diffuse_color = (1, 1, 1, 0.36)
    bpy.data.materials.new(name="CASTABLE")  # set new material to variable
    bpy.data.materials['CASTABLE'].diffuse_color = (0.168269, 0.0159962, 0.226966, 1)
    bpy.data.materials['CASTABLE'].metallic = 0
    bpy.data.materials['CASTABLE'].specular_intensity = 0
    bpy.data.materials['CASTABLE'].roughness = 1
    bpy.data.materials.new(name="DRAFT")  # set new material to variable
    bpy.data.materials['DRAFT'].diffuse_color = (0.246201, 0.250158, 0.266356, 1)
    bpy.data.materials['DRAFT'].metallic = 0
    bpy.data.materials['DRAFT'].specular_intensity = 0
    bpy.data.materials['DRAFT'].roughness = 1
    bpy.data.materials.new(name="DENTURETEETH")  # set new material to variable
    bpy.data.materials['DENTURETEETH'].diffuse_color = (0.73046, 0.651405, 0.533276, 1)
    bpy.data.materials['DENTURETEETH'].metallic = 0
    bpy.data.materials['DENTURETEETH'].specular_intensity = 0
    bpy.data.materials['DENTURETEETH'].roughness = 1
    bpy.data.materials.new(name="DENTUREBASE")  # set new material to variable
    bpy.data.materials['DENTUREBASE'].diffuse_color = (0.947306, 0.527115, 0.48515, 1)
    bpy.data.materials['DENTUREBASE'].metallic = 0
    bpy.data.materials['DENTUREBASE'].specular_intensity = 0
    bpy.data.materials['DENTUREBASE'].roughness = 1
    bpy.data.materials.new(name="MODEL")  # set new material to variable
    bpy.data.materials['MODEL'].diffuse_color = (1, 0.644479, 0.341914, 1)
    bpy.data.materials['MODEL'].metallic = 0
    bpy.data.materials['MODEL'].specular_intensity = 0
    bpy.data.materials['MODEL'].roughness = 1
    bpy.data.materials.new(name="IBT")  # set new material to variable
    bpy.data.materials['IBT'].diffuse_color = (0.768151, 0.768151, 0.266356, 1)
    bpy.data.materials['IBT'].metallic = 0
    bpy.data.materials['IBT'].specular_intensity = 0
    bpy.data.materials['IBT'].roughness = 1
    bpy.data.materials.new(name="BIOMED")  # set new material to variable
    bpy.data.materials['BIOMED'].diffuse_color = (0.17144, 0.610495, 0.637597, 0.7)
    bpy.data.materials['BIOMED'].metallic = 0
    bpy.data.materials['BIOMED'].specular_intensity = 0
    bpy.data.materials['BIOMED'].roughness = 1


##### FUNCIONES

def activeaddons():
    bpy.ops.preferences.addon_enable(module="object_print3d_utils")
    bpy.ops.preferences.addon_enable(module="mesh_looptools")
    bpy.ops.preferences.addon_enable(module="object_boolean_tools")
    bpy.ops.preferences.addon_enable(module="add_curve_extra_objects")
    bpy.ops.preferences.addon_enable(module="add_mesh_extra_objects")
    bpy.ops.preferences.addon_enable(module="measureit")
    bpy.ops.preferences.addon_enable(module="io_mesh_stl")
    bpy.ops.preferences.addon_enable(module="io_scene_obj")
    bpy.ops.preferences.addon_enable(module="io_mesh_ply")


def delete_all():
    for o in bpy.data.objects:
        bpy.data.objects.remove(o)


def borrartodascolecciones():
    for o in bpy.data.collections:
        bpy.data.collections.remove(o)


def borrartodosmateriales():
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)


def borrartodasmallas():
    for mallas in bpy.data.meshes:
        bpy.data.meshes.remove(mallas)


def borrartodasactions():
    for act in bpy.data.actions:
        bpy.data.actions.remove(act)


def set_mm():
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.space_data.overlay.grid_scale = 0.001


def set_clipping_planes():
    bpy.context.space_data.lens = 50
    bpy.context.space_data.clip_start = 1
    bpy.context.space_data.clip_end = 1e+006


def createcoll(cole):
    # Create new collection
    collection = bpy.data.collections.new(name=cole)
    scene = bpy.context.scene
    scene.collection.children.link(collection)


def crearcoleccionsinoexiste(cole):
    collectionFound = False
    print("START **************")
    for myCol in bpy.data.collections:
        print(myCol.name)
        if myCol.name == cole:
            collectionFound = True
            print("Collection found in scene")
            break
    if collectionFound == False:
        myCol = bpy.data.collections.new(cole)
        bpy.context.scene.collection.children.link(myCol)  # Creates a new collection
        print("created")
    else:
        print("exists already")


# Play /Stop Animation
def playanimation():
    bpy.ops.screen.animation_play()


def startanimation():
    bpy.context.scene.frame_set(0)


def endanimation():
    bpy.context.scene.frame_set(5)


def sculptobject():
    ob = bpy.context.selected_objects
    if ob == []:
        pass
    else:
        exitmode()

        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.sculpt.sculptmode_toggle()

        active_object = bpy.context.view_layer.objects.active

        if active_object.mode == "SCULPT" and not active_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()

        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Simplify")

        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

        bpy.context.scene.tool_settings.sculpt.detail_size = 6

        bpy.data.brushes["Simplify"].auto_smooth_factor = 0.1
        bpy.data.brushes["Simplify"].strength = 0
        bpy.context.scene.tool_settings.unified_paint_settings.size = 80

        bpy.data.brushes["Simplify"].use_automasking_topology = True
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'

        bpy.context.space_data.show_region_tool_header = True

        bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False

        bpy.context.scene.tool_settings.use_snap = False

        bpy.ops.ed.undo_push()


def flattenobject():
    ob = bpy.context.selected_objects
    if ob == []:
        pass
    else:

        exitmode()

        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.sculpt.sculptmode_toggle()

        active_object = bpy.context.view_layer.objects.active

        if active_object.mode == "SCULPT" and not active_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()

        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Flatten")

        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

        bpy.context.scene.tool_settings.sculpt.detail_size = 6

        bpy.data.brushes["Flatten/Contrast"].auto_smooth_factor = 0.1
        bpy.data.brushes["Flatten/Contrast"].strength = 0
        bpy.context.scene.tool_settings.unified_paint_settings.size = 80

        bpy.data.brushes["Flatten/Contrast"].use_automasking_topology = True
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'

        bpy.context.space_data.show_region_tool_header = True

        bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False

        bpy.context.scene.tool_settings.use_snap = False

        bpy.ops.ed.undo_push()


def smoothobject():
    ob = bpy.context.selected_objects
    if ob == []:
        pass
    else:
        exitmode()
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.sculpt.sculptmode_toggle()

        active_object = bpy.context.view_layer.objects.active

        if active_object.mode == "SCULPT" and not active_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()

        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Smooth")

        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

        bpy.context.scene.tool_settings.sculpt.detail_size = 6

        bpy.data.brushes["Smooth"].direction = 'SMOOTH'

        # bpy.data.brushes["Smooth/Contrast"].auto_smooth_factor = 0.1
        bpy.data.brushes["Smooth"].strength = 0.5
        bpy.context.scene.tool_settings.unified_paint_settings.size = 50

        # bpy.data.brushes["Smooth/Contrast"].use_automasking_topology = True
        # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'

        bpy.context.space_data.show_region_tool_header = True

        bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False

        bpy.context.scene.tool_settings.use_snap = False

        bpy.ops.ed.undo_push()


def Inflateobject():
    ob = bpy.context.selected_objects
    if ob == []:
        pass
    else:
        exitmode()
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.object.convert(target='MESH')
        bpy.ops.sculpt.sculptmode_toggle()

        active_object = bpy.context.view_layer.objects.active

        if active_object.mode == "SCULPT" and not active_object.use_dynamic_topology_sculpting:
            bpy.ops.sculpt.dynamic_topology_toggle()

        bpy.ops.wm.tool_set_by_id(name="builtin_brush.Inflate/Deflate")

        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)

        bpy.context.scene.tool_settings.sculpt.detail_size = 6

        bpy.data.brushes["Inflate/Deflate"].direction = 'INFLATE'

        bpy.data.brushes["Inflate/Deflate"].auto_smooth_factor = 0.2
        bpy.data.brushes["Inflate/Deflate"].strength = 0.3
        bpy.context.scene.tool_settings.unified_paint_settings.size = 30

        # bpy.data.brushes["Smooth/Contrast"].use_automasking_topology = True
        # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'

        bpy.context.space_data.show_region_tool_header = True

        bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
        bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False

        bpy.context.scene.tool_settings.use_snap = False

        bpy.ops.ed.undo_push()


def exitmode():
    cont = bpy.context.mode
    if cont == 'SCULPT':
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.ed.undo_push()


def reinicio():
    # delete_all()
    # borrartodascolecciones()
    # borrartodosmateriales()
    # borrartodasmallas()
    borrartodasactions()
    set_mm()
    set_clipping_planes()
    crearcoleccionsinoexiste("OriginalModels")
    crearcoleccionsinoexiste("Reconstruccion")
    activeaddons()
    # Materiales basicos
    color()
    addlampcamera()


def addlampcamera():
    lamp_data = bpy.data.lights.new(name="Lamp", type='POINT')
    lamp_data.energy = 200000
    lamp_object = bpy.data.objects.new(name="Lamp", object_data=lamp_data)
    bpy.context.collection.objects.link(lamp_object)
    lamp_object.location = (0, -150, 80)

    scn = bpy.context.scene

    # create the first camera
    cam1 = bpy.data.cameras.new("Camera 1")
    cam1.lens = 18

    # create the first camera object
    cam_obj1 = bpy.data.objects.new("Camera 1", cam1)
    cam_obj1.location = (10, -60, 5)
    cam_obj1.rotation_euler = (1.5, 0, 0.175)
    scn.collection.objects.link(cam_obj1)


def hideact():
    bpy.ops.object.hide_view_set()


def showact():
    bpy.ops.object.hide_view_clear()


def undo():
    bpy.ops.ed.undo()


def redo():
    bpy.ops.ed.redo()


def showhidelower():
    milista = ['lower']  # , 'Working_model', 'upper', 'nunca', 'ObjectMakingCut' # Para seleccionar solo estos
    seleccionado = []
    # Deseleccionar todo
    bpy.ops.object.select_all(action='DESELECT')
    # Meter objeto en lista seleccionado si esta en milista y si existe
    for o in bpy.data.objects:
        if o.name in milista:
            seleccionado.append(o)
    # Selecciono todo lo de la lista seleccionado
    for o in seleccionado:
        if o.visible_get():
            o.hide_set(True)
        else:
            o.hide_set(False)  # Hago visible si esta oculto para poder ser seleccionado


def showhideupper():
    milista = ['upper']  # , 'Working_model', 'upper', 'nunca', 'ObjectMakingCut' # Para seleccionar solo estos
    seleccionado = []
    # Deseleccionar todo
    bpy.ops.object.select_all(action='DESELECT')
    # Meter objeto en lista seleccionado si esta en milista y si existe
    for o in bpy.data.objects:
        if o.name in milista:
            seleccionado.append(o)
    # Selecciono todo lo de la lista seleccionado
    for o in seleccionado:
        if o.visible_get():
            o.hide_set(True)
        else:
            o.hide_set(False)  # Hago visible si esta oculto para poder ser seleccionado


def showhidesplint():
    milista = ['Splint']  # , 'Working_model', 'upper', 'nunca', 'ObjectMakingCut' # Para seleccionar solo estos
    seleccionado = []
    # Deseleccionar todo
    bpy.ops.object.select_all(action='DESELECT')
    # Meter objeto en lista seleccionado si esta en milista y si existe
    for o in bpy.data.objects:
        if o.name in milista:
            seleccionado.append(o)
    # Selecciono todo lo de la lista seleccionado
    for o in seleccionado:
        if o.visible_get():
            o.hide_set(True)
        else:
            o.hide_set(False)  # Hago visible si esta oculto para poder ser seleccionado


def showsplint():
    milista = ['Splint']  # , 'Working_model', 'upper', 'nunca', 'ObjectMakingCut' # Para seleccionar solo estos
    seleccionado = []
    # Deseleccionar todo
    bpy.ops.object.select_all(action='DESELECT')
    # Meter objeto en lista seleccionado si esta en milista y si existe
    for o in bpy.data.objects:
        if o.name in milista:
            seleccionado.append(o)
    # Selecciono todo lo de la lista seleccionado
    for o in seleccionado:
        o.hide_set(False)  # Hago visible si esta oculto para poder ser seleccionado
        o.select_set(True)  # Queda seleccionado objeto
        # Funciones ejemplo a realizar a cada objeto
        bpy.ops.object.select_all(action='INVERT')
        bpy.ops.object.hide_view_set()


def showslu():
    milista = ['Splint', 'upper',
               'lower']  # , 'Working_model', 'upper', 'nunca', 'ObjectMakingCut' # Para seleccionar solo estos
    seleccionado = []
    # Deseleccionar todo
    bpy.ops.object.select_all(action='DESELECT')
    # Meter objeto en lista seleccionado si esta en milista y si existe
    for o in bpy.data.objects:
        if o.name in milista:
            seleccionado.append(o)
    # Selecciono todo lo de la lista seleccionado
    for o in seleccionado:
        o.hide_set(False)  # Hago visible si esta oculto para poder ser seleccionado
        o.select_set(True)  # Queda seleccionado objeto
        # Funciones ejemplo a realizar a cada objeto
        bpy.ops.object.select_all(action='INVERT')
        bpy.ops.object.hide_view_set()
