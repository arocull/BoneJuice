import string
import bpy
from typing import List
from bpy.ops import armature
from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import Armature, EditBone, Operator
from mathutils import Vector
from ..utility import dist_threshold, raycast, get_active

class BoneJuice_SurfacePlacer(Operator):
    bl_idname = "armature.bj_bone_placer_surf"
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
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.armature.bj_bone_placer_surf", "scene_layout/object/types.html"),
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
    bl_idname = "object.bj_add_leaf_bones"
    bl_label = "Add Leaf Bones"
    bl_description = "Adds leaf bone endings to the selected bones"
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_AddLeafBones.bl_idname,
            text="Add Leaf Bones",
            icon='BONE_DATA')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.object.bj_add_leaf_bones", "scene_layout/object/types.html"),
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
