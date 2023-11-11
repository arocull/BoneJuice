import bpy
from bpy.types import Menu, Operator
from .armature.edit_ops import *
from .armature.spline_from_curve import *
from .mesh.merge_vertex_groups import *
from .armature.reduce_rig import *
from .armature.transer_animations import *
from .globals import BoneJuiceGlobals

class BoneJuiceMenu_EditArmature(bpy.types.Menu):
    bl_label = "BoneJuice"
    bl_idname = "VIEW3D_MT_edit_armature_bonejuice"

    def draw(self, context: bpy.types.Context):
        layout = self.layout

        # Draw settings that don't really fit in a category
        layout.operator(BoneJuice_SetBoneLength.bl_idname, text=BoneJuice_SetBoneLength.bl_label)
        layout.operator(BoneJuice_ConnectBones.bl_idname, text=BoneJuice_ConnectBones.bl_label)
        layout.operator(BoneJuice_AutoParentBones.bl_idname, text=BoneJuice_AutoParentBones.bl_label)
        layout.operator(BoneJuice_ReduceRig.bl_idname, text=BoneJuice_ReduceRig.bl_label)

        # Draw experimental settings
        if BoneJuiceGlobals.experimentalRegistered:
            layout.separator()
            # layout.operator(BoneJuice_TransferAnimations.bl_idname, BoneJuice_TransferAnimations.bl_label)

def BoneJuiceMenu_EditArmatureDraw(self, context):
    self.layout.separator()
    self.layout.menu(BoneJuiceMenu_EditArmature.bl_idname)
