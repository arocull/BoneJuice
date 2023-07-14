from math import pi
from re import I
import bpy
from bpy.types import PoseBone, Operator
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty, StringProperty
from typing import List
from .boneprops import LUCHADORESBONEPROPS

class BoneJuice_Luchadores_CopyBoneProps(Operator):
    """Annotates the selected bones for the Luchadores engine."""
    bl_idname = "bj.luchadores.copyboneprops"
    bl_label = "Copy Bone Properties (Luchadores)"
    bl_description = "Annotates the selected bones for the Luchadores engine"
    bl_options = {'REGISTER', 'UNDO'}

    def button(self, context):
        self.layout.operator(
            BoneJuice_Luchadores_CopyBoneProps.bl_idname,
            text=BoneJuice_Luchadores_CopyBoneProps.bl_label,
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_Luchadores_CopyBoneProps.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.context):
        bones: List[PoseBone] = context.selected_pose_bones
        activeBone: PoseBone = context.active_pose_bone
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            if bone == activeBone:
                continue
            
            for item in LUCHADORESBONEPROPS:
                if hasattr(activeBone, item):
                    bone[item] = activeBone[item]
        
        return {'FINISHED'}