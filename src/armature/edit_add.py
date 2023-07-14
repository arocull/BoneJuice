import string
import bpy
from typing import List
from bpy.props import IntProperty, StringProperty, BoolProperty, FloatProperty
from bpy.types import Armature, EditBone, Operator
from mathutils import Vector
from ..utility import dist_threshold, lerpVector, raycast, get_active
from math import pi

class BoneJuice_SurfacePlacer(Operator):
    bl_idname = "bj.surface_bone_placer"
    bl_label = "Surface Bone Placer"
    bl_description = "Places bones on the surface of an object, facing the normal"
    bl_options = {"REGISTER","UNDO"}

    armature: Armature = None
    boneLength: float = 0.2
    lastClick: Vector
    clicks: int = 0

    def button(self, context):
        self.layout.operator(
            BoneJuice_SurfacePlacer.bl_idname,
            text="Place Surface Bones",
            icon='BONE_DATA')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_SurfacePlacer.bl_idname, "blob/master/docs/examples/surface_bone_placer.md"),
        )
        return url_manual_prefix, url_manual_mapping

    def modal(self, context, event: bpy.types.Event): # Runs every time the user inputs
        # If we're not in the proper context (active object has changed or not in edit mode), leave before we break stuff
        # OR if user escapes or tabs out
        if get_active().data != self.armature or bpy.context.mode != 'EDIT_ARMATURE' or event.type in {'ESC', 'TAB'}:
            self.report({'INFO'}, "Exited Surface Bone Placer mode")
            return {'CANCELLED'}

        # Only accept plain left click inputs to allow for navigation
        if event.type == 'LEFTMOUSE' and not event.shift and not event.alt and not event.ctrl:
            self.place_bone(context, event)
            return {'RUNNING_MODAL'}
        
        # User is attempting to undo a mistake. Close modal to push these changes to the stack,
        # then allow pass-through so we can undo what we did
        if event.type == 'Z' and event.ctrl:
            self.report({'INFO'}, "Exited Surface Bone Placer mode")
            return {'CANCELLED', 'PASS_THROUGH'}

        return {'PASS_THROUGH'} # Allow user inputs to move through

    def invoke(self, context, event): # Runs when modal is started, or "invoked"
        if context.space_data.type != 'VIEW_3D':
            self.report({'WARNING'}, "Active space must be a 3D View")
            return {'CANCELLED'}

        if type(get_active().data) is Armature:
            self.armature = get_active().data
            bpy.ops.object.mode_set(mode='EDIT')
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        
        self.report({'WARNING'}, "Active/selected object must be an armature")
        return {'CANCELLED'}
    
    def place_bone(self, context, event):
        hit, pos, norm, idx = raycast(context, event, "BJIgnore")

         # Don't place a bone if we didn't find anything, or are too close to our last position
        if hit == None or (self.clicks > 0 and dist_threshold(pos, self.lastClick, 0.1)):
            return
        
        # Increment clicks and store last click position
        self.clicks = self.clicks + 1
        self.lastClick = pos
        
        # Create new bone
        bone: EditBone = self.armature.edit_bones.new("SurfaceBone")
        bone.head = pos - (norm * (self.boneLength / 2)) # Position head below surface normal
        bone.tail = pos + norm * self.boneLength # And make tail of it point out
        bone.align_roll(norm) # Align roll of bone to point toward Z Axis
        
        if bpy.context.active_bone: # If we have an active parent bone
            parent: EditBone = bpy.context.active_bone

            # Unselect all currently selected bones
            for b in bpy.context.selected_editable_bones:
                b.select = False
            bone.select = True # Select this bone

            bpy.ops.armature.parent_set(type='OFFSET') # Set bone parent to other bone with a relative offset
            bone.parent = bpy.context.active_bone # Then apply the new parent
            
            # Deselect all bones again
            for b in bpy.context.selected_editable_bones:
                b.select = False
            
            self.report({'INFO'}, "Placed bone " + bone.name + " as child of " + parent.name)
        else:
            self.report({'INFO'}, "Placed bone " + bone.name)
        
        # Apply inverse of global transform matrix so bone is placed at global coordinates, not local
        bone.transform(bpy.context.object.matrix_world.inverted())

