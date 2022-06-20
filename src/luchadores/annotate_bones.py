from math import pi
import bpy
from bpy.types import PoseBone, Operator
from bpy.props import BoolProperty, FloatVectorProperty, StringProperty
from typing import List

class BoneJuice_Luchadores_AnnotateBones(Operator):
    """Annotates the selected bones for the Luchadores engine."""
    bl_idname = "animation.bj_luchadores_annotatebones"
    bl_label = "Luchadores Bone Annotation"
    bl_description = "Annotates the selected bones for the Luchadores engine"
    bl_options = {'REGISTER', 'UNDO'}

    angles: FloatVectorProperty(
        name = 'Euler Angles',
        description = 'Angle on each axis to transform the bones by',
        subtype= 'EULER',
        step = 10,
        soft_min = -2 * pi,
        soft_max = 2 * pi
    )
    useTotal: BoolProperty(
        name = 'Divide by Total',
        description = 'If true, offset angles are divided by the total number of selected bones.',
        default = True
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_Luchadores_AnnotateBones.bl_idname,
            text="Luchadores Bone Annotation",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.animation.bj_curl_bones", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def annotateBone(self, bone: PoseBone):
        if not bone["color"]:
            bone["color"] = StringProperty(
                name="color",
                description="Color to draw for this bone",
                default="#000000",
            )

    def execute(self, context: bpy.types.Context):
        bones: List[PoseBone] = bpy.context.selected_pose_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            self.annotateBone(bone)
        
        return {'FINISHED'}