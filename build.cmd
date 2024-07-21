cd src
REM "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --command extension validate
"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --command extension build
REM "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --command extension validate build/bonejuice-0.1.1.zip
cd ..
move src\*.zip build\