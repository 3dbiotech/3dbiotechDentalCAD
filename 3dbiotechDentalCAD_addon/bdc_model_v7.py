import bpy, sys, os, bmesh, statistics, gpu, time, importlib, blf, time
import numpy as np
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy.types import PropertyGroup
from bpy.props import StringProperty, CollectionProperty, EnumProperty
from gpu_extras.batch import batch_for_shader
from mathutils import Vector
from bpy.props import FloatProperty
from bgl import *
from numpy import True_

####### FUNCIONES

def vista_ortho():
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':
            print(obj.data.type)
            obj.data.type = 'ORTHO'

def mostrarmensaje(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def crearmodelo():
    seleccionado = bpy.context.active_object
    if seleccionado == None:
        #ErrorMsg_call("No hay modelo seleccionado")
        print("No hay modelo seleccionado")
        #mostrarmensaje("Debe seleccionar un objeto")
    elif seleccionado != None:
        if seleccionado is not None and seleccionado.type == 'MESH' and seleccionado.select_get():
            print("ejecutando askmodelocerrado()")   
            obj = bpy.context.object # edit: now gets the currently active object 
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.context.tool_settings.mesh_select_mode = (True, False, False)
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_non_manifold()
            bpy.ops.object.mode_set(mode="OBJECT")
            verts = obj.data.vertices
            sel_verts = [v for v in verts if v.select]#Vertices seleccionados
            if sel_verts == []:
                #ErrorMsg_call("El modelo ya está cerrado")
                print("El modelo ya está cerrado")

            else:
                # set EDIT mode's select mode to "vertex select" 
                objj = bpy.context.selected_objects[0]###############
                objname = objj.name###############################
                print ("EL MODELO PARA CREAR ES EL")
                print(objj.name)##################################
                
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.context.tool_settings.mesh_select_mode = (True , False , False)


                bpy.ops.mesh.select_linked(delimit=set())
                bpy.ops.mesh.reveal()

                bpy.ops.mesh.select_all(action='INVERT')
                bpy.ops.mesh.delete(type='VERT')
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.delete_loose()

                bpy.ops.mesh.reveal()

                bpy.ops.mesh.select_non_manifold()

                bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665, use_dissolve_boundaries=True)

                bpy.ops.mesh.select_all(action='DESELECT')

                bpy.ops.object.editmode_toggle()

                bpy.ops.object.select_all(action='DESELECT') #deselect all object

                ###for x in bpy.context.object.material_slots: #For all of the materials in the selected object:
                ###    bpy.context.object.active_material_index = 0 #select the top material
                ###    bpy.ops.object.material_slot_remove() #delete it

                bpy.ops.object.shade_flat()

                bpy.ops.object.select_all(action='DESELECT') #deselect all object

                #bpy.data.objects['Model'].select_set(True)
                #obj = bpy.context.window.scene.objects['Model']
                #bpy.context.view_layer.objects.active = obj

                hacermodelodeltiron()
                
                if objname == "lower":
                    bpy.context.scene.objects['lower'].select_set(state=True)
                    solounaparte()
                elif objname == "upper":
                    bpy.context.scene.objects['upper'].select_set(state=True)    
                    solounaparte()
                        

                bpy.ops.ed.undo_push()

def delete_all():
    for o in bpy.data.objects:
        bpy.data.objects.remove(o)
    
def set_mm():
    #for s in bpy.data.screens:
    #    for a in s.areas:
    #        if a.type == 'OUTLINER':
    #            a.spaces[0].display_mode = 'VISIBLE_LAYERS'
    bpy.context.scene.unit_settings.length_unit = 'MILLIMETERS'
    bpy.context.scene.unit_settings.scale_length = 0.001
    bpy.context.space_data.overlay.grid_scale = 0.001
    
def set_clipping_planes():
    bpy.context.space_data.lens = 50
    bpy.context.space_data.clip_start = 1
    bpy.context.space_data.clip_end = 1e+006
    
def orto():
    
    for obj in bpy.context.scene.objects:
        if obj.type == 'CAMERA':
            print(obj.data.type)
            obj.data.type = 'ORTHO'
            
