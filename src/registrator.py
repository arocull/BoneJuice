from typing import List
import bpy

def registerClass(classType, toolContexts: List = [bpy.types.VIEW3D_MT_select_object], buttons: List = []):
    """Registers a class, its manual map, and buttons for it using the given list of menus"""
    bpy.utils.register_class(classType)
    bpy.utils.register_manual_map(classType.manual_map)

    for i in range(0, len(toolContexts)):
        but = classType.button # Default to button function
        if len(buttons) > 0: # ..unless we were given a list
            but = buttons[i]
        
        toolContexts[i].append(but)

def unregisterClass(classType, toolContexts: List = [bpy.types.VIEW3D_MT_select_object], buttons: List = []):
    """Unregisters a class, its manual map, and buttons for it using the given list of menus"""
    bpy.utils.unregister_class(classType)
    bpy.utils.unregister_manual_map(classType.manual_map)

    for i in range(0, len(toolContexts)):
        but = classType.button # Default to button function
        if len(buttons) > 0: # ..unless we were given a list
            but = buttons[i]
        
        toolContexts[i].remove(but)

def registerMenu(classType, drawFunc, toolContexts: List = []):
    bpy.utils.register_class(classType)
    for cont in toolContexts:
        cont.append(drawFunc)
def unregisterMenu(classType, drawFunc, toolContexts: List = []):
    for cont in toolContexts:
        cont.remove(drawFunc)
    bpy.utils.unregister_class(classType)
