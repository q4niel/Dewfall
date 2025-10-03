import os
import shutil
import tomllib
from util import compiler
from util import color
from util.platform import Platform
from util.binary_type import BinaryType

def main() -> None:
    if not os.path.exists("3rd"):
        print(f"{color.makeRed("Error")}: 3rd party libraries have not been installed")
        return

    with open("src/build.toml", "rb") as file:
        data: dict = tomllib.load(file)

    buildDir: str = "build"
    binDir: str = f"{buildDir}/bin"
    licDir: str = f"{buildDir}/lic"
    os.mkdir(buildDir)
    os.mkdir(binDir)
    os.mkdir(licDir)

    for src in data["global"]["copySources"][f"{Platform.getString()}"]:
        shutil.copy(src["from"], f"{buildDir}/{src["to"]}")

    for key, value in data["build"].items():
        print(color.makeMagenta(f"[ Building '{key}' ]\n"))
        if not compiler.init(): return

        for src in value["sources"]:
            if not compiler.compile (
                f"src/{src}",
                data["global"]["flags"]["shared"] +
                data["global"]["flags"]["compile"] +
                value["flags"]["shared"] +
                value["flags"]["compile"]
            ): return

        print()
        binType: BinaryType
        match value["binType"]:
            case "executable": binType = BinaryType.EXECUTABLE
            case "dynamic": binType = BinaryType.DYNAMIC
            case "static": binType = BinaryType.STATIC
            case _:
                print(f"{color.makeRed("Error")}: binType '{value["binType"]}' is invalid")
                return

        compiler.linkBinary (
            binDir,
            value["binName"],
            binType,
            data["global"]["flags"]["shared"] +
            data["global"]["flags"]["link"] +
            value["flags"]["shared"] +
            value["flags"]["link"],
            value["dynamicLibraries"]
        )

    return

if __name__ == "__main__": main()