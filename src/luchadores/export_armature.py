import bpy
import datetime
import json
from idprop.types import IDPropertyArray # UGLY HAX, see 'getBoneDict'
from typing import List
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty, StringProperty
from bpy.types import Bone, IDPropertyWrapPtr, NlaTrack, NlaTracks, Object, Operator, Armature, ArmatureBones
from .boneprops import LUCHADORESBONEPROPDEFAULTS, LUCHADORESBONEPROPS
from ..utility import floatListToDict, floatListToVector, getNlaStripLimits

class BoneJuice_Luchadores_ExportArmature(Operator, ExportHelper):
    """Export the selected armature as a Luchadores armature file."""
    bl_idname = "armature.bj_luchadores_exportarmature"
    bl_label = "Export LuchArmature"
    bl_description = "Export the selected armature as a Luchadores armature file"
    filename_ext: str = ".json"

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_Luchadores_ExportArmature.bl_idname,
            text="Luchadores Armature (.json)",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_Luchadores_ExportArmature.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    filter_glob: StringProperty(
        default="*.json",
        options={'HIDDEN'},
        maxlen=255,
    )
    limitToSelected: BoolProperty(
        name="Selected Tracks Only",
        description="If true, will only export the selected NLA animation tracks on this armature, instead of all of them.",
        default=False,
    )

    def err(self, errorOut: str):
        self.report({'WARNING'}, errorOut)
        return {'FINISHED'}
    
    def getAnimationData(self, context: bpy.types.Context, armatureObj: Object):
        outAnimations = {}

        if armatureObj.animation_data is None:
            return outAnimations

        tracks: NlaTracks = armatureObj.animation_data.nla_tracks

        for key in tracks.keys():
            track = tracks.get(key)
            if (not self.limitToSelected) or (self.limitToSelected and track.select):
                outAnimations[key] = getAnimationDict(track, context)
        
        return outAnimations

    def execute(self, context: bpy.types.Context):
        obj: Object = context.active_object
        if not obj:
            return self.err("No active Armature to work from!")

        if not type(obj.data) is Armature:
            return self.err("Active object is not an armature!")
        armature: Armature = obj.data
        boneList: ArmatureBones = armature.bones
        rootBone: Bone
        hasRoot: bool = False

        for bone in boneList.values():
            if bone.parent == None:
                if hasRoot:
                    return self.err("Armature has multiple root bones!")
                else:
                    rootBone = bone
                    hasRoot = True

        outObj = {
            "info": {
                "name": obj.name,
                "exported": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") # Log time when this armature was exported
            },
            "tree": None,
            "animations": None,
        }

        armature.pose_position = 'REST'
        outObj["tree"] = getBoneDict(rootBone) # Fill out bone objects
        armature.pose_position = 'POSE'
        outObj["animations"] = self.getAnimationData(context, obj) # Fill with armature animations

        outStr: str = json.dumps(outObj,ensure_ascii=True) # Error outside of file being open, so we don't lock a file down on accident

        f = open(self.filepath, 'w', encoding='utf-8')
        f.write(outStr)
        f.close()

        self.report({'INFO'}, "Successfully wrote file to %s" % self.filepath)
        return {'FINISHED'}


def getBoneDict(bone: Bone) -> dict[str, any]:
    boneData = {
        "name": bone.name,
        "position": floatListToDict(bone.head),
        "length": 0,
        "connected": bone.use_connect,
    }

    for (propKey, default) in zip(LUCHADORESBONEPROPS, LUCHADORESBONEPROPDEFAULTS):
        trimmed: str = propKey[1:len(propKey)] # Remove initial "l" infront of property names
        if propKey in bone:
            val = bone[propKey]

            # UGLY HAX - Tuple properties like colors get converted into this, but we need to re-convert them to a JSON parsable type!
            # Thus, we import an internal file we can't see, and then split up the object accordingly
            # I found the internal file location here https://developer.blender.org/rBbf948b2cef3ba340a6bba5e7bd7f4911c9a9275a
            if type(val) is IDPropertyArray:
                parsable: list = []
                for item in val:
                    parsable.append(item)
                val = parsable

            boneData[trimmed] = val
        else:
            boneData[trimmed] = default

    if bone.parent:
        boneData["length"] = bone.length
    
    if "drawable" in boneData:
        boneData["center"] = floatListToDict(bone.center)
        boneData["center_length"] = floatListToVector(bone.center).length
    
    if len(bone.children) > 0:
        childObjs: List[dict[str, any]] = []

        for childbone in bone.children:
            childObjs.append(getBoneDict(childbone))

        boneData["children"] = childObjs

    return boneData

def getAnimationDict(track: NlaTrack, context: bpy.types.Context) -> dict[str, any]:
    startFrame, endFrame = getNlaStripLimits(track.strips)

    animationData = {
        "fps": context.scene.render.fps,
        "start": startFrame,
        "end": endFrame,
    }

    return animationData