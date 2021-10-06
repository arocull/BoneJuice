import bpy
from bpy.ops import armature
from bpy.types import Armature, Bone, EditBone
from mathutils import Vector, Matrix
from .utility import dist_threshold, raycast, get_active, vect_to_string

# https://blender.stackexchange.com/questions/28225/armature-not-in-edit-mode

class BoneJuice_SurfacePlacer(bpy.types.Operator):
    bl_idname = "view3d.bone_placer_surf"
    bl_label = "Surface Bone Placer"
    bl_description = "Places bones on the surface of an object, facing the normal"
    bl_options = {"REGISTER"}

    armature: Armature = None
    boneLength: float = 0.2
    lastClick: Vector
    clicks: int = 0

    def modal(self, context, event: bpy.types.Event): # Runs every time the user inputs
        if event.type == 'LEFTMOUSE' and not event.shift and not event.alt and not event.ctrl:
            self.place_bone(context, event)
            return {'RUNNING_MODAL'}
        elif event.type in {'ESC', 'TAB', '4'}: # User is attempting to exit context
            #bpy.ops.object.mode_set('OBJECT')
            self.report({'INFO'}, "Exited Surface Bone Placer mode")
            return {'CANCELLED'}

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
        
        #bpy.ops.armature.bone_primitive_add(name = "SurfaceBone")
        #bone: EditBone = bpy.context.active_bone
        bone: EditBone = self.armature.edit_bones.new("SurfaceBone")
        bone.head = pos - (norm * (self.boneLength / 2))
        bone.tail = pos + norm * self.boneLength
        bone.align_roll(norm) # Align roll of bone to point toward Z Axis
        
        if bpy.context.active_bone: # If we have an active parent bone
            parent: EditBone = bpy.context.active_bone

            # Unselect all currently selected bones
            for b in bpy.context.selected_editable_bones:
                b.select = False
            bone.select = True # Select this bone

            bpy.ops.armature.parent_set(type='OFFSET') # Set bone parent to other bone with a relative offset
            #bone.transform(Matrix.inverted(parent.matrix), True, True) # Invert the transformation matrix of it
            bone.parent = bpy.context.active_bone # Then apply the new parent
            
            for b in bpy.context.selected_editable_bones:
                b.select = False
            
            self.report({'INFO'}, "Placed bone " + bone.name + " as child of " + parent.name)
        else:
            self.report({'INFO'}, "Placed bone " + bone.name)