__author__ = 'MpX'
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"includes": [], "packages": ["lxml._elementpath", "lxml"], "excludes": ["urllib.urlopen", "UserDict", "_posixsubprocess", "sets", "urllib.urlencode", "urlparse"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "AVITO Simple Parser",
        version = "0.1",
        description = "My GUI application!",
        #options = {"build_exe": build_exe_options},
        options = {"build_exe": build_exe_options},
        #options = {"path": "C:/Users/MpX/PycharmProjects/AVITOParser"},
        executables = [Executable("main.py", base=base)])