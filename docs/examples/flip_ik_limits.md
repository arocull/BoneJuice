# Flip IK Limits
In Pose mode, select the bones you want to flip, then go to `Pose > Flip IK Limits`.

## Limitations
This tool is currently only designed with basic IK in mind. This does not work for things like position or rotation remap constraints.

## Example - Mirroring an Armature
I completed my rig for the right-side of an armature, but when I ran Symmetrize in Edit Mode, the bones on the armature's right (left in picture) had the wrong IK limits! This means the arm will move awkwardly and backwards when we move our IK goal.

![](../images/exmp_flipiklim1.png)

To fix this, I selected all the bones on the right half of the armature (our left when facing it), then ran `Pose > Flip IK Limits` on the Z axis.

![](../images/exmp_flipiklim2.png)

Now our IK limits are the same!

![](../images/exmp_flipiklim3.png)