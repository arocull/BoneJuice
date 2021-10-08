from typing import List
import bpy

def registerClass(classType, toolContexts: List = [bpy.types.VIEW3D_MT_select_object]):
    """Registers a class, its manual map, and buttons for it using the given list of menus"""
    bpy.utils.register_class(classType)
    bpy.utils.register_manual_map(classType.manual_map)
    for item in toolContexts:
        item.append(classType.button)

def unregisterClass(classType, toolContexts: List = [bpy.types.VIEW3D_MT_select_object]):
    """Unregisters a class, its manual map, and buttons for it using the given list of menus"""
    bpy.utils.unregister_class(classType)
    bpy.utils.unregister_manual_map(classType.manual_map)
    for item in toolContexts:
        item.remove(classType.button)