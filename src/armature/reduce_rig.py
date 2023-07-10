import bpy
from bpy.types import EditBone, Operator, Armature, Object
from bpy.props import BoolProperty
from ..utility import fill_layers_array

# Steps
#
# 1. delete all non-deforming bones (that aren't object parents) (optional)
# 2. attempt to automatically parent unparented bones to nearest bone (optional)
# 3. remove any pose constraints on bones (optional)
# 4. assign all bones on same layer (optional)
#
class BoneJuice_ReduceRig(Operator):
    """Reduces a character rig for game exporting"""
    bl_idname = "bj.reduce_rig"
    bl_label = "Reduce Rig"
    bl_description = "Reduces a character rig for game exporting. THIS WILL CAUSE DATA LOSS and is meant for export processes"
    bl_options = {'REGISTER', 'UNDO'}

    auto_parent: BoolProperty(
        name = "Auto-Parent",
        description = "If true, attempts to automatically re-parent bones to nearest ones that share the same ancestor",
        default = True
    )
    clear_constraints: BoolProperty(
        name="Clear Constraints",
        description="If true, removes constraints on all bones",
        default=True,
    )
    reset_layers: BoolProperty(
        name = "Reset Layers",
        description = "If true, assigns all bones to a single layer when finished",
        default = True
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_ReduceRig.bl_idname,
            text=BoneJuice_ReduceRig.bl_label,
            icon='NONE')
    
    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_ReduceRig.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping
    
    def execute(self, context: bpy.types.Context):
        if not (context.active_object and context.active_object.type == 'ARMATURE'):
            self.report({'WARNING'}, "Must have an active Armature")
            return {'FINISHED'}

        # rigObj: Object = context.active_object        
        rig: Armature = context.active_object.data
        rig.layers = fill_layers_array(True,32)
        bpy.ops.object.mode_set(mode='EDIT')

        unparented: list[EditBone] = list[EditBone]()

        print(len(rig.edit_bones))
        
        # If we don't have a valid parent, find the highest deformable parent in hiearchy
        for bone in rig.edit_bones:
           if bone.use_deform and ((bone.parent == None) or (not bone.parent.use_deform)):
               set_best_parent(bone)
               if bone.parent == None: # If we still couldn't find a good parent, save it for later
                   unparented.append(bone)
        
        # Now, delete all non-deforming bones
        bpy.ops.armature.select_all(action='DESELECT')
        for bone in rig.edit_bones:
            if not bone.use_deform:
                bone.select = True
                print("A")
        bpy.ops.armature.delete()
        bpy.ops.armature.select_all(action='DESELECT')

        # Auto-parent bones
        if self.auto_parent:
            for bone in unparented:
                bone.select = True
            bpy.ops.bj.autoparent_bones()
        
        # Reset bone layers
        if self.reset_layers:
            layers = fill_layers_array(False)
            layers[0] = True
            for bone in rig.edit_bones:
                bone.layers = layers
            rig.layers = layers
        
        # Clear bone constraints
        if self.clear_constraints:
            bpy.ops.object.mode_set(mode='POSE')
            bpy.ops.pose.select_all(action='SELECT')
            bpy.ops.pose.constraints_clear()
        
        # Return to object mode--done!
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}


def set_best_parent(bone: EditBone):
    parents: list[EditBone] = bone.parent_recursive
    bone.parent = None
    for p in parents:
        if p.use_deform:
            bone.use_connect = False
            bone.parent = p
            break
