rmdir /s /q build\BoneJuice
xcopy src build\BoneJuice /i /S
cd build\BoneJuice\
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
cd ..
del /q BoneJuice.zip
"C:\Program Files\7-Zip\7z.exe" a -tzip BoneJuice.zip BoneJuice