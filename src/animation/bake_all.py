import bpy
from bpy.types import Operator, Armature, Object, Action, NlaTrack
from bpy.props import StringProperty, BoolProperty, IntProperty

class BoneJuice_Animation_BakeAll(Operator):
    """Bake all animations for the active armature."""
    bl_idname = "bj.anim_bakeall"
    bl_label = "Bake All Actions"
    bl_description = "Bakes all actions for the given armature"
    
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_Animation_BakeAll.bl_idname,
            text=BoneJuice_Animation_BakeAll.bl_label,
            icon='NONE')
    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_Animation_BakeAll.bl_idname, "docs/"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    filter: StringProperty(
        name = "Prefix Filter",
        description = "If not empty, only bakes animations with this prefix",
        default = "",
    )
    stepSize: IntProperty(
        name = "Step Size",
        description = "Number of frames between each key (including the previously keyed frame)",
        default = 1,
    )
    doOverwrite: BoolProperty(
        name = "Overwrite Actions",
        description = "If true, overwrites all actions with their baked variants",
        default = True,
    )
    doVisual: BoolProperty(
        name = "Visual Keying",
        description = "Keyframe from the final transformation (with constraints applied)",
        default = True,
    )
    doClean: BoolProperty(
        name = "Clean Curves",
        description = "If true, removes redundant keys after baking",
        default = False,
    )
    
    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        rig: Object = context.active_object
        if rig == None or (not type(rig.data) is Armature):
            self.report({'WARNING'}, "No active Armature!")
            return {'FINISHED'}
        
        bpy.ops.object.mode_set(mode='POSE') # Enter pose mode

        # Mute all NLA tracks
        for t in rig.animation_data.nla_tracks:
            track: NlaTrack = t
            track.mute = True
            track.is_solo = False

        actionCount: int = 0
        # Iterate through all actions, set armature to use them, and bake pose
        for actionData in bpy.data.actions:
            act: Action = actionData
            # Skip animations that aren't in our filter
            if len(self.filter) > 0 and not self.filter in act.name:
                continue
            rig.animation_data.action = act # Set rig to current action

            bpy.ops.object.mode_set(mode='POSE') # Enter pose mode
            bpy.ops.nla.bake(
                frame_start=int(act.frame_start),
                frame_end=int(act.frame_end),
                step=self.stepSize,
                
                only_selected=False,
                visual_keying=self.doVisual,
                use_current_action=self.doOverwrite,
                clean_curves=self.doClean,
                bake_types={'POSE'}, # only bake pose data, not objects

                # Can't clear constraints because rig may not be local
                # ...also need constraints for the upcoming anims
                clear_constraints=False,
                clear_parents=False, # Same goes for parents
            )
            actionCount += 1
        
        rig.animation_data.action = None

        self.report({'INFO'}, "Baked {0} actions.".format(actionCount))
        return {'FINISHED'}

