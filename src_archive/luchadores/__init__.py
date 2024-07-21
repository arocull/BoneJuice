import bpy
from .annotate_bones import BoneJuice_Luchadores_CopyBoneProps
from .boneprops import define_bone_props, Luchadores_BonePanel
from .export_armature import BoneJuice_Luchadores_ExportArmature
from ..registrator import registerClass, unregisterClass

def registerLuchadores():
    define_bone_props()

    bpy.utils.register_class(Luchadores_BonePanel)
    registerClass(BoneJuice_Luchadores_ExportArmature, [bpy.types.TOPBAR_MT_file_export])
    registerClass(BoneJuice_Luchadores_CopyBoneProps, [bpy.types.VIEW3D_MT_pose])

    print("LUCHADORES registered")

def unregisterLuchadores():
    bpy.utils.unregister_class(Luchadores_BonePanel)
    unregisterClass(BoneJuice_Luchadores_ExportArmature, [bpy.types.TOPBAR_MT_file_export])
    unregisterClass(BoneJuice_Luchadores_CopyBoneProps, [bpy.types.VIEW3D_MT_pose])

    print("LUCHADORES unregistered")