from typing import Dict
from ..utility import getRNA_UI

# Luchadores Bone Properties - A list of custom bone properties utilized in the Luchadores engine
LUCHADORES_BONE_PROPERTIES = {
    "ldrawable": {
        "name":"Drawable",
        "description":"Whether or not this bone should be drawn when rendering the armature in Luchadores engine",
        "default":False,
    },
    "ldrawcolor": {
        "name":"Draw Color",
        "description":"Color to draw for this bone in Luchadores engine",
        "min":0,
        "max":1,
        "subtype":'COLOR',
        "default":(0.0,0.0,0.0),
    },
    "ldrawthickness": {
        "name":"Draw Thickness",
        "description":"Thickness of this bone for drawing in Luchadores engine, in meters",
        "min":0,
        "max":10,
        "unit":'LENGTH',
        "default":0.2,
    },
    "lmassweight": {
        "name":"Mass Weight",
        "description":"Weight value for the amount of mass this bone uses relative to the entire character's mass",
        "min_float":0,
        "max_float":100,
        "use_soft_limits": True,
        "soft_max_float":10,
        "default":1.0,
    }
}

# Copy BPY Property - Creates a new property object, copying attributes from the given template
def copy_bpy_property(dupli: dict) -> Dict:
    return dupli.copy()

# Initialize Bone Properties - Loads default bone properties onto an object if there do not already exist
def initialize_bone_props(obj):
    rna_ui = getRNA_UI(obj)

    for key in LUCHADORES_BONE_PROPERTIES:
        if not hasattr(obj, key): # See if we already have said property
            obj[key] = LUCHADORES_BONE_PROPERTIES[key]['default']
            rna_ui[key] = copy_bpy_property(LUCHADORES_BONE_PROPERTIES[key]) # If not, give us a copy of it