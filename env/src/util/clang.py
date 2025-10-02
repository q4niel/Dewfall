import os
import shutil
import subprocess
from enum import Enum
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

class BinaryType(Enum):
    EXECUTABLE = 1
    DYNAMIC = 2
    STATIC = 3

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

def linkBinary (
        binaryDirectory: str,
        binaryName: str,
        binaryType: BinaryType,
        flags: list[str] = None,
        dynamicLibraries: dict = None,
        staticLibraries: dict = None
) -> bool:
    binExt: str = ""
    taskTypeMsg: str = ""
    match binaryType:
        case BinaryType.EXECUTABLE:
            binExt = Platform.getExecutableBinaryExtension()
            taskTypeMsg = "executable"
        case BinaryType.DYNAMIC:
            binExt = Platform.getDynamicBinaryExtension()
            taskTypeMsg = "dynamic"
        case BinaryType.STATIC:
            binExt = Platform.getStaticBinaryExtension()
            taskTypeMsg = "static"

    print(f"Linking into {taskTypeMsg} binary..", end="")

    if not os.path.exists(binaryDirectory):
        print(f" {color.makeRed("Failure")}: output directory '{binaryDirectory}' does not exist?")
        return False

    dynamics: list[str] = []
    if not dynamicLibraries == None:
        dynamics = ["-l:" + bin for bin in dynamicLibraries[Platform.getString()]]

    objects: list[str] = []
    for obj in os.listdir(Globals.objectsPath):
        objects.append(f"{Globals.objectsPath}/{obj}")

    procArgs: list[str] = [
        "clang++",
        f"-L{binaryDirectory}",
        *dynamics,
        *objects,
        "-o",
        f"{binaryDirectory}/{binaryName}{binExt}",
        *flags,
    ]

    callback: subprocess.CompletedProcess[str] = subprocess.run(procArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True