from typing import List
import bpy
from bpy.types import NlaTrack, Object
from .render_config import *

class BJT_BatchJob():
    """A batch rendering job for a given set of NLA tracks."""
    def __init__(self, config: BJT_RenderConfig, tracks: List[NlaTrack], onComplete: function, onCancel: function) -> None:
        self.config = config
        self.tracks = tracks
        self.onComplete = onComplete
        self.onCancel = onCancel

    config: BJT_RenderConfig
    tracks: List[NlaTrack]
    camera: Object
    onComplete: function
    onCancel: function

    def unbind(self) -> None:
        bpy.app.handlers.render_complete.remove(self.finishJob)
        bpy.app.handlers.render_complete.remove(self.cancelJob)

    def finishJob(self) -> None:
        self.unbind()
        self.onComplete()

    def cancelJob(self) -> None:
        self.unbind()
        self.onCancel()

    def runJob(self) -> None:
        self.config.apply() # Apply render config

        for track in self.tracks:
            track.mute = False

        # Bind event handlers
        bpy.app.handlers.render_complete.append(self.finishJob)
        bpy.app.handlers.render_cancel.append(self.cancelJob)

        # Initiate render
        bpy.ops.render.render(animation=True, write_still=False, use_viewport=False)