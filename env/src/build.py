import os
import tomllib
from util import clang
from util import color

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
        match value["binType"]:
            case "executable":
                clang.linkExec (
                        f"{buildDir}/{value["binDir"]}",
                    value["binName"],
                    data["global"]["flags"]["shared"] +
                    data["global"]["flags"]["link"] +
                    value["flags"]["shared"] +
                    value["flags"]["link"]
                )
            case "dynamic": pass

    return

if __name__ == "__main__": main()