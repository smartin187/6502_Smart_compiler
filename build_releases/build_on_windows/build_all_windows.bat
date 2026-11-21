:: Compile the emulator and compiler:

call build_releases/build_on_windows/build_windows.bat

:: Make zip:
(
    echo Smart Compiler and Emulator for Windows
    echo Apache License 2.0
    echo See https://github.com/smartin187/6502_Smart_compiler for more information.
) > "README.TXT"

powershell -NoProfile -Command "Compress-Archive -Path 'build_publish\windows\*.exe','README.TXT' -DestinationPath 'build_publish\windows\smart-windows-%PROCESSOR_ARCHITECTURE%.zip' -Force"
