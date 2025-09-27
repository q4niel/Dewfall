import os
import tomllib
from util import clang
from util import color

def main() -> None:
    if not os.path.exists("3rd"):
        print(f"{color.makeFailureRed("Error")}: 3rd party libraries have not been installed")
        return

    with open("src/build.toml", "rb") as file:
        data: dict = tomllib.load(file)

    clang.init()

    for src in data["global"]["compile"]:
        if not clang.compile (
            f"src/{src}",
            data["flags"]["shared"] + data["flags"]["compile"]
        ): return

    print()
    clang.linkExec (
        "app",
        data["flags"]["shared"] + data["flags"]["link"]
    )

if __name__ == "__main__": main()