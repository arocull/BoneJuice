import bpy
from bpy.types import EditBone, Operator
from bpy.props import EnumProperty, BoolVectorProperty
from typing import List

from bpy_types import PoseBone
from .utility import get_active

class BoneJuice_MarkSide(Operator):
    """Sets the side of the selected edit bones, similar to Armature > Names > Auto-Name Left/Right, but with more control"""
    bl_idname = "armature.bj_mark_bone_side"
    bl_label = "Mark Side"
    bl_description = "Sets the side of the selected edit bones, similar to Armature > Names > Auto-Name Left/Right, but with more control"
    bl_options = {'REGISTER', 'UNDO'}

    side: EnumProperty(
        name = 'Side',
        description = 'What method to use for setting the bone sides',
        items = [
            ('automatic', 'Automatic', 'Bones with head X positions > 0.01 will be marked as Left, and head X positions < -0.01 marked as right.'),
            ('left', 'Left', 'Marks the bones as left-sided'),
            ('right', 'Right', 'Marks the bones as right-sided'),
        ],
        default = 'automatic',
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_MarkSide.bl_idname,
            text="Mark Side",
            icon='MOD_MIRROR')
    def button_edit(self, context):
        self.layout.operator(
            BoneJuice_MarkSide.bl_idname,
            text="Mark Side",
            icon='MOD_MIRROR')
    def button_pose(self, context):
        self.layout.operator(
            BoneJuice_MarkSide.bl_idname,
            text="Mark Side",
            icon='MOD_MIRROR')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.armature.bj_mark_bone_side", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.types.Context):
        bones: List[EditBone] = bpy.context.selected_editable_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            name: str = bone.name.replace('.L', '').replace('.R', '')
            if self.side == 'automatic':
                if (bone.head.x > 0.01):
                    name += '.L'
                elif (bone.head.x < -0.01):
                    name += '.R'
            elif self.side == 'left':
                name += '.L'
            elif self.side == 'right':
                name += '.R'
            
            bone.name = name
        
        return {'FINISHED'}

class BoneJuice_BulkSetRotationMode(Operator):
    """Sets the rotation mode of the selected pose bones."""
    bl_idname = "armature.bj_set_rotation_mode"
    bl_label = "Set Rotation Mode"
    bl_description = "Sets the rotation mode of the selected pose bones."
    bl_options = {'REGISTER', 'UNDO'}

    rotMode: EnumProperty(
        name = 'Rotation Mode',
        description = 'What mode to use for rotations',
        items = [
            ('QUATERNION', 'Quaternion (WXYZ)', 'Use standard quaternions. No gimbal lock, but harder to use with animation curves. This is Blender\'s default.'),
            ('AXIS_ANGLE', 'Axis Angle', 'Use an axis angle instead for bone rotation.'),
            ('XYZ', 'XYZ Euler', 'Use euler angles for bone rotation. Susceptible to Gimbal Lock, but easier to animate.'),
            ('XZY', 'XZY Euler', 'Euler option, with different axis order.'),
            ('YXZ', 'YXZ Euler', 'Euler option, with different axis order.'),
            ('YZX', 'YZX Euler', 'Euler option, with different axis order.'),
            ('ZXY', 'ZXY Euler', 'Euler option, with different axis order.'),
            ('ZYX', 'ZYX Euler', 'Euler option, with different axis order.'),
        ],
        default = 'XYZ',
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_BulkSetRotationMode.bl_idname,
            text="Set Rotation Mode",
            icon='ORIENTATION_GIMBAL')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.armature.bj_set_rotation_mode", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.types.Context):
        bones: List[PoseBone] = bpy.context.selected_pose_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            bone.rotation_mode = self.rotMode

        self.report({'INFO'}, "Converted selected bone Rotation Modes to " + self.rotMode) # Provide user feedback
        
        return {'FINISHED'}