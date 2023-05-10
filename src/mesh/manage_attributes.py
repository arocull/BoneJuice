import bpy
from bpy.types import Operator
from bpy.props import StringProperty

class BoneJuice_BulkEditAttribute(Operator):
    """Edits a geometry attribute for all selected objects."""
    bl_idname = "object.bj_bulk_edit_attribute"
    bl_label = "Bulk Edit Attribute"
    bl_description = "Edits a geometry attribute for all selected objects."
    bl_options = {'REGISTER', 'UNDO'}

        ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_BulkEditAttribute.bl_idname,
            text=BoneJuice_BulkEditAttribute.bl_label,
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            (BoneJuice_BulkEditAttribute.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    attribName: StringProperty(
        name = "Attribute Name",
        description = "Name of the attribute to operate on.",
        default = "UVMap",
    )
    
    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        self.report({'WARNING'}, "No functionality set!")
        self.report({'INFO'}, "Completed.")
        return {'FINISHED'}