def solounaparte():
     ### ME QUEDO CON LA PARTE MAS AMPLIA ###############
    bpy.ops.mesh.separate(type='LOOSE')

    #### list of mesh objects

    # Lista todos los mesh########################
    #mesh_objs = [o for o in bpy.context.scene.objects
    #                if o.type == 'MESH']

    # Lista de solo seleccionado
    mesh_objs = bpy.context.selected_objects

    ###############################################

    # dict with surface area of each object
    obj_areas = {o:sum([f.area for f in o.data.polygons])
                    for o in mesh_objs}

    # which is biggest
    big_obj = max(obj_areas, key=obj_areas.get)

    # select and delete not biggest
    [o.select_set(o is not big_obj) for o in mesh_objs]
    bpy.ops.object.delete(use_global=False, confirm=False)

def aceptar():

    bpy.ops.object.mode_set(mode="OBJECT") #Going back to Object mode

    bpy.ops.object.select_all(action='DESELECT') #deselect all object

    bpy.data.objects['cutter'].select_set(True)
    obj = bpy.context.window.scene.objects['cutter']
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.convert(target='MESH')

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.object.editmode_toggle()
    collection = bpy.data.collections.new(name="OriginalModels")
    scene = bpy.context.scene
    scene.collection.children.link(collection)

    collection = bpy.data.collections.new(name="OriginalModels")
    scene = bpy.context.scene
    scene.collection.children.link(collection)

    collection = bpy.data.collections.new(name="OriginalModels")
    scene = bpy.context.scene
    scene.collection.children.link(collection)

    bpy.ops.object.select_all(action='DESELECT') #deselect all object

    bpy.data.objects['target'].select_set(True)
    obj = bpy.context.window.scene.objects['target']
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.convert(target='MESH')

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.editmode_toggle()


    bpy.ops.object.select_all(action='DESELECT') #deselect all object



    bpy.data.objects['target'].select_set(True)
    obj = bpy.context.window.scene.objects['target']
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.editmode_toggle()


    obj = bpy.context.object

    vg = obj.vertex_groups.get('surfaces')

    if vg is not None:
        obj.vertex_groups.remove(vg)


    obj = bpy.context.object

    vg = obj.vertex_groups.get('Group')

    if vg is not None:
        obj.vertex_groups.remove(vg)
        
        
    bpy.ops.object.vertex_group_add()
    obj.vertex_groups[-1].name="surfaces"
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.vertex_group_assign()


    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=0.001)
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.delete_loose()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.vertex_group_set_active(group='surfaces')
    bpy.ops.object.vertex_group_select()
    bpy.ops.object.editmode_toggle()



    bpy.ops.object.select_all(action='DESELECT') #deselect all object


    bpy.data.objects['cutter'].select_set(True)
    obj = bpy.context.window.scene.objects['cutter']
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.delete(use_global=False)


    bpy.ops.object.select_all(action='DESELECT') #deselect all object



    bpy.data.objects['target'].select_set(True)
    obj = bpy.context.window.scene.objects['target']
    bpy.context.view_layer.objects.active = obj


    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.separate(type='LOOSE')
    bpy.ops.object.editmode_toggle()


    bpy.context.scene.transform_orientation_slots[0].type = "GLOBAL"

def exportarSTL():
    seleccionado = bpy.context.active_object
    if seleccionado == None:
        ErrorMsg_call("Seleccione modelo a exportar")
        #mostrarmensaje("Debe seleccionar un objeto")
    elif seleccionado != None:
            bpy.ops.export_mesh.stl('INVOKE_DEFAULT', use_selection=True)

def vistaTOP():
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            override = bpy.context.copy()
            override['area'] = area
            bpy.ops.view3d.view_axis(override, type='TOP')
            break

def createcoll(cole):
    collection = bpy.data.collections.new(name=cole)
    scene = bpy.context.scene
    scene.collection.children.link(collection)
    
def moveracoleccion(cole):
    C = bpy.context

    # List of object references
    objs = C.selected_objects

    # Set target collection to a known collection 
    coll_target = C.scene.collection.children.get(cole)

    # Set target collection based on the collection in context (selected) 
    #coll_target = C.collection

    # If target found and object list not empty
    if coll_target and objs:

        # Loop through all objects
        for ob in objs:
            # Loop through all collections the obj is linked to
            for coll in ob.users_collection:
                # Unlink the object
                coll.objects.unlink(ob)

            # Link each object to the target collection
            coll_target.objects.link(ob)


def reducemesh(r):
    seleccionado = bpy.context.active_object
    if seleccionado == None:
        ErrorMsg_call("No hay modelo seleccionado")
        #mostrarmensaje("Debe seleccionar un objeto")
    elif seleccionado != None:
        bpy.ops.object.editmode_toggle()
        mod = bpy.context.object.modifiers.new(name='Decimate', type='DECIMATE')
        mod.ratio = r
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.modifier_apply(modifier="Decimate")

