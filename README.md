# BoneJuice
Armature utility plugin for Blender, for niche cases I encounter where it would be a lot nicer to have something do the work for me!

Version 0.0.8 which supports Blender 3.2+

Feature List (click on the links to see how-to/examples):
- Object Mode
    - **[Clean and Combine](docs/examples/clean_and_combine.md)** - Combine multiple meshes, with modifiers, into one export-ready object. Armatures are preserved.
    - **[Merge/Operate Vertex Groups](docs/examples/merge_vertex_groups.md)** - Run a math operation on one or two vertex groups. Also available in Weight Paint mode.
- Armature Edit Mode
    - **[Add Bone Circle](docs/examples/add_bone_circle.md)** - Creates a circle of bones around an active bone, with rolls adjusted to face it
    - **[Add Leaf Bones](docs/examples/add_leaf_bones.md)** - Add leaf bones to an armature for external purposes
    - **[Select End Bones](docs/examples/select_end_bones.md)** - Select bones at the bottom of the hiearchy
    - **[Surface Bone Placer](docs/examples/surface_bone_placer.md)** - Place bones on geometric surfaces with a single click
    - **[Mark Bone Side](docs/examples/mark_bone_side.md)** - Mark bones as left or right in an armature. Alternative to built-in method which relies on specific rules.
- Armature Pose Mode
    - **[Set Rotation Mode](docs/examples/set_bone_rotation_mode.md)** - Select multiple pose bones and set their rotation mode (Quaternion, XYZ Euler, Axis Angle, etc) with just the click of a button. Alternative to built-in method which can be hit-or-miss (although this will not convert keyframed transforms).
    - **[Curl Bones](docs/examples/curl_bones.md)** - Offsets euler rotations of all selected pose bones by the given rotation. Currently only works in Euler rotation mode.
    - **[Flip IK Limits](docs/examples/flip_ik_limits.md)** - Flips the minimum and maximum IK limit of a specified axis for all selected bones.
- Rendering
    - **(Work In Progress) Batch Render NLA Tracks** - Individually render out each animated NLA track inside of all selected objects. Renders from all selected cameras. Great for game animation previews or spritesheets.

# Installation
Download the zip file from the releases area on GitHub, and then go to `Edit > Preferences > Add-ons` and then click `Install` in the top right, and select the zip file. Make sure the plugin it points to is enabled.

If you want the latest version, use `$ make` (Linux-only) inside in this folder to get a zip file, or simply zip up the `src` folder and install that instead.

# Development
This plugin is developed using a custom environment in VS Code. I reccomend using the workspace settings and reccomended extensions.

When setting up, be sure to clone the Blender Python Autocomplete if you use the workspace settings (run inside this repository):
- `$ git clone https://github.com/Korchy/blender_autocomplete.git`

I also highly recommend these VS Code workspace extensions for editing this project.
- jacqueslucke.blender-development
- blenderfreetimeprojects.blender-python-code-templates

The Blender Development plugin is really helpful with it's built-in debugger. Press F1, and run `>Blender: Build and Start` to debug. The workspace configuration should be set up for you already.

If the debugger is failing to install modules, you may check out this thread [here](https://github.com/JacquesLucke/blender_vscode/issues/99) (I had to run `/home/usrname/.../blender-3.1.0-linux-x64/3.1/python/bin/python3.10 -m ensurepip` before I could use the debugger in Blender 3.1).