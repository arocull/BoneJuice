import bpy
from bpy.types import EditBone, PoseBone, Operator
from bpy.props import BoolProperty, EnumProperty
from typing import List

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
            # TODO: Switch to bpy.ops.pose.rotation_mode_set('')

        self.report({'INFO'}, "Converted selected bone Rotation Modes to " + self.rotMode) # Provide user feedback
        
        return {'FINISHED'}

class BoneJuice_SelectBoneChainEnds(Operator):
    """Selects the very last bones in the hiearchy below the currently selected bones"""
    bl_idname = "object.bj_select_bone_chain_ends"
    bl_label = "Select Ends Bones"
    bl_description = "Selects the very last bones in the hiearchy below the currently selected bones"
    bl_options = {'REGISTER', 'UNDO'}

        ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_SelectBoneChainEnds.bl_idname,
            text="Select End Bones",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_SelectBoneChainEnds.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    ignoreNonDeform: BoolProperty(
        name = "Ignore Non-Deforming",
        description = "If true, does not select non-deforming bones like IK Handles (but will still select deforming children if they have any)",
        default=True,
    )
    extendSelection: BoolProperty(
        name = "Extend",
        description = "If true, adds these bones to the selection rather than replacing it",
        default = False,
    )
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        startingBones: List[EditBone] = bpy.context.selected_editable_bones
        if len(startingBones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        if not self.extendSelection: # Deselect everything if that's what we're doing
            bpy.ops.armature.select_all(action='DESELECT')
        
        # Grab all child bones in hiearchy
        allBones: List[EditBone] = startingBones.copy()
        for bone in startingBones:
            allBones.extend(bone.children_recursive)
        
        for bone in allBones:
            if len(bone.children) == 0: # If this bone has no children
                if self.ignoreNonDeform and not bone.use_deform: # Pass if we're ignoring non-deformers, and this isn't deforming
                    pass
                else: # Otherwise, welcome to the club
                    bone.select = True

        self.report({'INFO'}, "Selected end bones")
        return {'FINISHED'}
