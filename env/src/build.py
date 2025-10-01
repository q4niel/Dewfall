import os
import shutil
import tomllib
from util import clang
from util import color
from util.platform import Platform

def main() -> None:
    if not os.path.exists("3rd"):
        print(f"{color.makeRed("Error")}: 3rd party libraries have not been installed")
        return

    with open("src/build.toml", "rb") as file:
        data: dict = tomllib.load(file)

    buildDir: str = "build"
    os.mkdir(buildDir)

    for dir in data["global"]["createDirectories"]:
        os.mkdir(f"{buildDir}/{dir}")

    for src in data["global"]["copySources"][f"{Platform.getString()}"]:
        shutil.copy(src["from"], f"{buildDir}/{src["to"]}")

    for key, value in data["build"].items():
        print(color.makeMagenta(f"[ Building '{key}' ]\n"))
        if not clang.init(): return

        for src in value["sources"]:
            if not clang.compile (
                f"src/{src}",
                data["global"]["flags"]["shared"] +
                data["global"]["flags"]["compile"] +
                value["flags"]["shared"] +
                value["flags"]["compile"]
            ): return

        print()
        binType: clang.BinaryType
        match value["binType"]:
            case "executable": binType = clang.BinaryType.EXECUTABLE
            case "dynamic": binType = clang.BinaryType.DYNAMIC
            case "static": binType = clang.BinaryType.STATIC
            case _:
                print(f"{color.makeRed("Error")}: binType '{value["binType"]}' is invalid")
                return

        clang.linkBinary (
            f"{buildDir}/{value["binDir"]}",
            value["binName"],
            binType,
            data["global"]["flags"]["shared"] +
            data["global"]["flags"]["link"] +
            value["flags"]["shared"] +
            value["flags"]["link"]
        )

    return

if __name__ == "__main__": main()