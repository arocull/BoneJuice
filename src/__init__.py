bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 5),
    "location" : "Edit Armature > Add, Edit Armature > Names, Object > Clean Up",
    "warning" : "",
    "category" : "Armature, Object"
}

import bpy
from .edit_add import BoneJuice_SurfacePlacer
from .edit_ops import *
from .object_ops import *
from .pose_ops import *
from .registrator import registerClass, unregisterClass

def register():
    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    registerClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    registerClass(BoneJuice_BulkSetRotationMode, [bpy.types.VIEW3D_MT_pose])
    registerClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    unregisterClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    unregisterClass(BoneJuice_BulkSetRotationMode, [bpy.types.VIEW3D_MT_pose])
    unregisterClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])

if __name__ == "__main__":
    register()