cd src
REM "C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --command extension validate
"C:\Program Files\Blender Foundation\Blender 4.2\blender.exe" --command extension build
cd ..
move src\*.zip build\