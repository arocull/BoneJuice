bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (2, 93, 0),
    "version" : (0, 0, 1),
    "location" : "3D View",
    "warning" : "Somewhat experimental",
    "category" : "3D View"
}

import bpy
from .bones import BoneJuice_SurfacePlacer
from .registrator import registerClass, unregisterClass

def register():
    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])

if __name__ == "__main__":
    register()