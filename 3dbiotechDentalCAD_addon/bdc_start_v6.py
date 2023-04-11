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

from .bdc_tools import *

##### ENLACE FUNCION-BOTON

def fb_start01():
    hideact()

def fb_start02():
    showact()

def fb_start03():
    undo()

def fb_start04():
    redo()
   
def fb_start05():
    startanimation()
        
def fb_start06():
    endanimation()

def fb_start07():
    playanimation()

def fb_start08():
    sculptobject()

def fb_start09():
    exitmode()

def fb_start10():
    reinicio()

def fb_start11():
    bpy.ops.object.delete()

def fb_start12():
    showhideupper()

def fb_start13():
    showhidelower()

def fb_start14():
    showhidesplint()

def fb_start15():
    flattenobject()

def fb_start16():
    smoothobject()

def fb_start17():
    Inflateobject()

def fb_start21():
    a = 'DENTURETEETH'
    asignarcolor(a)

def fb_start22():
    a = 'DENTUREBASE'
    asignarcolor(a)

def fb_start23():
    a = 'MODEL'
    asignarcolor(a)

def fb_start24():
    a = 'DRAFT'
    asignarcolor(a)

def fb_start25():
    a = 'BIOMED'
    asignarcolor(a)

def fb_start26():
    a = 'CASTABLE'
    asignarcolor(a)

def fb_start27():
    a = 'IBT'
    asignarcolor(a)

class BIOTECH_PT_start(bpy.types.Panel):
    bl_label="BIOTECHDENTALCAD"
    bl_idname="BIOTECH_PT_start"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_category="3dbiotech"
    #bl_options={"DEFAULT_CLOSED"}
    def draw(self,context):
        layout = self.layout
        view = context.space_data
        col = layout.column(align=True)
        col.operator("start.boton", text="Comenzar", icon="PLAY").action="boton10"
        col.label(text="Herramientas:", icon="MODIFIER")
        row = col.row()
        row.operator("start.boton", text="Ocultar", icon="HIDE_ON").action="boton01"
        row.operator("start.boton", text="Mostrar", icon="HIDE_OFF").action="boton02"
        row = col.row()
        row.operator("start.boton", text="Deshacer", icon="LOOP_BACK").action="boton03"
        row.operator("start.boton", text="Rehacer", icon="LOOP_FORWARDS").action="boton04"
        row = col.row()
        row.operator("start.boton", text="Inicio", icon="REW").action="boton05"
        row.operator("start.boton", text="Fin", icon="FF").action="boton06"
        row.operator("start.boton", text="Reproducir", icon="PLAY").action="boton07"
        layout = self.layout
        view = context.space_data
        col = layout.column(align=True)
        col.label(text="Modelo:", icon="VIEW3D")
        row = col.row()
        row.operator("start.boton", text="Superior", icon="TRIA_UP").action="boton12"
        row.operator("start.boton", text="Inferior", icon="TRIA_DOWN").action="boton13"
        row.operator("start.boton", text="Ferula", icon="MOD_THICKNESS").action="boton14"

class BIOTECH_PT_startsculpt(bpy.types.Panel):
    bl_label="Esculpir"
    bl_idname="BIOTECH_PT_startsculpt"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_options={"DEFAULT_CLOSED"}
    bl_parent_id="BIOTECH_PT_start"
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        col = layout.column(align=True)
        row = col.row()
        row.operator("start.boton", text="Simplificar", icon="BRUSH_SMOOTH").action="boton08"
        row.operator("start.boton", text="Alisar", icon="BRUSH_FLATTEN").action="boton15"
        row.operator("start.boton", text="Suavizar", icon="BRUSH_SMOOTH").action="boton16"
        row = col.row()
        row.operator("start.boton", text="Inflar", icon="BRUSH_INFLATE").action="boton17"
        row.operator("start.boton", text="Salir modificar", icon="EVENT_ESC").action="boton09"
        row.operator("start.boton", text="Eliminar", icon="TRASH").action="boton11"

class BIOTECH_PT_startview(bpy.types.Panel):
    bl_label="Vistas"
    bl_idname="BIOTECH_PT_startview"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_options={"DEFAULT_CLOSED"}
    bl_parent_id="BIOTECH_PT_start"
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        col = layout.column(align=True)
        col.label(text="Alinear vista desde:", icon="VIEW3D")
        row = col.row()
        row.operator("view3d.view_axis", text="Frontal").type = 'FRONT'
        row.operator("view3d.view_axis", text="Posterior").type = 'BACK'
        row = col.row()
        row.operator("view3d.view_axis", text="Izquierda").type = 'LEFT'
        row.operator("view3d.view_axis", text="Derecha").type = 'RIGHT'
        row = col.row()
        row.operator("view3d.view_axis", text="Superior").type = 'TOP'
        row.operator("view3d.view_axis", text="Inferior").type = 'BOTTOM'
        col = layout.column(align=True)
        col.label(text="Bloquear vista de objeto:", icon="LOCKED")
        col.prop(view, "lock_object", text="")
        col.operator("view3d.view_selected", text="View to Selected")
        col = layout.column(align=True)
        col.label(text="Cursor:", icon='PIVOT_CURSOR')
        row = col.row(align=True)
        row.operator("view3d.snap_cursor_to_center", text="World Origin")
        row.operator("view3d.view_center_cursor", text="View")
        col.operator("view3d.snap_cursor_to_selected", text="Cursor to Selected")

