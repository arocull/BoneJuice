import bpy
from bpy.types import EditBone, Operator
from bpy.props import BoolProperty, EnumProperty, FloatProperty
from typing import List
from mathutils import Vector

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

class BoneJuice_ConnectBones(Operator):
    """Connects the active bone to its immediate child, or vice-versa."""
    bl_idname = "bj.connect_bones"
    bl_label = "Connect Bones"
    bl_description = "Connects the active bone to its immediate child."
    bl_options = {'REGISTER', 'UNDO'}

        ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_ConnectBones.bl_idname,
            text=BoneJuice_ConnectBones.bl_label,
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_ConnectBones.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    reverse: BoolProperty(
        name = "Reverse",
        description = "If true, connects all child bones of the active bone to their parent instead. This creates a more continuous skeleton, but will modify bone head positions",
        default=False,
    )
    recursive: BoolProperty(
        name = "Recursive",
        description = "If true, performs this operation on all children of this bone as well",
        default=True,
    )
    ignoreNonDeform: BoolProperty(
        name = "Ignore Non-Deforming",
        description = "If true, does not iterate through non-deforming bones like IK Handles",
        default=True,
    )
    reverseOnEnds: BoolProperty(
        name = "Reverse on Ends",
        description = "If true and not fully Reversed, reverse mode will trigger on bones with no children",
        default=False,
    )
    alignEnds: BoolProperty(
        name = "Align End Bones",
        description = "If true, attempts to align end bones as if they were leaf bones to their parents, but keeping the bone heads in place",
        default=True,
    )
    leafLength: FloatProperty(
        name = "Aligned Bone Length",
        description = "Length of the aligned bones",
        default = 0.1,
        min = 0,
        soft_min = 0,
        soft_max = 1,
    )

    def draw(self, context: bpy.context):
        layout = self.layout
        col = layout.column()

        col.prop(self, "recursive")
        col.prop(self, "ignoreNonDeform")
        col.prop(self, "reverse")
        if not self.reverse:
            col.label(text="Forward Settings")
            if not self.alignEnds:
                col.prop(self, "reverseOnEnds")
            col.prop(self, "alignEnds")
            if self.alignEnds:
                col.prop(self, "leafLength")

    def align_bone(self, bone: EditBone):
        if bone.parent is None:
            return
        
        dir: Vector = (bone.head - bone.parent.head).normalized()
        bone.tail = bone.head + (dir * self.leafLength)
        bone.roll = bone.parent.roll

    def get_bone_children(self, bone: EditBone) -> List[EditBone]:
        if not self.ignoreNonDeform: # If we're including non-deforming, use the whole list
            return bone.children
        
        # Otherwise, only pick out deforming bones
        validChildren: List[EditBone] = list()
        for item in bone.children:
            if item.use_deform:
                validChildren.append(item)
        
        return validChildren

    def connectToChild(self, bone: EditBone):
        boneChildren = self.get_bone_children(bone)

        if len(boneChildren) == 1: # If we only have one child, set our tail position to its head, then connect the child to us
            child = boneChildren[0]
            bone.tail = child.head
            child.use_connect = True
        elif len(boneChildren) > 1: # Otherwise, set our tail to an average position of all the child bone heads
            tailPos = Vector((0.0,0.0,0.0))
            for item in boneChildren:
                tailPos += item.head
            tailPos /= len(boneChildren)
            bone.tail = tailPos
        else:
            if self.reverseOnEnds:
                self.connectToParent(bone)
            elif self.alignEnds:
                self.align_bone(bone)

        if self.recursive and len(boneChildren) > 0:
            for item in boneChildren:
                self.connectToChild(item)
        
    def connectToParent(self, bone: EditBone):
        if not (bone.parent is None): # Only run if we have a parent bone
            currentTail = bone.head.copy()
            bone.head = bone.parent.tail.copy()
            bone.tail = currentTail
            bone.use_connect = True # Connect ourselves to our parent

        # Edit children AFTER we've moved the parent bone, to kind of pull things backward
        boneChildren = self.get_bone_children(bone)
        if self.recursive and len(boneChildren) > 0:
            for item in boneChildren:
                self.connectToParent(item)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        startingBone: EditBone = bpy.context.active_bone
        if startingBone == None:
            self.report({'WARNING'}, "No active Edit Bone")
            return {'FINISHED'}

        if self.reverse:
            self.connectToParent(startingBone)
        else:
            self.connectToChild(startingBone)

        return {'FINISHED'}

class BoneJuice_SetBoneLength(Operator):
    """Sets the length of the selected edit bones"""
    bl_idname = "bj.set_bone_length"
    bl_label = "Set Bone Length"
    bl_description = "Sets the length of the selected edit bones"
    bl_options = {'REGISTER', 'UNDO'}

    boneLength: FloatProperty(
        name = "Bone Length",
        description = "Length of the bones to add",
        default = 0.1,
        min = 0,
        soft_min = 0,
        soft_max = 1,
    )
    disconnectBones: BoolProperty(
        name = "Disconnect",
        description = "If true, disconnect bones so child bone heads are not pulled",
        default=True,
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_SetBoneLength.bl_idname,
            text=BoneJuice_SetBoneLength.bl_label,
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_SetBoneLength.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    def execute(self, context: bpy.types.Context):
        bones: List[EditBone] = bpy.context.selected_editable_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}

        for bone in bones:
            if self.disconnectBones:
                for item in bone.children:
                    item.use_connect = False
            bone.length = self.boneLength
        
        return {'FINISHED'}
