from math import pi
import bpy
from bpy.types import PoseBone, Operator
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty, StringProperty
from typing import List
from .boneprops import LUCHADORES_BONE_PROPERTIES, copy_bpy_property, initialize_bone_props

class BoneJuice_Luchadores_AnnotateBones(Operator):
    """Annotates the selected bones for the Luchadores engine."""
    bl_idname = "animation.bj_luchadores_annotatebones"
    bl_label = "Luchadores Bone Annotation"
    bl_description = "Annotates the selected bones for the Luchadores engine"
    bl_options = {'REGISTER', 'UNDO'}

    def button(self, context):
        self.layout.operator(
            BoneJuice_Luchadores_AnnotateBones.bl_idname,
            text=BoneJuice_Luchadores_AnnotateBones.bl_label,
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_Luchadores_AnnotateBones.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def annotateBone(self, bone: PoseBone):
        initialize_bone_props(bone)

    def execute(self, context: bpy.types.Context):
        bones: List[PoseBone] = bpy.context.selected_pose_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            self.annotateBone(bone)
        
        return {'FINISHED'}