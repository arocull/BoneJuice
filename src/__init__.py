import bpy
from .utility import getPreferences
from .registrator import registerClass, unregisterClass, registerMenu, unregisterMenu
from .luchadores import registerLuchadores, unregisterLuchadores
from .index import BINDINGS, BINDINGS_EXPERIMENTAL, MENUBINDINGS
from .globals import BoneJuiceGlobals

## PREFERENCES
from bpy.types import AddonPreferences
from bpy.props import BoolProperty

class BoneJuicePreferences(AddonPreferences):
    bl_idname: str = __name__

    def toggleExperimental(self, context: bpy.types.Context):
        if self.enableExperimental and (not BoneJuiceGlobals.experimentalRegistered):
            registerExperimental()
        elif (not self.enableExperimental) and BoneJuiceGlobals.experimentalRegistered:
            unregisterExperimental()

    def toggleLuchadores(self, context: bpy.types.Context):
        if self.enableLuchadores and (not BoneJuiceGlobals.luchadoresRegistered):
            registerLuchadoresHelper()
        elif (not self.enableLuchadores) and BoneJuiceGlobals.luchadoresRegistered:
            unregisterLuchadoresHelper()

    enableExperimental: BoolProperty(
        name="Enable Experimental Tools",
        description="These tools are messy, unrefined, and extremely niche, but may have some use",
        default=False,
        update=toggleExperimental
    )

    enableLuchadores: BoolProperty(
        name="Enable Luchadores Workflow",
        description="Enables tools for annotating and exporting armatures to the Luchadores engine",
        default=False,
        update=toggleLuchadores
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="BoneJuice Preferences")
        layout.prop(self, "enableExperimental")
        layout.prop(self, "enableLuchadores")

## REGISTER
def registerLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = True
    registerLuchadores()

def unregisterLuchadoresHelper():
    BoneJuiceGlobals.luchadoresRegistered = False
    unregisterLuchadores()

def registerExperimental():
    BoneJuiceGlobals.experimentalRegistered = True
    for item in BINDINGS_EXPERIMENTAL:
        registerClass(item[0], item[1], item[2])
def unregisterExperimental():
    for item in BINDINGS_EXPERIMENTAL:
        unregisterClass(item[0], item[1], item[2])
    BoneJuiceGlobals.experimentalRegistered = False

def register():
    bpy.utils.register_class(BoneJuicePreferences)
    for item in BINDINGS:
        registerClass(item[0], item[1], item[2])
    if getPreferences(bpy.context).enableExperimental:
        registerExperimental()
    if getPreferences(bpy.context).enableLuchadores:
        registerLuchadoresHelper()
    for item in MENUBINDINGS:
        registerMenu(item[0], item[1], item[2])

def unregister():
    for item in MENUBINDINGS:
        unregisterMenu(item[0], item[1], item[2])
    for item in BINDINGS:
        unregisterClass(item[0], item[1], item[2])
    if BoneJuiceGlobals.experimentalRegistered:
        unregisterExperimental()
    if BoneJuiceGlobals.luchadoresRegistered:
        unregisterLuchadoresHelper()
    bpy.utils.unregister_class(BoneJuicePreferences)

if __name__ == "__main__":
    register()
