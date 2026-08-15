:: Use this script for build to Windows from Windows
:: A confirmation can be ask you for delete the build_publish folder if it exists

cd ..
cd ..

if exist "build_publish\" (
    echo Deleting build_publish folder
    rmdir /s "build_publish"
)

mkdir build_publish\windows

:: compile main.py
echo Building main.py

pyinstaller --onefile main.py

copy dist\main.exe build_publish\windows\

:: Compile smart_emulator.py

echo Building smart_emulator.py

pyinstaller --onefile smart_emulator.py

copy dist\smart_emulator.exe build_publish\windows\

echo Compilation terminated. Result in build_publish\windows
