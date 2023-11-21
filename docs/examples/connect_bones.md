# Connect Bones
Connects a tree of disjoint bones by aligning a parent bone's tail with it's children, or vice-versa.

Exported armatures do not include bone ends unless leaf bones are used. If further work is to be done inside Blender, one must clean up the data first, which this tool should aid in the process of.

## Accessing
While editing an Armature, go to `Armature > Connect Bones`.

## Use
Make active the root bone you would like to work off of, and run the operator. The operator will run recursively on all children of the active bone, if specified.

## Example - Imported Rig Cleanup
WIP. For now, see the [example](https://alanocull.com/assets/tools/bj_connect_bones_full.mp4) on my website.

# Example - Connect Two Bones
If a bone only has one child, you can connect the tail of a bone to its child instantly.

![](../images/exmp_connect_bones5.png)

![](../images/exmp_connect_bones6.png)


# Example - Rig Only
If one is only looking for an armature and doesn't care about the skinned mesh, you can use the "Reverse" setting instead for an extra-clean rig. However, note that it will shift the origins of all your bones up the chain by one.

![](../images/exmp_connect_bones7.png)

You can use [add leaf bones](docs\examples\add_leaf_bones.md) to fill-in the bones that disappeared.
