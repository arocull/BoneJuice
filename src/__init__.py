bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (3, 3, 0),
    "version" : (0, 0, 11),
    "location" : "Edit Armature, Pose Mode, Object Mode",
    "warning" : "",
    "doc_url": "https://github.com/arocull/BoneJuice",
    "category" : "Armature, Object"
}

import bpy
from .utility import getPreferences
from .registrator import registerClass, unregisterClass
from .luchadores import registerLuchadores, unregisterLuchadores
from .index import BINDINGS

## PREFERENCES
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

class BoneJuiceGlobals:
    luchadoresRegistered: bool = False

class BoneJuicePreferences(AddonPreferences):
    bl_idname: str = __name__

    def toggleLuchadores(self, context):
        print(self.enableLuchadores)
        print(BoneJuiceGlobals.luchadoresRegistered)
        if self.enableLuchadores and (not BoneJuiceGlobals.luchadoresRegistered):
            registerLuchadoresHelper()
        elif (not self.enableLuchadores) and BoneJuiceGlobals.luchadoresRegistered:
            unregisterLuchadoresHelper()

    enableLuchadores: BoolProperty(
        name="Enable Luchadores Workflow",
        description="If true, enables tools for annotating and exporting to the Luchadores engine.",
        default=False,
        update=toggleLuchadores
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BoneJuice Preferences")
        layout.prop(self, "enableLuchadores")

## REGISTER
def registerLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = True
    registerLuchadores()

def unregisterLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = False
    unregisterLuchadores()

def register():
    bpy.utils.register_class(BoneJuicePreferences)

    for item in BINDINGS:
        registerClass(item[0], item[1], item[2])

    if getPreferences(bpy.context).enableLuchadores:
        registerLuchadoresHelper()

def unregister():
    for item in BINDINGS:
        unregisterClass(item[0], item[1], item[2])

    if BoneJuiceGlobals.luchadoresRegistered:
        unregisterLuchadoresHelper()

    bpy.utils.unregister_class(BoneJuicePreferences)

if __name__ == "__main__":
    register()