class BoneJuice_AddLeafBones(Operator):
    """Adds leaf bone endings to the selected bones."""
    bl_idname = "bj.add_leaf_bones"
    bl_label = "Add Leaf Bones"
    bl_description = "Adds leaf bone endings to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_AddLeafBones.bl_idname,
            text="Leaf Bones",
            icon='BONE_DATA')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_AddLeafBones.bl_idname, "blob/master/docs/examples/add_leaf_bones.md"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    preserveSelection: BoolProperty(
        name = "Preserve Selection",
        description = "If true, does not alter selection to select the newly created bones",
        default = False,
    )
    boneLength: FloatProperty(
        name = "Bone Length",
        description = "Length of the bones to add",
        default = 0.1,
        min = 0,
        soft_min = 0,
        soft_max = 1,
    )
    suffix: StringProperty(
        name = "Name Suffix",
        description = "The leaf bones will have the name of their parent with this suffix added",
        default = "_leaf",
    )
    usePrefixInstead: BoolProperty(
        name = "Use Suffix as Prefix",
        description = "If true, uses the Name Suffix as a prefix instead",
        default = False,
    )
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        bones: List[EditBone] = bpy.context.selected_editable_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}
        
        armatureObj = bpy.context.active_object
        editArmature: Armature
        if type(armatureObj.data) is Armature:
            editArmature = armatureObj.data
        else:
            self.report({'WARNING'}, "Active object is not an armature!")
            return {'FINISHED'}

        newLeafBones: List[EditBone] = []
        for bone in bones:
            boneName: str = bone.name
            if self.usePrefixInstead:
                boneName = self.suffix + bone.name
            else:    
                lastIdentifierIdx = max(boneName.rfind("_"), boneName.rfind("."))
                if lastIdentifierIdx == -1:
                    boneName = boneName + self.suffix
                else:
                    boneName = boneName[0:lastIdentifierIdx] + self.suffix + boneName[lastIdentifierIdx:len(boneName)]
            
            leafBone: EditBone = editArmature.edit_bones.new(boneName)
            leafBone.parent = bone
            leafBone.use_deform = False
            leafBone.use_connect = True
            leafBone.head = bone.tail

            headPos = Vector((bone.head[0], bone.head[1], bone.head[2]))
            tailPos = Vector((bone.tail[0], bone.tail[1], bone.tail[2]))
            leafTail: Vector = (tailPos - headPos).normalized() * self.boneLength + tailPos

            leafBone.tail = [leafTail.x, leafTail.y, leafTail.z]
            newLeafBones.append(leafBone)
        
        if not self.preserveSelection:
            bpy.ops.armature.select_all(action='DESELECT')
            for bone in newLeafBones:
                bone.select = True

        self.report({'INFO'}, "Geneated leaf bones.")
        return {'FINISHED'}

class BoneJuice_AddBoneCircle(Operator):
    """Creates a circle of bones around the active one."""
    bl_idname = "bj.add_bone_circle"
    bl_label = "Add Bone Circle"
    bl_description = "Creates a circle of bones around the active one"
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_AddBoneCircle.bl_idname,
            text="Bone Circle",
            icon='BONE_DATA')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_AddBoneCircle.bl_idname, "blob/master/docs/examples/add_bone_circle.md"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    count: IntProperty (
        name = "Count",
        description = "Number of bones to place around the circle",
        default = 5,
        min = 1,
        soft_max = 12,
    )
    rotationOffset: FloatProperty(
        name = "Rotation Offset",
        description = "Offset to start rotation with, in degrees",
        soft_min = 0,
        soft_max = 2 * pi,
        subtype='ANGLE',
        unit='ROTATION',
    )
    circleRadius: FloatProperty(
        name = "Radius",
        description = "Radius to place the bones in around the current one",
        default = 1.0,
        soft_min = 0.05,
        soft_max = 2.0,
        unit = 'LENGTH',
    )
    boneLength: FloatProperty(
        name = "Bone Length",
        description = "Length of the bones to add",
        default = 0.2,
        min = 0,
        soft_min = 0.1,
        soft_max = 1,
        unit = 'LENGTH',
    )
    toTail: FloatProperty(
        name = "Head/Tail",
        description= "Proportion for bone placement, near either the head (0%) or tail (100%) of the active bone",
        default = 0.0,
        soft_min = 0.0,
        soft_max = 1.0,
        precision = 3,
        subtype = 'FACTOR',
    )
    boneName: StringProperty(
        name = "Name",
        description = "Name of the created bones. # will be replaced with the index",
        default = "circle#",
    )
    useDeform: BoolProperty(
        name = "Use Deform",
        description = "If true, bones are marked to deform. False otherwise",
        default = False,
    )
    preserveSelection: BoolProperty(
        name = "Preserve Selection",
        description = "If true, does not alter selection to select the newly created bones",
        default = False,
    )
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.context):
        bones: List[EditBone] = bpy.context.selected_editable_bones
        if len(bones) == 0:
            self.report({'WARNING'}, "No bones selected")
            return {'FINISHED'}
        
        armatureObj = bpy.context.active_object
        editArmature: Armature
        if type(armatureObj.data) is Armature:
            editArmature = armatureObj.data
        else:
            self.report({'WARNING'}, "Active object is not an armature!")
            return {'FINISHED'}
        
        if context.active_bone is None:
            self.report({'WARNING'}, "No active edit bone!")
            return {'FINISHED'}
        bone: EditBone = context.active_bone
        origRoll: float = bone.roll

        newBones: List[EditBone] = []
        idx: int = 0
        while idx < self.count:
            idx = idx + 1
            theta: float = self.rotationOffset + (((2 * pi) / float(self.count)) * float(idx))
            boneName: str = str(self.boneName).replace('#', str(idx))
            
            circleBone: EditBone = editArmature.edit_bones.new(boneName)
            circleBone.parent = bone
            circleBone.use_deform = self.useDeform
            circleBone.use_connect = False

            headPos = Vector((bone.head[0], bone.head[1], bone.head[2]))
            tailPos = Vector((bone.tail[0], bone.tail[1], bone.tail[2]))
            basePose: Vector = lerpVector(headPos, tailPos, self.toTail)
            tailDir: Vector = (tailPos - headPos).normalized()
            circleTail: Vector = tailDir * self.boneLength + basePose

            bone.roll = origRoll + theta

            circleBone.head = basePose + bone.z_axis * self.circleRadius
            circleBone.tail = circleTail + bone.z_axis * self.circleRadius
            circleBone.align_roll(basePose - circleBone.head)
            newBones.append(circleBone)
        
        bone.roll = origRoll

        if not self.preserveSelection:
            bpy.ops.armature.select_all(action='DESELECT')
            for bone in newBones:
                bone.select = True

        self.report({'INFO'}, "Geneated circle bones.")
        return {'FINISHED'}
