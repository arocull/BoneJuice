import bpy
from bpy.types import Operator, StringProperty

class BoneJuice_OperationName(Operator):
    """Operation description."""
    bl_idname = "object.bj_operation_name"
    bl_label = "Operation Name"
    bl_description = "Operation description."
    bl_options = {'REGISTER', 'UNDO'}

        ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_OperationName.bl_idname,
            text="Operation Name",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.object.bj_operation_name", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    renderPrefix: StringProperty(
        name = "Example Property",
        description = "Description.",
        default = "Default Value",
    )
    
    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        self.report({'WARNING'}, "No functionality set!")
        self.report({'INFO'}, "Completed.")
        return {'FINISHED'}
