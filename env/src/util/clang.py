import os
import shutil
import subprocess
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

    clangArgs: list[str] = [
        "clang++",
        *flags,
        "-c",
        src,
        "-o",
        f"{Globals.objectsPath}/{os.path.basename(src)[:-3]}o"
    ]

    print(f"Compiling '{src}'...", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run(clangArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True

def linkExec(binaryDirectory: str, binaryName: str, flags: list[str] = None) -> bool:
    print(f"Linking into executable binary..", end="")

    if not os.path.exists(binaryDirectory):
        print(f" {color.makeRed("Failure")}: output directory '{binaryDirectory}' does not exist?")
        return False

    objects: list[str] = []
    for obj in os.listdir(Globals.objectsPath):
        objects.append(f"{Globals.objectsPath}/{obj}")

    clangArgs: list[str] = [
        "clang++",
        *flags,
        *objects,
        "-o",
        f"{binaryDirectory}/{binaryName}{Platform.getBinaryFileExtension()}"
    ]

    callback: subprocess.CompletedProcess[str] = subprocess.run(clangArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True