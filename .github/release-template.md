| OS \ Arch | x64 (AMD64) | ARM64 |
|-----------------------|-----|-------|
| Linux (Debian/Ubuntu) | `smart-compiler-emulator_x.x_Linux-amd64.deb` | `smart-compiler-emulator_x.x_Linux-arm64.deb` |
| Linux (other) | `Smart_Linux-amd64.zip` | `Smart_Linux-arm64.zip` |
| Windows | `smart-windows-AMD64.zip` | _Not supported_ ; use [`other platforms`](#for-other-platforms) |
| [Other platforms](#for-other-platforms) | Source code (zip) ; use python 3.13 for run. | Source code (zip) ; use python 3.13 for run. |

## For `Other platforms`

1) Get the source code. Download the source code (as zip file or do a git clone).
2) Extract the zip file (skip this step if you did a git clone).
3) Install Python 3.13 (or higher).
4) You can run Smart:

**For run the compiler:**
```bash
python main.py --help
python main.py your_program.sma
```

**For run the emulator:**
```bash
python smart_emulator.py --help
python smart_emulator.py # Open the GUI
python smart_emulator.py your_program.sma
```

5) Optional: if you need the Smart libraries:
    - On the zip file or on the clone, find the `smart_lib` folder.
    - If your OS is supported by Smart (Linux or Windows), copy the `smart_lib` to the path of library. You know the path with:
```bash
python main.py --show-lib-path
```
Copy the `smart_lib` to the path.
If your OS is not supported by Smart, you can't use the path of library, but for use the library, copy the `smart_lib` folder in any path, and for import a library, use the absolute path of the library.