def crearcoleccionsinoexiste(cole):
    import bpy
    collectionFound = False
    print("START **************")
    for myCol in bpy.data.collections:
        print(myCol.name)
        if myCol.name == cole:
            collectionFound = True
            print ("Collection found in scene")
            break
    if collectionFound == False:
        myCol = bpy.data.collections.new(cole)
        bpy.context.scene.collection.children.link(myCol) #Creates a new collection
        print("created")
    else:
        print("exists already")

####  CLASS O P E R A T O R

class ImportarSUP_CLASS(bpy.types.Operator, ImportHelper):
    """Batch Import Stl files and join them"""
    #bl_idname = "import_scene.custom_stls"
    bl_idname = "import_scene.s"
    bl_label = "Importar superior"
    bl_options = {'PRESET', 'UNDO'}
    
    # ImportHelper mixin class uses this
    filename_ext = ".stl"

    filter_glob: StringProperty(
            default="*.stl",
            options={'HIDDEN'},
            )

    # Selected files
    files: CollectionProperty(type=PropertyGroup)

    def execute(self, context):
        # Get the folder
        folder = os.path.dirname(self.filepath)
        obs = []
        # Iterate through the selected files
        for i in self.files:

            # Generate full path to file
            path_to_file = (os.path.join(folder, i.name))
            bpy.ops.import_mesh.stl(filepath=path_to_file)
            # Append Object(s) to the list
            obs.append(context.selected_objects[:])
            # Print the imported object reference
            print ("Imported object:", context.object)
        
        # Join the objects based on: 
        # https://blender.stackexchange.com/a/133024/
        ##### despues de esto poner el codigo cambiar nombre
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        obj = bpy.context.active_object
        obj.name = "upper"
        obj.data.name = "upper"
            
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.context.object.show_name = True
        bpy.ops.object.transforms_to_deltas(mode='ALL')

        # RESANAR
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.fill_holes(sides=30)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        #bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665, use_dissolve_boundaries=True)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()

        bpy.ops.mesh.delete(type='FACE')

        bpy.ops.mesh.select_non_manifold()

        bpy.ops.mesh.looptools_relax(input='selected', interpolation='linear', iterations='10', regular=True)

        bpy.ops.object.editmode_toggle()
        bpy.ops.ed.undo_push()

        #### ASIGNAR COLOR
        activeObject = bpy.context.active_object #Set active object to variable
        mat = bpy.data.materials['DENTUREBASE'] #set new material to variable
        activeObject.data.materials.append(mat) #add the material to the object

        ##### mover a coleccion
        moveracoleccion("OriginalModels")

        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.ed.undo_push()
        return {'FINISHED'}

