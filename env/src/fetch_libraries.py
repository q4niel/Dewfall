import os
import shutil
import tarfile
import requests
import tomllib
from util.platform import Platform

def fetch(name: str, url: str) -> None:
    preEntries: list[str] = os.listdir("3rd")
    archive: str = url.replace("/", "")

    with open(f"3rd/raw/{archive}", "wb") as file:
        file.write(requests.get(url).content)

    with tarfile.open(f"3rd/raw/{archive}", "r:*") as tar:
        tar.extractall(path=f"3rd")

    for entry in os.listdir("3rd"):
        if entry in preEntries: continue
        os.rename(f"3rd/{entry}", f"3rd/{name}")

if __name__ == "__main__":
    if os.path.exists("3rd"):
        shutil.rmtree("3rd")

    os.mkdir("3rd")
    os.mkdir("3rd/raw")

    with open("src/build.toml", "rb") as file:
        data: dict = tomllib.load(file)

    for lib in data["global"]["3rdLibraries"][Platform.getString()]:
        fetch(lib["name"], lib["url"])

    shutil.rmtree("3rd/raw")