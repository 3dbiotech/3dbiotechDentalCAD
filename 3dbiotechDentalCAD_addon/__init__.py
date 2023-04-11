bl_info ={
    "name":"3DBiotechDentalCAD",
    "autor":"Juan Chups y Robert Brun",
    "version":(0,8),
    "blender":(3,5,0),
    "location":"View3d",
    "description":"Demo para e-learning. Addon con herramientas desarrolladas a medida para el tratamiento de modelos dentales.",
    "warning":"¡Atención modulo en desarrollo!",
    "wiki_url":"https://github.com/orgs/3dbiotech/repositories",
    "category":"Dental"
}

import bpy, sys, os, bmesh, statistics, gpu, time, importlib, blf, time
import numpy as np

from bpy_extras.io_utils import ImportHelper
from bpy.types import (Operator, PropertyGroup, WindowManager)
from bpy.props import (StringProperty, CollectionProperty, EnumProperty, FloatProperty)
from gpu_extras.batch import batch_for_shader

from mathutils import Vector
from bgl import *
from numpy import True_



from .bdc_start_v6 import *
from .bdc_model_v7 import *



classesBDCstart = [
    BIOTECH_OT_start,
    BIOTECH_PT_start,
    BIOTECH_PT_startview,
    BIOTECH_PT_startsculpt,
    BIOTECH_PT_materialpanel
    ]

classesBDCmodel = [
    BIOTECH_PT_menumodel,
    BIOTECH_OT_botonesop,
    ImportarSUP_CLASS,
    ImportarINF_CLASS,
    ]

def register():
    for cls in classesBDCstart:
        bpy.utils.register_class(cls)
    for cls in classesBDCmodel:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classesBDCstart:
        bpy.utils.unregister_class(cls)
    for cls in classesBDCmodel:
        bpy.utils.unregister_class(cls)

if __name__=="__main__":
    register()