import bpy
from bpy.props import BoolProperty, FloatProperty, FloatVectorProperty
from ..utility import getRNA_UI

LUCHADORESBONEPROPS = [
    'ldrawable',
    'ldrawcolor',
    'ldrawthickness',
    'lmassweight',
]
LUCHADORESBONEPROPDEFAULTS = [
    False,
    (0.0,0.0,0.0),
    0.2,
    1.0,
]

def define_bone_props():
    bpy.types.Bone.ldrawable = BoolProperty(
        name = "Drawable",
        description = "Whether or not this bone should be drawn when rendering the armature in Luchadores engine",
        default = False,
    )
    bpy.types.Bone.ldrawcolor = FloatVectorProperty(
        name = "Draw Color",
        description = "Color to draw for this bone in Luchadores engine",
        min = 0,
        max = 1,
        subtype = 'COLOR',
        default = (0.0,0.0,0.0),
    )
    bpy.types.Bone.ldrawthickness = FloatProperty(
        name = "Draw Thickness",
        description = "Thickness of this bone for drawing in Luchadores engine, in meters",
        min = 0,
        max = 10,
        soft_max=1,
        step=0.05,
        unit = 'LENGTH',
        default = 0.2,
    )
    bpy.types.Bone.lmassweight = FloatProperty(
        name = "Mass Weight",
        description = "Weight value for the amount of mass this bone uses relative to the entire character's mass",
        min = 0,
        max = 100,
        soft_max = 10,
        default = 1.0
    )

# Luchadores Bone Properties - A list of custom bone properties utilized in the Luchadores engine
class Luchadores_BonePanel(bpy.types.Panel):
    bl_label: str = "Luchadores Properties"
    bl_idname: str = "BONE_PT_luchadores"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context: str = "bone"

    @classmethod
    def poll(cls, context: bpy.context):
        return hasattr(context.active_bone, "lmassweight")
    
    def draw(self, context: bpy.context):
        layout = self.layout

        bone = context.active_bone
        for item in LUCHADORESBONEPROPS:
            layout.prop(bone, property=item)
