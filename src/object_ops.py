import bpy
from bpy.types import EditBone, GreasePencil, Mesh, Modifier, Object, Operator, Curve
from bpy.props import BoolProperty, EnumProperty, BoolVectorProperty, FloatProperty
from typing import List
from .utility import get_active, set_active

class BoneJuice_CleanAndCombine(Operator):
    """Cleans up modifiers and object data and combines all of the selected objects into the active object"""
    bl_idname = "object.bj_clean_combine"
    bl_label = "Clean and Combine"
    bl_description = "Cleans up modifiers and mesh data and combines all of the selected mesh objects into the active object. THIS WILL CAUSE DATA LOSS and is meant primarly for rapid export processes."
    bl_options = {'REGISTER', 'UNDO'}

    do_join: BoolProperty(
        name = 'Join',
        description = 'If true, automatically joins the objects into the active object.',
        default = True,
    )
    application: EnumProperty(
        name = 'Modifier Application',
        description = 'Helps determine how modifiers are applied. Note that Armatures are never applied nor removed',
        items = [
            ('none', 'None', 'Do nothing with the modifiers. This may cause errors while merging.'),
            ('visible', 'Visible', 'If a modifier is currently visible, apply it. Otherwise, discard it.'),
            ('viewport', 'Viewport', 'Apply modifiers using their viewport settings.'),
            ('render', 'Render', 'Apply modifiers using their render settings. (Only limited render settings are supported.)'),
            ('visible_render', 'Visible Render', 'If a modifier is visible in rendering, apply it. Otherwise, discard it. Applies with render settings. (Only limited render settings are supported.)'),
        ],
        default = 'visible',
    )
    triangulation: EnumProperty(\
        name = 'Triangulation',
        description = 'What polgyons should be triangulated',
        items = [
            ('all', 'All', 'Triangulates the entire mesh after merging'),
            ('ngons', 'N-Gons', 'Triangulates only n-gons on the mesh after merging'),
            ('none', 'None', 'Does not perform triangulation'),
        ],
        default = 'ngons',
    )
    merge_dist: FloatProperty(
        name = 'Vertex Merge Distance',
        description = 'Maximum distance for merging vertices of final mesh',
        min = 0,
        soft_min = 0,
        soft_max = 0.1,
        default = 0.0001,
    )
    delete_loose_geom: BoolProperty(
        name = 'Delete Loose Geometry',
        description = 'If true, deletes loose geometry (vertices and edges) after merging.',
        default = True,
    )

    def button(self, context):
        self.layout.operator(
            BoneJuice_CleanAndCombine.bl_idname,
            text="Clean and Combine",
            icon='MOD_DATA_TRANSFER')

    def manual_map():
        url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
        url_manual_mapping = (
            ("bpy.ops.object.bj_clean_combine", "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping
    
    def step_modifiers(self, context: bpy.types.Context, obj: Object):
        for key in obj.modifiers.keys(): # Get list of modifiers as keys
            mod: Modifier = obj.modifiers[key]

            # If this is an armature, don't apply it nor remove it
            if mod.type == 'ARMATURE':
                continue

            apply: bool = False
            useRender: bool = False

            print(mod.type + ", " + str(mod.show_viewport))

            if self.application == 'visible' and mod.show_viewport:
                apply = True
            elif self.application == 'viewport':
                apply = True
            elif self.application == 'render':
                apply = True
                useRender = True
            elif self.application == 'visible_render' and mod.show_render:
                apply = True
                useRender = True

            if useRender and apply: # Apply Render settings to modifier
                if hasattr(mod, 'render_levels') and hasattr(mod, 'levels'):
                    mod.levels = mod.render_levels

            if apply:
                bpy.ops.object.modifier_apply(modifier=key, report=True)
            else:
                bpy.ops.object.modifier_remove(modifier=key, report=True)

    def execute(self, context: bpy.types.Context):
        objects: List[Object] = bpy.context.selected_objects
        primary: Object = get_active()

        if len(objects) == 0 or primary == None:
            self.report({'WARNING'}, "Must have an active object and at least 1 selected object")
            return {'FINISHED'}

        # Apply modifiers
        if not (self.application == 'none'):
            for obj in objects:
                # Update active object so we apply the correct modifiers
                set_active(obj)

                # Convert curves and grease pencil to Mesh
                objType = type(get_active().data)
                if objType is Curve or objType is GreasePencil:
                    bpy.ops.object.convert(target = 'MESH', keep_original = False)
                    if primary == obj: # Re-select primary if it was a converted curve
                        primary = get_active()
                else: # Don't step modifiers if this was just converted
                    self.step_modifiers(context, obj)
        
        set_active(primary) # Re-set the primary object
        objects = bpy.context.selected_objects # Refetch other objects in case they changed as well
        
        # Join objects
        if self.do_join:
            bpy.ops.object.join()
        
        primary = get_active() # Update primary object just in case its reference changed when merging
        objects = bpy.context.selected_objects # Refetch other objects in case they changed as well
        
        # Perform mesh cleanup, on all objects remaining in selection, just in case they weren't all joined
        for obj in objects:
            set_active(obj) # Set current object as active
            if type(get_active().data) is Mesh:
                bpy.ops.object.mode_set(mode='EDIT') # Enter edit mode

                # Perform triangulation
                if self.triangulation == 'all':
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED',ngon_method='BEAUTY')
                elif self.triangulation == 'ngons':
                    bpy.ops.mesh.select_face_by_sides(number=4,type='GREATER',extend=False)
                    bpy.ops.mesh.quads_convert_to_tris(quad_method='FIXED',ngon_method='BEAUTY')
                
                # Merge nearby vertices
                if self.merge_dist > 0:
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.remove_doubles(threshold=self.merge_dist)
                
                # Remove the remaining geometry
                if self.delete_loose_geom:
                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.ops.mesh.delete_loose(use_verts=True,use_edges=True,use_faces=False)

                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.object.mode_set(mode='OBJECT')

            # Apply object transform
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True, properties=False)

        set_active(primary)
        
        self.report({'INFO'}, "Finished cleaning and merging objects!") # Provide user feedback
        return {'FINISHED'}