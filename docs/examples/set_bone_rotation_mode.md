# Set Bone Rotation Mode
Firstly, note that Blender has a built-in version of this tool called `Pose > Convert Rotation Modes` and it does the exact same thing but better.
I just did not see it until after I programmed this (whoops!).

In Pose mode, select the bones you want to edit, then go to `Pose > Set Rotation Mode`. Choose the rotation mode you want, and all selected pose bones will be set to the new rotation mode.

## Limitations
Note that if the bones already have a keyframed rotation, these keyframes will not be converted to the new rotation mode, and you may run into issues with rotation channels clashing.