class ImportarINF_CLASS(bpy.types.Operator, ImportHelper):
    """Batch Import Stl files and join them"""
    #bl_idname = "import_scene.custom_stls"
    bl_idname = "import_scene.i"
    bl_label = "Importar inferior"
    bl_options = {'PRESET', 'UNDO'}

    # ImportHelper mixin class uses this
    filename_ext = ".stl"

    filter_glob: StringProperty(
            default="*.stl",
            options={'HIDDEN'},
            )

    # Selected files
    files: CollectionProperty(type=PropertyGroup)

    def execute(self, context):
        import bpy

        # Get the folder
        folder = os.path.dirname(self.filepath)
        
        obs = []
        # Iterate through the selected files
        for i in self.files:

            # Generate full path to file
            path_to_file = (os.path.join(folder, i.name))
            bpy.ops.import_mesh.stl(filepath=path_to_file)
            # Append Object(s) to the list
            obs.append(context.selected_objects[:])
            # Print the imported object reference
            print ("Imported object:", context.object)
        
        # Join the objects based on: 
        # https://blender.stackexchange.com/a/133024/
        ##### despues de esto poner el codigo cambiar nombre
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
    
        obj = bpy.context.active_object
        obj.name = "lower"
        obj.data.name = "lower"
            
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()
        bpy.context.object.show_name = True
        bpy.ops.object.transforms_to_deltas(mode='ALL')

        # RESANAR
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=0.0001)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        bpy.ops.mesh.delete(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.fill_holes(sides=30)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()
        #bpy.ops.object.editmode_toggle()

        bpy.ops.mesh.dissolve_limited(angle_limit=0.0872665, use_dissolve_boundaries=True)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.mesh.select_all(action='DESELECT')

        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()

        bpy.ops.mesh.delete(type='FACE')

        bpy.ops.mesh.select_non_manifold()

        bpy.ops.mesh.looptools_relax(input='selected', interpolation='linear', iterations='10', regular=True)

        bpy.ops.object.editmode_toggle()
        bpy.ops.ed.undo_push()
        
        ##########################################################################
        ### ADD COLOR
        activeObject = bpy.context.active_object #Set active object to variable
        mat = bpy.data.materials['MODEL'] #set new material to variable
        activeObject.data.materials.append(mat) #add the material to the object

        ######### mover a coleccion
        moveracoleccion("OriginalModels")
        bpy.ops.object.select_all(action='DESELECT')

        bpy.ops.ed.undo_push()
        return {'FINISHED'}

font_info = {
    "font_id": 0,
    "handler": None,
}

class ErrorMsg():
    def __init__(self, context,message):
        for window in bpy.context.window_manager.windows:
            screen = window.screen
            
        for area in screen.areas:
              
              if area.type == 'VIEW_3D':
                for space in area.spaces:
                  
                  if space.type == 'VIEW_3D':
                   
                    for region in area.regions:
                      
                      if region.type == 'WINDOW':
                          width = region.width
                          height = region.height 
                          
        self.message = message                  
        x0 = width/4
        x100 = width*3/4

        ysup = height*3/10
        yinf = height*6/10
    ####Vertex positions for viriable bar########
        vertices = (
            (x0,ysup), (x0,yinf),
            (x100,yinf), (x100,ysup))

        indices = (
            (0, 1, 2), (2, 3, 0))
            
        #####text position######
        global xText, yText
        xText = width*2/4
        yText = (ysup+yinf)/2
              
        shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')

        batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
                   
        self.handle = bpy.types.SpaceView3D.draw_handler_add(
           self.draw_callback_px,(context,shader,batch),
           'WINDOW', 'POST_PIXEL')
           
        for area in bpy.context.window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()                 

    def draw_callback_px(self, context,shader,batch):
        shader.bind()
        glEnable(GL_BLEND)
        shader.uniform_float("color", (0.4, 0.8, 0.8, 0.5))
        batch.draw(shader)
        glDisable(GL_BLEND)
            # BLF drawing routine
        font_id = font_info["font_id"]
        xdimtext = blf.dimensions(font_id, self.message)[0]
        blf.position(font_id, xText-(xdimtext), yText, 0)
        blf.size(font_id, 24, 72)
        blf.draw(font_id, self.message)
        
                
    def remove_handle(self):
        bpy.types.SpaceView3D.draw_handler_remove(self.handle, 'WINDOW')
        
class ErrorMsg_call():
    def __init__(self, message):
        context = bpy.context
        dns = bpy.app.driver_namespace
        dns["error"] = ErrorMsg(context, message) 
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')
        time.sleep(1)
        error = dns.get("error")
        error.remove_handle()
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP')

#### PANELES 

class BIOTECH_PT_menumodel(bpy.types.Panel):
    bl_label="Diseño de modelos"
    bl_idname="BIOTECH_PT_menumodel"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="3dbiotech"
    bl_options={"DEFAULT_CLOSED"}
    def draw(self,context):
        layout=self.layout
        layout.label(text="Entrada de datos", icon="NEWFOLDER")
        row1=layout.row()
        layout=self.layout
        row1=layout.row()
        row1.operator("model.boton", text="Inferior", icon="TRIA_DOWN_BAR").action="importstlinf"
        row1.operator("model.boton", text="Superior", icon="TRIA_UP_BAR").action="importstlsup"
        layout.label(text="Visualización", icon="HIDE_OFF")
        row1=layout.row()
        row1.operator("model.boton", text="Reducir malla", icon="MOD_DECIM").action="reducemesh"
        row1.operator("model.boton", text="Crear modelo", icon="OUTLINER_OB_VOLUME").action="crearmodelo"
        layout.label(text="Salida de datos", icon="FOLDER_REDIRECT")
        row7=layout.row()
        row7.operator("model.boton", text="Exportar modelo", icon="OUTLINER_OB_VOLUME").action="exportarSTL"
        
#### AÑADIR OPERADORES A LOS PANELES

class BIOTECH_OT_botonesop(bpy.types.Operator):
    bl_label="MI_BOTON"
    bl_idname="model.boton"
    
    action:EnumProperty(
        items=[
            ('importstlinf','','Importar lower'),
            ('importstlsup','','Importar upper'),
            ('reducemesh','','Reducir malla'),
            ('crearmodelo','','Crear modelo'),
            ('exportarSTL','','exportarSTL')
            ]
    )
    def execute(self, context):
        if self.action == "importstlinf":
            bpy.ops.import_scene.i('INVOKE_DEFAULT')
            
        elif self.action == "importstlsup":
            bpy.ops.import_scene.s('INVOKE_DEFAULT')

        elif self.action == "reducemesh":
            reducemesh(float(0.9)) 

        elif self.action == "crearmodelo":
            crearmodelo()
            objetos = bpy.data.objects
            nombreobjetos = []
            for o in objetos:
                nombreobjetos.append(o.name)
            print (nombreobjetos)
            if "upper" in nombreobjetos:
                for obj in bpy.data.objects:
                    obj.select_set(False)
                bpy.data.objects["upper"].hide_set(False)
                bpy.data.objects["upper"].select_set(True)
                print ( "upper ")
                ob = bpy.context.scene.objects['upper']

                bpy.context.view_layer.objects.active = ob
                ob.select_set(True)
                bpy.data.objects["upper"].hide_set(False)
                bpy.data.objects["upper"].select_set(True)
                crearmodelo()

            if "lower" in nombreobjetos:
                for obj in bpy.data.objects:
                    obj.select_set(False)
                bpy.data.objects["lower"].hide_set(False)
                bpy.data.objects["lower"].select_set(True)
                print ( "lower ")
                ob = bpy.context.scene.objects['lower']

                bpy.context.view_layer.objects.active = ob
                ob.select_set(True)
                bpy.data.objects["lower"].hide_set(False)
                bpy.data.objects["lower"].select_set(True)
                crearmodelo()  

        elif self.action == "exportarSTL":
            exportarSTL()
 
        return {'FINISHED'}

####  HACER MODELO DEL TIRON

def hacermodelodeltiron():
    
    def dyno_on():
        context = bpy.context
        bpy.ops.object.mode_set(mode="SCULPT")
        if context.sculpt_object.use_dynamic_topology_sculpting == True:
            pass
        else:
           bpy.ops.sculpt.dynamic_topology_toggle() 
           
    def guess_model():
        print("ejecutando GUESS_MODEL()")   
        obj = bpy.context.object # edit: now gets the currently active object 
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_non_manifold()

        bpy.ops.object.mode_set(mode="OBJECT")

        verts = obj.data.vertices
        sel_verts = [v for v in verts if v.select]#Vertices seleccionados
        if sel_verts == []:
            obj.name = "_base"
            upper = 1
        else:
            non_sel_verts = [v for v in verts if not v.select]
            # get the z-coordinates from each vertex and the maximum and minimum
            z_coords_sel = [v.co[2] for v in sel_verts]
            z_coords_non_sel = [v.co[2] for v in non_sel_verts]

            mean_z_sel = statistics.mean(z_coords_sel)
            mean_z_non_sel = statistics.mean(z_coords_non_sel)


            #print(mean_z_sel)
            #print(mean_z_non_sel)

            if mean_z_sel > mean_z_non_sel:
                upper = 2
                #obj.name = "upper"
            else:
                upper = 3
                #obj.name = "lower"
                
        return upper

    def cleanup():
        print("ejecutando CleanUP")
        verts_sel_O = 0
        verts_sel = 1 
        while verts_sel != verts_sel_O: 
            ob = bpy.context.object
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_non_manifold() 
            bpy.ops.object.mode_set(mode="OBJECT")
            verts_sel_O = len([v for v in ob.data.vertices if v.select])
            verts_sel = 0           
            me = bpy.context.object.data
            bm = bmesh.new()   # create an empty BMesh
            bm.from_mesh(me)   # fill it in from a Mesh
            # Erase single vertices (not forming faces)
            for v in bm.verts:
                if not v.link_edges:
                    v.select = True
                    bm.verts.remove(v)
            # Erase edges not forming faces
            for ed in bm.edges:
                if len(ed.link_faces) == 0:
                    for v in ed.verts:
                        if len(v.link_faces) == 0:
                            v.select = True
                            bm.verts.remove(v)
            # Erase trienagles with less than 2 neighbours
            for v in bm.verts:
                if len(v.link_edges) == 2:
                    v.select = True
                    bm.verts.remove(v)

            bm.to_mesh(me)
            me.update()
            bm.free()
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_non_manifold() 
            bpy.ops.object.mode_set(mode="OBJECT")
            verts_sel = len([v for v in ob.data.vertices if v.select])
            
    def modelbase():
        print("ejecutando MODELBASE()")
        upper = guess_model()
        print(upper) # añado para verlo en consola
        if upper == 1:
            #ErrorMsg_call("Este modelo ya esta cerrado")
            print("Este modelo ya esta cerrado")
                     
            return {"CANCELLED"}  
        else:
            cleanup()
            if upper == 2:           
                ob = bpy.context.object
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_non_manifold() 
                bpy.ops.object.mode_set(mode="OBJECT")   
                v_all = np.zeros(len(ob.data.vertices)*3, dtype=np.float32)
                ob.data.vertices.foreach_get('co', v_all)
                v_selected = np.zeros(len(ob.data.vertices), dtype=np.bool)
                ob.data.vertices.foreach_get('select', v_selected)
                v_all.shape = (v_all.size //3,3)
                z_co = v_all[:,2]
                max_z = np.amax(z_co[v_selected])
                z_co[v_selected] = max_z
                ob.data.vertices.foreach_set('co', v_all.ravel())
                ob.data.update()
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.edge_face_add()
                bpy.ops.mesh.select_more()
                bpy.ops.mesh.hide(unselected=True)
                dyno_on()
                bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
                bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 2
                bpy.ops.sculpt.detail_flood_fill()
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.vertices_smooth(factor=1, repeat=5)
                bpy.ops.mesh.reveal()
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_non_manifold() 
                bpy.ops.mesh.dissolve_mode(use_verts=True)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode="OBJECT")
                cleanup()
                
            else:
                ob = bpy.context.object
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_non_manifold() 
                bpy.ops.object.mode_set(mode="OBJECT")   
                v_all = np.zeros(len(ob.data.vertices)*3, dtype=np.float32)
                ob.data.vertices.foreach_get('co', v_all)
                v_selected = np.zeros(len(ob.data.vertices), dtype=np.bool)
                ob.data.vertices.foreach_get('select', v_selected)
                v_all.shape = (v_all.size //3,3)
                z_co = v_all[:,2]
                min_z = np.amin(z_co[v_selected])
                z_co[v_selected] = min_z
                ob.data.vertices.foreach_set('co', v_all.ravel())
                ob.data.update()
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.edge_face_add()
                bpy.ops.mesh.select_more()
                bpy.ops.mesh.hide(unselected=True)
                dyno_on()
                bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
                bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 2
                bpy.ops.sculpt.detail_flood_fill()
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.mesh.select_all(action='SELECT')
                bpy.ops.mesh.vertices_smooth(factor=1, repeat=5)
                bpy.ops.mesh.reveal()
                bpy.ops.mesh.select_all(action='DESELECT')        
                bpy.ops.mesh.select_non_manifold() 
                bpy.ops.mesh.dissolve_mode(use_verts=True)
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode="OBJECT")
                cleanup()

    def relief():
        print("ejecutando RELIEF")
        ob1 = bpy.context.object
        bpy.ops.object.duplicate_move()
        ob2 = bpy.context.object
        bpy.context.object.data.remesh_voxel_size = 0.7
        bpy.context.object.data.use_remesh_preserve_volume = True
        bpy.context.object.data.use_remesh_fix_poles = True
        #bpy.context.object.data.use_remesh_smooth_normals = True
        bpy.ops.object.voxel_remesh()
        bpy.ops.object.modifier_add(type='SMOOTH')
        obsmooth = ob2.modifiers[0].name
        bpy.context.object.modifiers[obsmooth].factor = 1
        bpy.context.object.modifiers[obsmooth].iterations = 5
        bpy.ops.object.modifier_apply(modifier=obsmooth)
        ob1.select_set(True)
        bpy.ops.object.join()
        bpy.context.object.data.remesh_voxel_size = 0.2
        bpy.context.object.data.use_remesh_preserve_volume = True
        bpy.context.object.data.use_remesh_fix_poles = True
        #bpy.context.object.data.use_remesh_smooth_normals = True
        bpy.ops.object.voxel_remesh()
        ob = bpy.context.object
        ob.name += "_relief"
        
    modelbase()