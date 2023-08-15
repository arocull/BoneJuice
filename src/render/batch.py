from tokenize import String
import bpy
from bpy.ops import action
from bpy.types import NlaStrip, NlaTrack, NlaTracks, Object, Operator, Camera
from bpy.props import BoolProperty, IntProperty, StringProperty
from typing import Dict, List
from ..utility import get_active, set_active, NlaDictList_append

# TODO: Convert this to a dialogue!
class BoneJuice_BatchRenderActions(Operator):
    """Adjusts render settings, and then renders out each NLA track on selected objects using a list of cameras."""
    bl_idname = "bj.batch_render_actions"
    bl_label = "Batch Render NLA Tracks"
    bl_description = "Adjusts render settings, and then renders out each NLA track on select objects using a list of cameras."
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_BatchRenderActions.bl_idname,
            text="Batch Render NLA Tracks",
            icon='ARMATURE_DATA')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_BatchRenderActions.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    renderPrefix: StringProperty(
        name = "Render Prefix",
        description = "Additional prefix for filenames, this is added to the configured render path during the batch render.",
        default = "BATCH_",
    )
    framerateGoal: IntProperty(
        name = "Framerate",
        description = "Custom framerate to render scenes at. Animations will last the same amount of time, but will render with this FPS instead with a different # frames.",
        min = 1,
        max = 240,
        default = 10,
    )
    doLooping: BoolProperty(
        name = "Looping Animations",
        description = "If true, stops rendering the animation immediately before the last keyframe, to make loops more smooth.",
        default = True,
    )
    limitToSelected: BoolProperty(
        name = "Selected Tracks Only",
        description = "If true, will only render NLA tracks that are selected inside the active object.",
        default = True,
    )
    constrainStartFrame: BoolProperty(
        name = "Constrain Start Frame",
        description="If true, will clamp start frame to the frame the animation track starts on. Otherwise, uses the current render settings' start frame.",
        default = False,
    )
    constrainEndFrame: BoolProperty(
        name = "Constrain End Frame",
        description="If true, will clamp end frame to the frame the animation track starts on. Otherwise, uses the current render settings' end frame.",
        default = True,
    )


    ## EXECUTION
    def appendToTrackList(renderTracks: Dict[str, List[NlaTrack]], key: str, track: NlaTrack):
        if hasattr(renderTracks, key):
            renderTracks[key].append(track)
        else:
            renderTracks[key] = [track]
    
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context: bpy.types.Context):
        # First, get all camera objects to render from
        if not bpy.context.collection:
            self.report({'WARNING'}, "No active collection! Select a collection containing the cameras you want to render.")
            return {'FINISHED'}

        allCams: List[Object] = [] # List of only cameras
        for obj in bpy.context.collection.all_objects:
            if type(obj.data) is Camera:
                allCams.append(obj)

        if len(allCams) == 0:
            self.report({'WARNING'}, "No render cameras found! Select a collection containing the cameras you want to render.")
            return {'FINISHED'}
        
        if len(context.selected_objects) == 0:
            self.report({'WARNING'}, "No objects are selected!")
            return {'FINISHED'}

        # Then, get all selected animation actions
        selectedObj: List[Object] = context.selected_objects
        activeObj = get_active()
        
        # Get all NLA actions. The reaseon they are stored in a list is so we can have different objects with the same tracks coincide
        renderTracks: Dict[str, List[NlaTrack]] = dict()
        for obj in selectedObj: # For each object, iterate through it's NLA tracks, and gather them (or selected ones)
            set_active(obj) # Set object to active to iterate through it's animation data
            try:
                tracks: NlaTracks = bpy.context.object.animation_data.nla_tracks
                for key in tracks.keys():
                    track = tracks.get(key)
                    if not self.limitToSelected:
                        NlaDictList_append(renderTracks, key, track)
                    elif self.limitToSelected and track.select:
                        NlaDictList_append(renderTracks, key, track)
            except AttributeError:
                """Could not find animation data in object"""
        set_active(activeObj) # Reset active object

        if len(renderTracks) == 0:
            self.report({'WARNING'}, "No valid NLA Tracks to render!")
            return {'FINISHED'}


        # ...now start preparing for render! Save existing render configurations.
        outputPrefix: String = context.scene.render.filepath # Fetch output prefix
        frameStart = context.scene.frame_start
        frameEnd = context.scene.frame_end
        setFPS: int = context.scene.render.fps
        setFPSBase: float = context.scene.render.fps_base
        setFrameMapOld: int = context.scene.render.frame_map_old
        setFrameMapNew: int = context.scene.render.frame_map_new
        setFrameStep: int = context.scene.frame_step

        def renderComplete(self, dummy):
            context.scene.render.filepath = outputPrefix # Reset ouput prefix
            context.scene.frame_start = frameStart
            context.scene.frame_end = frameEnd
            context.scene.render.fps = setFPS
            context.scene.render.fps_base = setFPSBase
            context.scene.render.frame_map_old = setFrameMapOld
            context.scene.render.frame_map_new = setFrameMapNew
            context.scene.frame_step = setFrameStep

            bpy.app.handlers.render_complete.remove(renderComplete)
            bpy.app.handlers.render_cancel.remove(renderComplete)

        # Start render! For all NLA tracks...
        for key in renderTracks:
            # mute all other tracks,
            for muteKey in renderTracks:
                for track in renderTracks[muteKey]:
                    track.mute = True
                    track.is_solo = False
            
            animFrameStart = frameStart
            animFrameEnd: int = frameStart
            # but unmute these! And get largest frame value.
            for track in renderTracks[key]:
                track.mute = False

                strips: List[NlaStrip] = track.strips
                for strip in strips:
                    if strip.frame_end > animFrameEnd:
                        animFrameEnd = strip.frame_end
                    if strip.frame_start < animFrameStart:
                        animFrameStart = strip.frame_start
            
            # Next, set render settings to match FPS settings, and constrain frame render times
            
            if self.constrainStartFrame:
                context.scene.frame_start = int(animFrameStart)
            if self.constrainEndFrame:
                context.scene.frame_end = int(animFrameEnd)
            
            if self.doLooping:
                context.scene.frame_end = context.scene.frame_end - 1

            animFrameLength: int = context.scene.frame_end - context.scene.frame_start # Get length of animation in frames
            oldFPS: float = (float(setFPS) / setFPSBase)
            animTimeLength: float = float(animFrameLength) / (float(setFPS) / setFPSBase) # Get original time length of animation in seconds
            
            # NOW, convert animation to new frame rate
            context.scene.render.fps = self.framerateGoal
            context.scene.render.fps_base = 1.000
            context.scene.frame_step = 1

            animNewLength: int = animTimeLength * context.scene.render.fps # New length of animation in frames
            
            # X number of frames with normal FPS settings are Y number of frames with new FPS settings
            context.scene.render.frame_map_old = int(animFrameLength)
            context.scene.render.frame_map_new = int(animNewLength)
            # Adjust beginning of start and end of animation to fit new FPS settings + scalings
            context.scene.frame_start = int((float(context.scene.frame_start) / oldFPS) * context.scene.render.fps)
            context.scene.frame_end = int(context.scene.frame_start + animNewLength)

            # ...and for all cameras!
            for cam in allCams:
                context.scene.render.filepath = outputPrefix + self.renderPrefix + "_" + cam.name + "_" + key + "_####" # generate output path
                self.report({'INFO'}, "Now rendering action '" + key + "' with camera '" + cam.name + "'...")
                bpy.app.handlers.render_complete.append(renderComplete)
                bpy.app.handlers.render_cancel.append(renderComplete)
                context.scene.camera = cam
                bpy.ops.render.render(animation=True, write_still=False, use_viewport=False) # and finally, render!
                # TODO: Wait for render to complete to move on
        
        self.report({'INFO'}, "Completed batch render and reset render settings.")

        return {'FINISHED'}