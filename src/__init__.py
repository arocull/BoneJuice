bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 10),
    "location" : "Edit Armature, Pose Mode, Object Mode",
    "warning" : "",
    "doc_url": "https://github.com/arocull/BoneJuice",
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
from .luchadores import registerLuchadores, unregisterLuchadores

## PREFERENCES
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

class BoneJuiceGlobals:
    luchadoresRegistered: bool = False

class BoneJuicePreferences(AddonPreferences):
    bl_idname: str = __name__

    def toggleLuchadores(self, context):
        print(self.enableLuchadores)
        print(BoneJuiceGlobals.luchadoresRegistered)
        if self.enableLuchadores and (not BoneJuiceGlobals.luchadoresRegistered):
            registerLuchadoresHelper()
        elif (not self.enableLuchadores) and BoneJuiceGlobals.luchadoresRegistered:
            unregisterLuchadoresHelper()

    enableLuchadores: BoolProperty(
        name="Enable Luchadores Workflow",
        description="If true, enables tools for annotating and exporting to the Luchadores engine.",
        default=False,
        update=toggleLuchadores
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BoneJuice Preferences")
        layout.prop(self, "enableLuchadores")

## REGISTER
def registerLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = True
    registerLuchadores()

def unregisterLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = False
    unregisterLuchadores()

def register():
    bpy.utils.register_class(BoneJuicePreferences)

    registerClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_AddLeafBones, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_AddBoneCircle, [bpy.types.TOPBAR_MT_edit_armature_add])
    registerClass(BoneJuice_SelectBoneChainEnds, [bpy.types.VIEW3D_MT_select_edit_armature])
    registerClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    registerClass(BoneJuice_ConnectBones, [bpy.types.VIEW3D_MT_edit_armature])
    registerClass(BoneJuice_SetBoneLength, [bpy.types.VIEW3D_MT_edit_armature])
    registerClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    registerClass(BoneJuice_MergeVertexGroups, [bpy.types.VIEW3D_MT_paint_weight, bpy.types.VIEW3D_MT_object_apply])
    registerClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])
    registerClass(BoneJuice_FlipIKLimits, [bpy.types.VIEW3D_MT_pose])
    registerClass(BoneJuice_BatchRenderActions, [bpy.types.TOPBAR_MT_render])

    if getPreferences(bpy.context).enableLuchadores:
        registerLuchadoresHelper()

def unregister():
    unregisterClass(BoneJuice_SurfacePlacer, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_AddLeafBones, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_AddBoneCircle, [bpy.types.TOPBAR_MT_edit_armature_add])
    unregisterClass(BoneJuice_SelectBoneChainEnds, [bpy.types.VIEW3D_MT_select_edit_armature])
    unregisterClass(BoneJuice_MarkSide, [bpy.types.VIEW3D_MT_edit_armature_names, bpy.types.VIEW3D_MT_pose_names], [BoneJuice_MarkSide.button_edit, BoneJuice_MarkSide.button_pose])
    unregisterClass(BoneJuice_ConnectBones, [bpy.types.VIEW3D_MT_edit_armature])
    unregisterClass(BoneJuice_SetBoneLength, [bpy.types.VIEW3D_MT_edit_armature])
    unregisterClass(BoneJuice_CleanAndCombine, [bpy.types.VIEW3D_MT_object_cleanup])
    unregisterClass(BoneJuice_MergeVertexGroups, [bpy.types.VIEW3D_MT_paint_weight, bpy.types.VIEW3D_MT_object_apply])
    unregisterClass(BoneJuice_CurlBones, [bpy.types.VIEW3D_MT_pose])
    unregisterClass(BoneJuice_FlipIKLimits, [bpy.types.VIEW3D_MT_pose])
    unregisterClass(BoneJuice_BatchRenderActions, [bpy.types.TOPBAR_MT_render])

    if BoneJuiceGlobals.luchadoresRegistered:
        unregisterLuchadoresHelper()

    bpy.utils.unregister_class(BoneJuicePreferences)

if __name__ == "__main__":
    register()