import bpy

class SubMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_object_attributes"
    bl_label = "Attributes"

    def draw(self, context):
        layout = self.layout

        layout.operator("geometry.attribute_add", text="Add Attribute")
        layout.operator("geometry.attribute_remove", text="Remove Attribute")
        layout.operator("geometry.attribute_convert", text="Convert Attribute")

        layout.separator()

        # use existing memu
        layout.menu("VIEW3D_MT_transform")


bpy.utils.register_class(SubMenu)

# test call to display immediately.
bpy.ops.wm.call_menu(name="OBJECT_MT_select_submenu")