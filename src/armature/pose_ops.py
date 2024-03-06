from math import pi
import bpy
from bpy.types import PoseBone, Operator
from bpy.props import BoolProperty, FloatVectorProperty, EnumProperty
from typing import List

class BoneJuice_CurlBones(Operator):
    """Curls the selected bones."""
    bl_idname = "bj.curl_bones"
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
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops.bj.curl_bones", "blob/master/docs/examples/curl_bones.md"),
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

class BoneJuice_FlipIKLimits(Operator):
    """Swaps the minimum and maximum values of IK limits of given bones."""
    bl_idname = "bj.flip_ik_limits"
    bl_label = "Flip IK Limits"
    bl_description = "Swaps the minimum and maximum values of IK limits of selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    axis: EnumProperty(
        name = 'Axis',
        description = 'Which axis to flip IK ranges on',
        items = [
            ('x', 'X', 'Flips the X axis IK limits'),
            ('y', 'Y', 'Flips the Y axis IK limits'),
            ('z', 'Z', 'Flips the Z axis IK limits'),
        ],
        default = 'z',
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_FlipIKLimits.bl_idname,
            text="Flip IK Limits",
            icon='MOD_MIRROR')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops.bj.flip_ik_limits", "blob/master/docs/examples/flip_ik_limits.md"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.types.Context):
        bones: List[PoseBone] = bpy.context.selected_pose_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            swap: float = 0
            
            if self.axis == 'x':
                swap = bone.ik_max_x
                bone.ik_max_x = bone.ik_min_x * (-1)
                bone.ik_min_x = swap * (-1)
            if self.axis == 'y':
                swap = bone.ik_max_y
                bone.ik_max_y = bone.ik_min_y * (-1)
                bone.ik_min_y = swap * (-1)
            else:
                swap = bone.ik_max_z
                bone.ik_max_z = bone.ik_min_z * (-1)
                bone.ik_min_z = swap * (-1)
        
        return {'FINISHED'}