class BIOTECH_PT_materialpanel(bpy.types.Panel):
    bl_label="Resinas Formlabs"
    bl_idname="BIOTECH_PT_materialpanel"
    bl_space_type="VIEW_3D"
    bl_region_type="UI"
    bl_options={"DEFAULT_CLOSED"}
    bl_parent_id="BIOTECH_PT_start"
    def draw(self, context):
        layout = self.layout
        view = context.space_data
        col = layout.column(align=True)
        row = col.row()
        row.operator("start.boton", text="DENTURE BASE", icon="COLLECTION_COLOR_01").action="boton22"
        row.operator("start.boton", text="MODEL", icon="COLLECTION_COLOR_02").action="boton23"
        row.operator("start.boton", text="DENTURE TEETH", icon="COLLECTION_COLOR_03").action="boton21"
        row = col.row()
        row.operator("start.boton", text="DRAFT", icon="SEQUENCE_COLOR_09").action="boton24"
        row.operator("start.boton", text="CASTABLE", icon="COLLECTION_COLOR_06").action="boton26"
        row.operator("start.boton", text="IBT", icon="COLORSET_09_VEC").action="boton27"
        row = col.row()
        row.operator("start.boton", text="BIOMED", icon="COLLECTION_COLOR_05").action="boton25"

##### AÑADIR OPERADORES A LOS PANELES

class BIOTECH_OT_start(bpy.types.Operator):
    bl_label="Inicio"
    bl_idname="start.boton"
    bl_description ="Basicos de 3dbiotech"
    bl_options = {'REGISTER', 'UNDO'}
    
    action:EnumProperty(
        items=[
            ('boton01','','ACCION 02'),
            ('boton02','','ACCION 02'),
            ('boton03','','ACCION 03'),
            ('boton04','','ACCION 04'),
            ('boton05','','ACCION 05'),
            ('boton06','','ACCION 06'),
            ('boton07','','ACCION 07'),
            ('boton08','','ACCION 08'),
            ('boton09','','ACCION 09'),
            ('boton10','','ACCION 10'),
            ('boton11','','ACCION 11'),
            ('boton12','','ACCION 02'),
            ('boton13','','ACCION 03'),
            ('boton14','','ACCION 04'),
            ('boton15','','ACCION 05'),
            ('boton16','','ACCION 06'),
            ('boton17','','ACCION 07'),
            ('boton18','','ACCION 08'),
            ('boton19','','ACCION 09'),
            ('boton20','','ACCION 10'),
            ('boton21','','ACCION 11'),
            ('boton22','','ACCION 02'),
            ('boton23','','ACCION 03'),
            ('boton24','','ACCION 04'),
            ('boton25','','ACCION 05'),
            ('boton26','','ACCION 06'),
            ('boton27','','ACCION 07'),
            ('boton28','','ACCION 08'),
            ('boton29','','ACCION 09'),
            ('boton30','','ACCION 10')
            ]
    )

##### BOTONES UNIVERSALES

    def execute(self, context):
        if self.action == "boton01":
            fb_start01()
        elif self.action == "boton02":
            fb_start02()
        elif self.action == "boton03":
            fb_start03()
        elif self.action == "boton04":
            fb_start04()
        elif self.action == "boton05":
            fb_start05()
        elif self.action == "boton06":
            fb_start06()
        elif self.action == "boton07":
            fb_start07()         
        elif self.action == "boton08":
            fb_start08()
        elif self.action == "boton09":
            fb_start09()
        elif self.action == "boton10":
            fb_start10()
        elif self.action == "boton11":
            fb_start11()
        elif self.action == "boton12":
            fb_start12()
        elif self.action == "boton13":
            fb_start13()
        elif self.action == "boton14":
            fb_start14()
        elif self.action == "boton15":
            fb_start15()
        elif self.action == "boton16":
            fb_start16()
        elif self.action == "boton17":
            fb_start17()         
        elif self.action == "boton18":
            fb_start18()
        elif self.action == "boton19":
            fb_start19()
        elif self.action == "boton20":
            fb_start20()
        elif self.action == "boton21":
            fb_start21()
        elif self.action == "boton22":
            fb_start22()  
        elif self.action == "boton23":
            fb_start23()
        elif self.action == "boton24":
            fb_start24()
        elif self.action == "boton25":
            fb_start25()
        elif self.action == "boton26":
            fb_start26()
        elif self.action == "boton27":
            fb_start27()         
        elif self.action == "boton28":
            fb_start28()
        elif self.action == "boton29":
            fb_start29()
        elif self.action == "boton30":
            fb_start30()

        return {'FINISHED'}