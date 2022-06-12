bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (3, 0, 0),
    "version" : (0, 0, 7),
    "location" : "Edit Armature, Pose Mode, Object Mode",
    "warning" : "",
    "category" : "Armature, Object"
}

import bpy
from .armature.edit_add import *
from .armature.edit_ops import *
from .mesh.clean_and_combine import *
from .mesh.merge_vertex_groups import *
from .armature.pose_ops import *
from .render.batch import *
from .registrator import registerClass, unregisterClass



def register():
    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_AddLeafBones, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_SelectBoneChainEnds, [bpy.types.VIEW3D_MT_select_edit_armature])
    registerClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    registerClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    registerClass(BoneJuice_MergeVertexGroups, [bpy.types.VIEW3D_MT_paint_weight, bpy.types.VIEW3D_MT_object_apply])
    registerClass(BoneJuice_BulkSetRotationMode, [bpy.types.VIEW3D_MT_pose])
    registerClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])
    registerClass(BoneJuice_BatchRenderActions, [bpy.types.TOPBAR_MT_render])

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_AddLeafBones, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_SelectBoneChainEnds, [bpy.types.VIEW3D_MT_select_edit_armature])
    unregisterClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    unregisterClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    unregisterClass(BoneJuice_MergeVertexGroups, [bpy.types.VIEW3D_MT_paint_weight, bpy.types.VIEW3D_MT_object_apply])
    unregisterClass(BoneJuice_BulkSetRotationMode, [bpy.types.VIEW3D_MT_pose])
    unregisterClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])
    unregisterClass(BoneJuice_BatchRenderActions, [bpy.types.TOPBAR_MT_render])

if __name__ == "__main__":
    register()