import tomllib
from util import clang

if __name__ == "__main__":
    with open("src/build.toml", "rb") as file:
        buildData: dict = tomllib.load(file)

    clang.init()

    shallLink: bool = True
    for src in buildData["global"]["compile"]:
        if not clang.compile (
            f"src/{src}",
            buildData["flags"]["shared"] + buildData["flags"]["compile"]
        ): shallLink = False

    print()
    clang.linkExec (
        "app",
        buildData["flags"]["shared"] + buildData["flags"]["link"]
    )