import os
import shutil
import tarfile
import requests
import tomllib

def fetch(path: str, url: str) -> None:
    with open(f"3rd/raw/{path}", "wb") as file:
        file.write(requests.get(url).content)

    with tarfile.open(f"3rd/raw/{path}", "r:*") as tar:
        tar.extractall(path=f"3rd/{path}")

if __name__ == "__main__":
    os.mkdir("3rd/raw")

    with open("3rd/config.toml", "rb") as file:
        configData: dict = tomllib.load(file)

    for lib in configData["libraries"]:
        fetch(lib["path"], lib["url"])

    shutil.rmtree("3rd/raw")