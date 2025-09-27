import tomllib
from util import clang

if __name__ == "__main__":
    with open("src/config.toml", "rb") as file:
        configData: dict = tomllib.load(file)

    clang.init()

    shallLink: bool = True
    for src in configData["global"]["compile"]:
        if not clang.compile (
            f"src/{src}",
            configData["flags"]["shared"] + configData["flags"]["compile"]
        ): shallLink = False

    print()
    clang.linkExec (
        "app",
        configData["flags"]["shared"] + configData["flags"]["link"]
    )