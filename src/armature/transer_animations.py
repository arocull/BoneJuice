import bpy
from bpy.types import Operator, Object, Armature, NlaStrip, Bone, PoseBone
from bpy.props import PointerProperty
from ..utility import fill_layers_array

class BoneJuice_TransferAnimations(Operator):
    """Transfers animations from one collection to the other."""
    bl_idname = "bj.transfer_animations"
    bl_label = "Transfer Animations"
    bl_description = "Operation description."
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_TransferAnimations.bl_idname,
            text=BoneJuice_TransferAnimations.bl_label,
            icon='NONE')
    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_TransferAnimations.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping
    
    def verifyArmature(self, object: bpy.types.Object) -> bool:
        return object.type == 'ARMATURE'
    
    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        #self.layout.label("Transfer baked animation data from the selected armature to the active one?")
        return context.window_manager.invoke_props_dialog(self)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        if context.active_object == None or (context.active_object and not self.verifyArmature(context.active_object)):
            self.report({'WARNING'}, "Needs an active Armature to transfer to!")
            return {'FINISHED'}
        if len(context.selected_objects) != 1 or not self.verifyArmature(context.selected_objects[0]):
            self.report({'WARNING'}, "Must have one selected Armature to transfer from!")
            return {'FINISHED'}
        if context.selected_objects[0] == context.active_object:
            self.report({'WARNING'}, "Can't transfer animations from self!")
            return {'FINISHED'}
        
        transferTo: Object = context.active_object
        transferFrom: Object = context.selected_objects[0]

        armTo: Armature = transferTo.data
        armFrom: Armature = transferTo.data

        layersTo: list[bool] = armTo.layers
        layersFrom: list[bool] = armFrom.layers
        armTo.layers = fill_layers_array(True)
        armFrom.layers = fill_layers_array(True)

        armTo.layers

        # Clear animation data from rig we're transferring to
        if not transferTo.animation_data == None:
            transferTo.animation_data_clear()
        transferTo.animation_data_create()

        bpy.ops.object.mode_set(mode='POSE') # Enter pose mode to perform animation
        
        for _, track in enumerate(transferFrom.animation_data.nla_tracks):
            self.report({'INFO'}, "Baking " + track.name + "...")

            track.is_solo = True

            # Default to scene beginning and end
            startTime: float = context.scene.frame_end
            endTime: float = context.scene.frame_start
            # ...if strips have earlier/later configured beginnings and ends, use those instead
            for strip in track.strips:
                
                startTime = min(startTime, strip.action.frame_start)
                endTime = max(endTime, strip.action.frame_end)
            
            storedEndTime = endTime
            endTime = max(startTime, endTime)
            startTime = min(storedEndTime, startTime)

            # Create new NLA track on other rig to use
            
            newTrack = transferTo.animation_data.nla_tracks.new()
            newTrack.name = track.name

            # Iterate through every frame of animation
            for frame in range(int(startTime), int(endTime)):
                context.scene.frame_set(frame)

                for boneKey in armTo.bones.keys():
                    fromBone: Bone = armFrom.bones.get(boneKey)
                    if not fromBone == None:
                        toBone: PoseBone = armTo.bones.get(boneKey)
                        toBone.matrix = fromBone.matrix_local
                        #toBone.matrix_local
                        # toBone.keyframe_insert()
                    bpy.ops.action.keyframe_insert(type='ALL') # Key all channels
                    
                armTo.bones[0].matrix_local = armFrom.bones[0].keys()
                armTo.bones.keyframe_insert()
            
            newStrip: NlaStrip = newTrack.strips.new(name=track.name+"_bake",start=int(startTime),action=armTo.animation_data.action)
            
            track.is_solo = False
        
        armTo.layers = layersTo
        armFrom.layers = layersFrom
        
        bpy.ops.object.mode_set(mode='OBJECT')

        self.report({'INFO'}, "Completed.")
        return {'FINISHED'}
