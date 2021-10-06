# BoneJuice
Armature utility plugin for Blender, for niche cases I encounter where it would be a lot nicer to have something do the work for me!

Current features include:
- Surface Bone Placer - Quickly place bones on geometric surfaces
- ...more to come!

# Dependencies
When setting up, be sure to clone the Blender Python Autocomplete if you use the workspace settings (run inside this repository):
- `git clone https://github.com/Korchy/blender_autocomplete.git`

# Tools
## Surface Bone Placer
Currently lacks a button. For now, run using the operator search menu (may be `Tab` or `Spacebar`, then type in "`surface bone placer`"). You might need Python tooltips enabled for this.

Select the Armature you want to work with, then run Surface Bone Placer. If you would like the bones to fall under a parent instead, make the bone you want them to be childs of active (select it with a click).

Once the modal has started, left-click on 3D surfaces to place bones on them. The bone head will fall slightly inside the mesh, and the bone tail will face outward based off the surface normal. Note that the armature must have no transformations for bones to land in the correct spot (may fix later). Parent bone transforms are fine.

When you are finished placing bones, hit `Escape` to exit the modal. When using the placed bones, I recommend using Automatic Weights over Envelope weights for inotial weighting of your mesh.

An example of what it does (made center bone active, then used tool to place bones on surface of mesh):

![](docs/images/exmp_surface_bones.png)