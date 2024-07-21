# BoneJuice
Armature utility plugin for Blender, for niche cases I encounter where it would be a lot nicer to have something do the work for me!

Version 1.0.0 which supports Blender 4.2, using the extension system. See **Releases** on sidebar for legacy versions.

Feature List (click on the links to see how-to/examples):
- Object Mode
    - **[Clean and Combine](docs/examples/clean_and_combine.md)** - Combine multiple meshes, with modifiers, into one export-ready object. Armatures are preserved.
    - **[Merge/Operate Vertex Groups](docs/examples/merge_vertex_groups.md)** - Run a math operation on one or two vertex groups. Also available in Weight Paint mode.
- Armature Edit Mode
    - **[Connect Bones](docs/examples/connect_bones.md)** - Quickly clean up imported rigs by reconnecting bones to their children.
    - **[Reduce Rig](docs/examples/reduce_rig.md)** - Reduces a rig to deform-only bones, while patching up the bone hierarchy.
    - **Auto-Parent Bones** - Does exactly as it sounds: attempts to reparent selected bones based on proximity.
    - **Spline from Curve** - Generates Spline IK with optional Bone control points from a curve.
    - **[Add Bone Circle](docs/examples/add_bone_circle.md)** - Creates a circle of bones around an active bone, with rolls adjusted to face it
    - **[Add Leaf Bones](docs/examples/add_leaf_bones.md)** - Add leaf bones to an armature for external purposes
    - **[Select End Bones](docs/examples/select_end_bones.md)** - Select bones at the bottom of the hierarchy
    - **Set Bone Length** - Does exactly as it sounds: sets the length of all selected bones to a set value
    - **[Surface Bone Placer](docs/examples/surface_bone_placer.md)** - Place bones on geometric surfaces with a single click
- Armature Pose Mode
    - **[Flip IK Limits](docs/examples/flip_ik_limits.md)** - Flips the minimum and maximum IK limit of a specified axis for all selected bones.
    - **[Curl Bones](docs/examples/curl_bones.md)** - Offsets Euler rotations of all selected pose bones by the given rotation. Currently only works in Euler rotation mode.
- Animation
    - **Bake All Actions** - Bakes all scene actions for the given armature.

# Installation
Download the zip file from the releases area on GitHub, and then go to `Edit > Preferences > Add-ons` and then click `Install from Disk` in the top right dropdown, and select the zip file. Make sure the plugin it points to is enabled.

If you want the latest version, use `$ make` (Linux-only) inside this folder to get a zip file, or simply zip up the `src` folder and install that instead.

# Development
This plugin is developed using a custom environment in VS Code. I recommend using the workspace settings and recommended extensions.

When setting up, be sure to clone the Blender Python Autocomplete if you use the workspace settings (run inside this repository):
- `$ git clone https://github.com/Korchy/blender_autocomplete.git`

I also highly recommend these VS Code workspace extensions for editing this project.
- `jacqueslucke.blender-development`
- `blenderfreetimeprojects.blender-python-code-templates`

The Blender Development plugin is really helpful with its built-in debugger. Press F1, and run `>Blender: Build and Start` to debug. The workspace configuration should be set up for you already.

### Common Issues
- If the debugger is running into permission issues on setup, you may have installed the addon as a ZIP beforehand. Open Blender and uninstall the addon, before closing Blender and re-attempting the debugging process.
- If the debugger is failing to install modules, you may check out this thread [here](https://github.com/JacquesLucke/blender_vscode/issues/99)
    - In Blender 3.1 on Linux, `/home/usrname/.../blender-3.1.0-linux-x64/3.1/python/bin/python3.10 -m ensurepip`
    - In Blender 3.6 and 4.1 on Windows, I had to run `python.exe -m pip install debugpy` in `C:\Program Files\Blender Foundation\Blender X.X\X.X\python\bin`
