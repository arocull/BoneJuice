# Reduce Rig

Reduces an annotated rig to deform-bones only. Ideal for optimizing a rig for games, though may require some retargetting.

**Make a copy or backup of your rig before using. This tool utilizes a destructive workflow.**

## Accessing
While in Object Mode, go to `Object > Clean Up > Reduce Rig`.

## Problem Statement
Because Rigify is intended for animation, not all deform bones are related to each other. Inside Blender this is fine, but if you want to minimize the amount of necessary bones for exporting to a game engine (so you, say, only export deformation bones), the bone hiearchy becomes messy, resulting in poor animation blending results as seen below.

![](../images/exmp_reducerig4.png)

To resolve this, we need to put all deformation bones into a proper hiearchy before exporting, then retarget our animations from the actual Rigify rig to our new one.

## Use
Remove all non-deforming bones from a rigify rig to minimize bone count, while fixing the bone hiearchy to allow for proper animation blending.

First, make your armature active.

![](../images/exmp_reducerig1.png)

Then, run Reduce Rig on it.

![](../images/exmp_reducerig2.png)

This should remove all deformation bones, reset our bone layers, and clear our animation contraints (depending on the settings you used). Even the bone parents were set up for us--though modification will be needed in edge cases.

![](../images/exmp_reducerig3.png)

We now have a clean, optimized, and properly-hiearched armature for exporting to game engines (with 174 bones instead of 933), while keeping the bone names and placements the exact same (thus deforming the same!).

Animation retargeting can be used to properly export animations for this new rig. **Process is still yet to be determined.**
