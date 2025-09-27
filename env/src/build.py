import tomllib
from util import clang

if __name__ == "__main__":
    with open("src/build.toml", "rb") as file:
        data: dict = tomllib.load(file)

    clang.init()

    shallLink: bool = True
    for src in data["global"]["compile"]:
        if not clang.compile (
            f"src/{src}",
            data["flags"]["shared"] + data["flags"]["compile"]
        ): shallLink = False

    print()
    clang.linkExec (
        "app",
        data["flags"]["shared"] + data["flags"]["link"]
    )