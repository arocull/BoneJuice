import bpy
from bpy.props import IntProperty, StringProperty, BoolProperty, FloatProperty
from bpy.types import Armature, EditBone, Operator, Curve

class BoneJuice_SplineFromCurve(Operator):
    """Generates an IK spline from the selected curve and active rig."""
    bl_idname = "bj.spline_from_curve"
    bl_label = "IK Spline from Curve"
    bl_description = "Generates an IK spline from the selected curve and active rig"
    bl_options = {'REGISTER', 'UNDO'}

    ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_SplineFromCurve.bl_idname,
            text=BoneJuice_SplineFromCurve.bl_label,
            icon='NONE')
    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops."+BoneJuice_SplineFromCurve.bl_idname, "scene_layout/object/types.html"),
        )
        return url_manual_prefix, url_manual_mapping
    
    ## PROPERTIES ##
    boneName: StringProperty(
        name = "Name",
        description = "Name of the created bones. # will be replaced with the index",
        default = "spline#",
    )
    useDeform: BoolProperty(
        name = "Use Deform",
        description = "If true, the Spline bones are marked to deform. False otherwise",
        default = True,
    )
    generateControls: BoolProperty(
        name = "Generate Controls",
        description = "If true, generates control points along the spline annotated for Rigify",
        default = False,
    )
    ctrlboneName: StringProperty(
        name = "Control Name",
        description = "Name of the created control bones. # will be replaced with the index",
        default = "splinectrl#",
    )
    ctrlLength: FloatProperty(
        name = "Control Length",
        description = "Length of the control bones",
        default = 0.1,
        min = 0,
        soft_min = 0.05,
        soft_max = 1,
        unit = 'LENGTH',
    )
    doHooks: BoolProperty(
        name = "Attach Hooks",
        description = "If true, automatically attach curve hooks to the generated control bones",
        default = True,
    )

    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: bpy.context):
        layout = self.layout
        col = layout.column()

        col.prop(self, "boneName")
        col.prop(self, "useDeform")
        col.prop(self, "generateControls")
        if self.generateControls:
            col.label(text="Control Settings")
            col.prop(self, "ctrlboneName")
            col.prop(self, "ctrlLength")
            col.prop(self, "doHooks")

    def bonespline_from_curve(self, curve_object: bpy.types.Object, spline: bpy.types.Spline):
        armature = bpy.context.active_object
        armData: Armature = armature.data
        bpy.ops.object.mode_set(mode='EDIT') # Enter into edit mode
        bpy.ops.armature.select_all(action='DESELECT')
        
        isBezier: bool = not spline.bezier_points == None
        pts = None#: bpy.types.SplinePoints | bpy.types.SplineBezierPoints = None
        if isBezier:
            pts = spline.bezier_points
        else:
            pts = spline.points
        numpts: int = len(pts)

        lastBone: EditBone = bpy.context.active_bone
        lastBoneName: str
        ctrlNames: list[str] = []

        for i in range(numpts):
            # Convert relative coordinates to world coordinates
            startPos = curve_object.matrix_world @ pts[(i-1)%numpts].co
            endPos = curve_object.matrix_world @ pts[i].co
            
            # Generate spline/deform bone
            boneName: str = str(self.boneName).replace('#', str(i))
            lastBoneName = boneName
            circleBone: EditBone = armature.data.edit_bones.new(boneName)
            circleBone.parent = lastBone
            lastBone = circleBone

            circleBone.use_deform = self.useDeform
            circleBone.use_connect = i > 0
            circleBone.head = startPos
            circleBone.tail = endPos

            if self.generateControls:
                boneName = str(self.ctrlboneName).replace('#', str(i))
                controlBone: EditBone = armature.data.edit_bones.new(boneName)
                controlBone.parent = bpy.context.active_bone
                controlBone.head = startPos
                controlBone.tail = startPos + (lastBone.z_axis * self.ctrlLength)
                controlBone.use_deform = False
                ctrlNames.append(boneName)

        if self.generateControls:
            if self.doHooks:
                # NOW, exit into Object Mode, then Edit the Curve
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.objects.active = curve_object
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.curve.select_all(action='DESELECT')

                for i, point in enumerate(spline.bezier_points):
                    m = curve_object.modifiers.new(name='BJ Spline Hook', type='HOOK')
                    m.center = point.co
                    m.vertex_indices_set([i*3, i*3+1, i*3+2])  # left handle, point, right handle?
                    bpy.context.evaluated_depsgraph_get() # magic spell
                    m.object = armature
                    m.subtarget = ctrlNames[(i+1)%numpts]

                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.context.view_layer.objects.active = armature
            bpy.ops.object.mode_set(mode='POSE')

            # Set up rigify properties for all control bones
            # ...use try-catch in case Rigify isn't enabled
            try:
                for i in range(numpts):
                    b = armature.pose.bones[ctrlNames[i]]
                    b.rigify_type = 'basic.raw_copy'
                    b.rigify_parameters.optional_widget_type = 'sphere'
            except AttributeError: # Rigify was not enabled, fail encoding
                pass
        else:
            bpy.ops.object.mode_set(mode='POSE')

        # Get end of chain
        splineStart: bpy.types.PoseBone = armature.pose.bones.get(lastBoneName)
        c = splineStart.constraints.new(type='SPLINE_IK')
        c.target = curve_object
        c.chain_count = numpts
        bpy.ops.object.mode_set(mode='EDIT')


    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        armatureObj = bpy.context.active_object
        editArmature: Armature
        if type(armatureObj.data) is Armature:
            editArmature = armatureObj.data
        else:
            self.report({'WARNING'}, "Active object is not an armature!")
            return {'FINISHED'}
        
        for obj in bpy.context.selected_objects:
            if type(obj.data) is Curve:
                curve: Curve = obj.data
                for spline in curve.splines:
                    self.bonespline_from_curve(curve_object=obj, spline=spline)

        if self.generateControls:
            self.report({'WARNING'}, "Active object is not an armature!")
        self.report({'INFO'}, "Generated spline IK.")

        return {'FINISHED'}
