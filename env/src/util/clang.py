import os
import shutil
import subprocess
from . import color

def init() -> bool: return Globals.init()
class Globals:
    execExt: str
    objectsPath: str
    buildPath: str
    binPath: str

    @staticmethod
    def init() -> bool:
        match os.name:
            case "nt": Globals.execExt = ".exe"
            case "posix": Globals.execExt = ""
            case _:
                print(f"{color.makeRed("Error")}: unsupported OS")
                return False

        Globals.objectsPath = "objects"
        Globals.buildPath = "build"
        Globals.binPath = f"{Globals.buildPath}/bin"

        if os.path.exists(Globals.objectsPath):
            shutil.rmtree(Globals.objectsPath)

        os.mkdir(Globals.objectsPath)
        os.mkdir(Globals.buildPath)
        os.mkdir(Globals.binPath)
        return True

def compile(src: str, flags: list[str] = []) -> bool:
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

def linkExec(binaryName: str, flags: list[str] = []) -> bool:
    objects: list[str] = []
    for obj in os.listdir(Globals.objectsPath):
        objects.append(f"{Globals.objectsPath}/{obj}")

    clangArgs: list[str] = [
        "clang++",
        *flags,
        *objects,
        "-o",
        f"{Globals.buildPath}/{binaryName}{Globals.execExt}"
    ]

    print(f"Linking into executable binary..", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run(clangArgs, capture_output=True, text=True)

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True