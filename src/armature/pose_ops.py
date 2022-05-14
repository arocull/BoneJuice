from math import pi
import bpy
from bpy.types import PoseBone, Operator
from bpy.props import BoolProperty, FloatVectorProperty
from typing import List

class BoneJuice_CurlBones(Operator):
    """Curls the selected bones."""
    bl_idname = "animation.bj_curl_bones"
    bl_label = "Curl Bones"
    bl_description = "Sets the rotation mode of the selected pose bones. Only works on bones with a Euler rotation mode."
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
            BoneJuice_CurlBones.bl_idname,
            text="Curl Bones",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.animation.bj_curl_bones", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.types.Context):
        bones: List[PoseBone] = bpy.context.selected_pose_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        totalLen = float(len(bones))
        for bone in bones:
            newAngles = bone.rotation_euler
            for i in range(0, 3):
                if self.useTotal:
                    newAngles[i] += self.angles[i] / totalLen
                else:
                    newAngles[i] += self.angles[i]

            bone.rotation_euler = newAngles
        
        return {'FINISHED'}