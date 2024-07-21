from copyreg import constructor
import bpy
from bpy.types import Object

class BJT_RenderConfig:
    """Retains a set of render configuration settings"""
    def __init__(
        self, prefix: str, camera: bpy.types.Object, start: int = 1, end: int = 250, fps: int = 24, fpsbase: float = 1.00, step: int = 1, map_old: int = 100, map_new: int = 100
    ) -> None:
        self.prefix = prefix
        self.camera = camera
        self.start = start
        self.end = end
        self.fps = fps
        self.fpsbase = fpsbase
        self.step = step
        self.map_old = map_old
        self.map_new = map_new
    
    prefix: str
    camera: Object
    start: int
    end: int
    fps: int
    fpsbase: float
    step: int
    map_old: int
    map_new:int

    def apply(self):
        """Apply the render settings to the current Blender context"""
        context = bpy.context
        context.scene.render.filepath = self.prefix
        context.scene.frame_start = self.start
        context.scene.frame_end = self.end
        context.scene.render.fps = self.fps
        context.scene.render.fps_base = self.fpsbase
        context.scene.frame_step = self.step
        context.scene.render.frame_map_old = self.map_old
        context.scene.render.frame_map_new = self.map_new
        context.scene.camera = self.camera

def makeRenderConfigDefault(context: bpy.types.Context) -> BJT_RenderConfig:
    return BJT_RenderConfig(
        context.scene.render.filepath,
        context.scene.camera,
        context.scene.frame_start,
        context.scene.frame_end,
        context.scene.render.fps,
        context.scene.render.fps_base,
        context.scene.frame_step,
        context.scene.render.frame_map_old,
        context.scene.render.frame_map_new,
    )