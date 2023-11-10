import bpy
from .armature.edit_add import *
from .armature.edit_ops import *
from .mesh.clean_and_combine import *
from .mesh.merge_vertex_groups import *
from .armature.pose_ops import *
from .render.batch import *
from .armature.reduce_rig import *
from .armature.transer_animations import *
from .armature.spline_from_curve import *
from .menus import *

BINDINGS: list = [
    (BoneJuice_AddLeafBones,        [bpy.types.TOPBAR_MT_edit_armature_add],    []),
    (BoneJuice_AddBoneCircle,       [bpy.types.TOPBAR_MT_edit_armature_add],    []),
    (BoneJuice_SurfacePlacer,       [bpy.types.TOPBAR_MT_edit_armature_add],    []),
    (BoneJuice_SplineFromCurve,     [bpy.types.TOPBAR_MT_edit_armature_add],    []),
    (BoneJuice_SelectBoneChainEnds, [bpy.types.VIEW3D_MT_select_edit_armature], []),
    (BoneJuice_MarkSide,            [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose]),
    (BoneJuice_AutoParentBones,     [bpy.types.VIEW3D_MT_edit_armature_parent], []),
    (BoneJuice_ConnectBones,        [],        []),
    (BoneJuice_SetBoneLength,       [],        []),
    (BoneJuice_ReduceRig,           [bpy.types.VIEW3D_MT_object_cleanup],        []),
    (BoneJuice_CleanAndCombine,     [bpy.types.VIEW3D_MT_object_cleanup],       []),
    (BoneJuice_MergeVertexGroups,   [bpy.types.VIEW3D_MT_paint_weight, bpy.types.VIEW3D_MT_object_apply], []),
    (BoneJuice_CurlBones,           [bpy.types.VIEW3D_MT_pose],                 []),
    (BoneJuice_FlipIKLimits,        [bpy.types.VIEW3D_MT_pose],                 []),
]

MENUBINDINGS: list = [
    (BoneJuiceMenu_EditArmature,    BoneJuiceMenu_EditArmatureDraw,             [bpy.types.VIEW3D_MT_edit_armature]),
]

BINDINGS_EXPERIMENTAL: list = [
    (BoneJuice_BatchRenderActions,  [bpy.types.TOPBAR_MT_render],               []),
    (BoneJuice_TransferAnimations,  [bpy.types.VIEW3D_MT_object_animation],     []),
]
