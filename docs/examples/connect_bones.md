# Connect Bones
Connects a tree of disjoint bones by aligning a parent bone's tail with it's children, or vice-versa.

Exported armatures do not include bone ends unless leaf bones are used. If further work is to be done inside Blender, one must clean up the data first, which this tool should aid in the process of.

## Accessing
While editing an Armature, go to `Armature > Connect Bones`.

## Use
Make active the root bone you would like to work off of, and run the operator. The operator will run recursively on all children of the active bone, if specified.

## Example - Imported Rig Cleanup
**Note: This model is not my own. Credit to Blizzard Entertainment who owns the rights to the character. This use for educational purposes only.**

First, make active your root bone.

![](../images/exmp_connect_bones1.png)

Then run `Armature > Connect Bones` to open the operator dialogue. This will perform a basic action for us.

![](../images/exmp_connect_bones2.png)

It looks alright, but the end bones are still tilted sideways! We can patch that up by reversing the operator on the end bones.

![](../images/exmp_connect_bones3.png)

Viola! Our bones orientations are now proper. Note that they may take some adjustment, however.

**TODO: Optionally add leaf bones here instead.**

# Example - Extra Clean
If one is only looking for an armature, you can use the "Reverse" setting instead. However, note that it will shift the origins of your bones up the chain once.

![](../images/exmp_connect_bones4.png)

...which means deforming doesn't feel right!

![](../images/exmp_connect_bones5.png)

**TODO: Propogate bone names down with leaf bones so chain ends up being valid?**