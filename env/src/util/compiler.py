import os
import shutil
import subprocess
from .binary_type import BinaryType
from . import color
from .platform import Platform

def init() -> bool: return Globals.init()
class Globals:
    objectsPath: str

    @staticmethod
    def init() -> bool:
        Globals.objectsPath = "objects"

        if os.path.exists(Globals.objectsPath):
            shutil.rmtree(Globals.objectsPath)

        os.mkdir(Globals.objectsPath)
        return True

def compile(src: str, flags: list[str] = None) -> bool:
    if not os.path.exists(src):
        print(f"{color.makeRed("Error")}: source '{src}' does not exist!")
        return False

    if os.path.isdir(src):
        print(f"{color.makeRed("Error")}: source '{src}' is a directory?")
        return False

    procArgs: list[str] = [
        "clang++",
        "-c",
        src,
        "-o",
        f"{Globals.objectsPath}/{os.path.basename(src)[:-3]}o",
        *flags,
    ]

    print(f"Compiling '{src}'...", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run(procArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True

def _makeLibList(libs: dict) -> list[str]:
    if libs == None: return []
    return ["-l:" + lib for lib in libs[Platform.getString()]]

def _execArgs (
        binaryDirectory: str,
        dynamicLibraries: dict,
        staticLibraries: dict,
        objectFiles: list[str],
        binName: str,
        flags: list[str]
) -> list[str]: return [
    "clang++",
    f"-L{binaryDirectory}",
    *_makeLibList(dynamicLibraries),
    *_makeLibList(staticLibraries),
    *objectFiles,
    "-o",
    f"{binaryDirectory}/{binName}{Platform.getExecutableBinaryExtension()}",
    *flags
]

def _dynamicArgs (
    binaryDirectory: str,
    staticLibraries: dict,
    objectFiles: list[str],
    binName: str,
    flags: list[str]
) -> list[str]: return []

def _staticArgs (
    binaryDirectory: str,
    staticLibraries: dict,
    objectFiles: list[str],
    binName: str,
    flags: list[str]
) -> list[str]: return []

def linkBinary (
        binaryDirectory: str,
        binaryName: str,
        binaryType: BinaryType,
        flags: list[str] = None,
        dynamicLibraries: dict = None,
        staticLibraries: dict = None
) -> bool:
    print(f"Linking into {Platform.getBinaryExtensionString(binaryType)} binary..", end="")

    if not os.path.exists(binaryDirectory):
        print(f" {color.makeRed("Failure")}: output directory '{binaryDirectory}' does not exist?")
        return False

    objects: list[str] = []
    for obj in os.listdir(Globals.objectsPath):
        objects.append(f"{Globals.objectsPath}/{obj}")

    procArgs = _execArgs (
        binaryDirectory,
        dynamicLibraries,
        staticLibraries,
        objects,
        binaryName,
        flags
    )

    callback: subprocess.CompletedProcess[str] = subprocess.run(procArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True