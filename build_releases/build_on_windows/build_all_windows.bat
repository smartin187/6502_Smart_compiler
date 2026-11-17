:: Compile the emulator and compiler:

call build_releases/build_on_windows/build_windows.bat

:: Make zip:

powershell -NoProfile -Command "Compress-Archive -Path 'build_publish\windows\*.exe' -DestinationPath 'build_publish\windows\smartykit-windows-%PROCESSOR_ARCHITECTURE%.zip' -Force"
