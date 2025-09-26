import os
import subprocess
from . import color
def init() -> None:
    os.mkdir("objects")
    os.mkdir("build")

def compile(src: str, flags: list[str] = []) -> bool:
    if not os.path.exists(src):
        print(f"{color.makeFailureRed("Error")}: source '{src}' does not exist!")
        return False

    if os.path.isdir(src):
        print(f"{color.makeFailureRed("Error")}: source '{src}' is a directory?")
        return False

    print(f"Compiling '{src}'...", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run (
        ["clang++", *flags, "-c", src, "-o", f"objects/{os.path.basename(src)[:-3]}o"],
        capture_output=True,
        text=True
    )

    if callback.returncode != 0:
        print(f" {color.makeFailureRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeSuccessGreen("Success")}")
    return True

def linkExec(binaryName: str, flags: list[str] = []) -> bool:
    binExt: str = ""
    match os.name:
        case "nt": binExt = ".exe"
        case "posix": pass
        case _:
            print(f"{color.makeFailureRed("Error")}: unsupported OS")
            return False

    objects: list[str] = []
    for obj in os.listdir("objects"):
        objects.append(f"objects/{obj}")

    print(f"Linking into executable binary..", end="")
    callback: subprocess.CompletedProcess[str] = subprocess.run (
        ["clang++", *flags, *objects, "-o", f"build/{binaryName}{binExt}"],
        capture_output=True,
        text=True
    )

    if callback.returncode != 0:
        print(f" {color.makeFailureRed("Failure")}")
        print(callback.stderr)
        return False

    print(f" {color.makeSuccessGreen("Success")}")
    return True