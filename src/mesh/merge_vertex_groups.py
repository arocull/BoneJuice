import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty
from bpy.types import Object, Operator, Mesh, VertexGroup
from ..utility import *

class BoneJuice_MergeVertexGroups(Operator):
    """Combine two vertex groups on selected meshes using a given operation."""
    bl_idname = "bj.merge_vert_groups"
    bl_label = "Merge Vertex Groups"
    bl_description = "Combine two vertex groups on selected meshes using a given operation."
    bl_options = {'REGISTER', 'UNDO'}

        ## MAPPING
    def button(self, context):
        self.layout.operator(
            BoneJuice_MergeVertexGroups.bl_idname,
            text="Merge Vertex Groups",
            icon='NONE')

    def manual_map():
        url_manual_prefix = "https://github.com/arocull/BoneJuice/"
        url_manual_mapping = (
            ("bpy.ops.bj.merge_vert_groups", "blob/master/docs/examples/merge_vertex_groups.md"),
        )
        return url_manual_prefix, url_manual_mapping

    ## PROPERTIES
    groupAName: StringProperty(
        name = "Group A",
        description = "The name of the first vertex group to be used in the operation.",
        default = "Group",
    )
    groupBName: StringProperty(
        name = "Group B",
        description = "The name of the second vertex group to be used in the operation.",
        default = "Group.001",
    )
    groupCName: StringProperty(
        name = "Output Group",
        description = "The name of the vertex group to be outputted to. Will create one if not currently present.",
        default = "merged_group",
    )
    groupOperation: EnumProperty(
        name = 'Operation',
        description = 'What operation to use for the formula.',
        items = [
            ('add', 'Add', 'A + B = C'),
            ('subtract', 'Subtract', 'A - B = C'),
            ('multiply', 'Multiply', 'A * B = C'),
            ('divide', 'Divide', 'A / B = C'),
            ('modulus', 'Modulus', 'A % B = C'),
            ('pow', 'Power', 'A ^ B = C'),
            ('min', 'Minimum', 'min(A, B) = C'),
            ('max', 'Maximum', 'max(A, B) = C'),
        ],
        default = 'add',
    )
    useConstant: EnumProperty(
        name = 'Use Constant',
        description = 'Utilizes the provided constant in place of the given group.',
        items = [
            ('no', 'No', 'Does not use the constant value.'),
            ('b', 'For B', 'Use constant in place of vertex group B'),
            ('a', 'For A', 'Use constant in place of vertex group A'),
        ],
        default = 'no',
    )
    operationConstant: FloatProperty(
        name = 'Constant',
        description = 'Numberic value to use in place of B, if Use Constant is checked.',
        default = 0
    )


    ## functions
    def runOperation(self, a: float, b: float) -> float:
        match self.groupOperation:
            case 'subtract':
                return a - b
            case 'multiply':
                return a * b
            case 'divide':
                if (b == 0): # Approach infinity
                    if (a == 0): # Unless we're also zero
                        return 0
                    return 1
                return a / b
            case 'modulus':
                return a % b
            case 'pow':
                return pow(a, b)
            case 'min':
                return min(a, b)
            case 'max':
                return max(a, b)
            case _:
                return a + b
    def getVertexGroup(self, obj: bpy.types.Object, grpName: str) -> VertexGroup:
        return obj.vertex_groups.get(grpName)
    
    ## INVOKE DIALOGUE
    def invoke(self, context: bpy.types.Context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    ## ACTUAL EXECUTION
    def execute(self, context: bpy.types.Context):
        primary = get_active() # Fetch primary object
        objects = bpy.context.selected_objects # Fetch selected objects
        
        # Iterate through all objects so we can work on the meshes
        for obj in objects:
            set_active(obj) # Set current object as active
            if type(get_active().data) is Mesh:

                # First, get vertex groups and make sure everything is in order!
                groupA: VertexGroup = None
                groupB: VertexGroup = None
                groupC: VertexGroup = self.getVertexGroup(obj, self.groupCName)

                # If we're not using a constant for group a, fetch it
                if self.useConstant != 'a':
                    groupA = self.getVertexGroup(obj, self.groupAName)
                    if not groupA:
                        self.report({'WARNING'}, "Could not find vertex group '" + self.groupAName + "' on mesh '" + obj.name + "' Skipping.")
                        break
                if self.useConstant != 'b':
                    groupB = self.getVertexGroup(obj, self.groupBName)
                    if not groupB:
                        self.report({'WARNING'}, "Could not find vertex group '" + self.groupBName + "' on mesh '" + obj.name + "'. Skipping.")
                        break
                
                if not groupC:
                    groupC = bpy.context.active_object.vertex_groups.new(name=self.groupCName)

                # Then fetch total vertices
                numVerts = len(obj.data.vertices)
                vertIndices: List[int] = []
                vertWeightsA: List[float] = []
                vertWeightsB: List[float] = []
                # Fill in indices and weights
                for i in range(0, numVerts):
                    vertIndices.append(i)

                    # Append A weights
                    if groupA:
                        try: # Attempt to append the weight of the given vertex if it exists in the group
                            vertWeightsA.append(groupA.weight(i))
                        except: # If it isn't present, just append zero instead
                            vertWeightsA.append(0)
                    else:
                        vertWeightsA.append(self.operationConstant)
                    
                    # Append B weights
                    if groupB:
                        try: # Attempt to append the weight of the given vertex if it exists in the group
                            vertWeightsB.append(groupB.weight(i))
                        except: # If it isn't present, just append zero instead
                            vertWeightsB.append(0)
                    else:
                        vertWeightsB.append(self.operationConstant)
                
                # Finally, perform operation and add vertices with weights > 0 to the array
                for i in range(0, numVerts):
                    result: float = clampf(self.runOperation(vertWeightsA[i], vertWeightsB[i]), 0, 1)
                    if (result > 0):
                        groupC.add([i], result, 'REPLACE')
                    else:
                        groupC.remove([i])

                self.report({'INFO'}, "Completed operation for mesh object '" + obj.name + "'.")

        set_active(primary) # Re-select primary object

        return {'FINISHED'}
