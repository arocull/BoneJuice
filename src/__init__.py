bl_info = {
    "name" : "BoneJuice",
    "author" : "Alan O'Cull",
    "description" : "Armature Utility Plugin for Blender",
    "blender" : (2, 93, 0),
    "version" : (0, 0, 1),
    "location" : "3D View",
    "warning" : "Somewhat experimental",
    "category" : "3D View"
}

import bpy
from .bones import BoneJuice_SurfacePlacer

def register():
    bpy.utils.register_class(BoneJuice_SurfacePlacer)
    pass

def unregister():
    bpy.utils.unregister_class(BoneJuice_SurfacePlacer)
    pass

if __name__ == "__main__":
    register()