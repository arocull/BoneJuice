# Add Leaf Bones
Creates leaf bones at the end of all currently selected bones. Useful for ensuring compatability with other programs outside of export formats.

## Accessing
While editing an Armature, go to `Add > Add Leaf Bones`.

## Use
Select the bones you want to add leaf bones to, and then run the operator.

## Example - Adding Leaf Bones
Select the root bone of your armature in Edit mode.

![](../images/exmp_selectendbones1.png)

Then run `Select > Select End Bones`--this should select all the outermost bones of your model.
If you use "Ignore Non-Deforming," it should not grab IK handles if you marked them properly! 

![](../images/exmp_selectendbones2.png)

Afterward, run `Add > Add Leaf Bones`. Leaf bones will automatically be placed on these end bones, and selected.

![](../images/exmp_addleafbones1.png)

Finally, run `Armature > Change Bone Layers` and select a new layer to hide the Leaf Bones while you continue working in Blender.

![](../images/exmp_addleafbones2.png)