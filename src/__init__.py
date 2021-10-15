bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (2, 93, 2),
    "version" : (0, 0, 3),
    "location" : "Edit Armature > Add, Edit Armature > Names, Object > Clean Up",
    "warning" : "",
    "category" : "Armature, Object"
}

import bpy
from .edit_add import BoneJuice_SurfacePlacer
from .edit_ops import *
from .object_ops import *
from .registrator import registerClass, unregisterClass

def register():
    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names])
    registerClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names])
    unregisterClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])

if __name__ == "__main__":
    register()