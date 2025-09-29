import os
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

    print(f"Compiling '{src}'...", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run (
        ["clang++", *flags, "-c", src, "-o", f"{Globals.objectsPath}/{os.path.basename(src)[:-3]}o"],
        capture_output=True,
        text=True
    )

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

    print(f"Linking into executable binary..", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run (
        ["clang++", *flags, *objects, "-o", f"{Globals.buildPath}/{binaryName}{Globals.execExt}"],
        capture_output=True,
        text=True
    )

    if callback.returncode != 0:
        print(f" {color.makeRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeGreen("Success")}")
    return True