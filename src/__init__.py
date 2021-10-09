bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (2, 93, 0),
    "version" : (0, 0, 2),
    "location" : "Edit Armature",
    "warning" : "",
    "category" : "Armature"
}

import bpy
from .edit_add import BoneJuice_SurfacePlacer
from .edit_ops import *
from .registrator import registerClass, unregisterClass

def register():
    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names])

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names])

if __name__ == "__main__":
    register()