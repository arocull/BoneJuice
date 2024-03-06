import bpy
from bpy.types import Operator
from bpy.props import StringProperty

class BoneJuice_OperationName(Operator):
    """Operation description."""
    bl_idname = "bj.operation_name"
    bl_label = "Operation Name"
    bl_description = "Operation description"
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_OperationName.bl_idname,
            text=BoneJuice_OperationName.bl_label,
            icon='NONE')
    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_OperationName.bl_idname, "blob/master/README.md"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    exampleVar: StringProperty(
        name = "Example Property",
        description = "Description",
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
