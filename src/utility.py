import bpy
from bpy_extras import view3d_utils
from bpy_types import AddonPreferences
from mathutils import Vector, Matrix
from typing import List, Dict
from bpy.types import NlaStrips, NlaTrack

# Raycast - Taken and modified from Blender's view3d_raycast modal template 
def raycast(context, event, filter: str) -> tuple[any, Vector, Vector, int]:
    """Raycasts in the 3D view toward the current mouse position, then returns collided object, position, normal, and face index"""
    # get the context arguments
    scene = context.scene
    region = context.region
    rv3d = context.region_data
    coord = event.mouse_region_x, event.mouse_region_y

    # get the ray from the viewport and mouse
    view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)

    ray_target = ray_origin + view_vector

    def visible_objects_and_duplis():
        """Loop over (object, matrix) pairs (mesh only)"""

        depsgraph = context.evaluated_depsgraph_get()
        for dup in depsgraph.object_instances:
            if dup.is_instance:  # Real dupli instance
                obj = dup.instance_object
                yield (obj, dup.matrix_world.copy())
            else:  # Usual object
                obj = dup.object
                yield (obj, obj.matrix_world.copy())

    def obj_ray_cast(obj, matrix):
        """Wrapper for ray casting that moves the ray into object space"""

        # get the ray relative to the object
        matrix_inv = matrix.inverted()
        ray_origin_obj = matrix_inv @ ray_origin
        ray_target_obj = matrix_inv @ ray_target
        ray_direction_obj = ray_target_obj - ray_origin_obj

        # cast the ray
        success, location, normal, face_index = obj.ray_cast(ray_origin_obj, ray_direction_obj)

        if success:
            return location, normal, face_index
        else:
            return None, None, None

    # cast rays and find the closest object
    best_length_squared = -1.0
    best_obj = None
    hitPosition = Vector((0.0,0.0,0.0))
    hitNormal = Vector((0.0,0.0,1.0))
    hitFaceIndex = 0

    # For all visible and duplicate objects
    for obj, matrix in visible_objects_and_duplis():
        # IF it's a mesh, has mesh data, and the string filter is not inside the object name...
        if obj.type == 'MESH' and len(obj.data.vertices) > 0 and filter not in obj.name:
            hit, normal, face_index = obj_ray_cast(obj, matrix)
            if hit is not None:
                hit_world = matrix @ hit
                length_squared = (hit_world - ray_origin).length_squared
                if best_obj is None or length_squared < best_length_squared:
                    best_length_squared = length_squared
                    best_obj = obj

                    # Update hit data
                    hitPosition = hit_world
                    hitNormal = normal
                    hitFaceIndex = face_index
    
    # If we hit an object, use that
    if best_obj is not None:
        #scene.cursor.location = hitPosition
        return best_obj.original, hitPosition, hitNormal, hitFaceIndex
    
    # If view vector is orthographic and horizontal, just take ray origin
    if abs(view_vector.z) <= 0.001:
        hitPosition = ray_origin
        return None, hitPosition, -view_vector, 0

    # If not, snap to origin
    hitPosition = ray_origin - view_vector * (ray_origin.z / view_vector.z)
    #scene.cursor.location = hitPosition
    return None, hitPosition, Vector((0.0, 0.0, 1.0)), 0 # Normal vector should always point up

def dist(posA: Vector, posB: Vector) -> float:
    """Returns the Euclidean distance between two points."""
    return (posA - posB).length

def dist_threshold(posA: Vector, posB: Vector, threshold: float = 1.0) -> bool:
    """Returns true if the Euclidean distance between two points is less than the threshold. False otherwise."""
    return dist(posA, posB) < threshold

def get_active() -> bpy.types.Object:
    """Gets the active Object"""
    return bpy.context.object

def set_active(obj: bpy.types.Object):
    """Sets the active Object, use None to deselect"""
    bpy.context.view_layer.objects.active = obj

def get_active_bone() -> bpy.types.EditBone:
    """Gets the active Edit Bone"""
    return bpy.context.active_bone

def vect_to_string(v: Vector) -> str:
    """Converts a 3D vector to a string separated by commas"""
    return str(v.x) + ", " + str(v.y) + ", " + str(v.z)

def invert_matrix_stack(mats: List[Matrix]) -> List[Matrix]:
    newMatArray: List[Matrix] = []
    
    for mat in mats:
        newMatArray.append(mat.inverted())
    
    newMatArray.reverse()
    return newMatArray

def NlaDictList_append(renderTracks: Dict[str, List[NlaTrack]], key: str, track: NlaTrack):
    """Append a given NLA track to a list of NLA tracks that fall under a given string key."""
    if hasattr(renderTracks, key):
        renderTracks[key].append(track)
    else:
        renderTracks[key] = [track]

def isCollection(self, obj):
    """Returns true if the given object is a collection."""
    if not obj is bpy.types.Collection:
        return False
    return True

def clampf(num: float, min: float, max: float) -> float:
    return min if num < min else max if num > max else num

def lerpVector(a: Vector, b: Vector, alpha: float) -> Vector:
    return (a * (1 - alpha)) + (b * alpha)

def getPreferences(context: bpy.types.Context) -> AddonPreferences:
    print(context.preferences.addons)
    return context.preferences.addons[__package__].preferences

def vectorToFloatList(inp: Vector) -> List[float]:
    return [inp.x, inp.y, inp.z]

def floatListToVector(inp: List[float]) -> Vector:
    return Vector((inp[0], inp[1], inp[2]))

def floatListToDict(inp: List[float]) -> dict[str, float]:
    return {
        "x": inp[0],
        "y": inp[1],
        "z": inp[2],
    }

def getNlaStripLimits(strips: NlaStrips):
    animFrameStart = 1
    animFrameEnd: int = 1

    for strip in strips:
        if strip.frame_end > animFrameEnd:
            animFrameEnd = strip.frame_end
        if strip.frame_start < animFrameStart:
            animFrameStart = strip.frame_start
    
    return animFrameStart, animFrameEnd

def getRNA_UI(obj):
    rna_ui = obj.get('_RNA_UI')
    if rna_ui is None:
        obj['_RNA_UI'] = {}
        rna_ui = obj['_RNA_UI']
    
    return rna_ui

def fill_layers_array(state: bool = False, size: int = 32) -> list[bool]:
    """Returns an array of booleans of the given state and size"""
    bools = list[bool]()
    for _ in range(0, size):
        bools.append(state)
    return bools

def share_layers_array(a: list[bool], b: list[bool]) -> bool:
    """Checks if two arrays of bools are both true at any given index"""
    for i in range(0, min(len(a), len(b))):
        if a[i] and b[i]: # If the same index is true on both layers, return true
            return True
    return False
