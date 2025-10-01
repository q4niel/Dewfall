import os
import sys
from enum import Enum
from . import color

class Platform:
    class Enumeration(Enum):
        LINUX = 1
        WINDOWS = 2

    enum: Enumeration

    @staticmethod
    def init() -> bool:
        match os.name:
            case "posix": Platform.enum = Platform.Enumeration.LINUX
            case "nt": Platform.enum =  Platform.Enumeration.WINDOWS
            case _: return False
        return True

    @staticmethod
    def getString() -> str: #type: ignore[return]
        match Platform.enum:
            case Platform.Enumeration.LINUX: return "linux"
            case Platform.Enumeration.WINDOWS: return "windows"

    @staticmethod
    def getBinaryFileExtension() -> str: #type: ignore[return]
        match Platform.enum:
            case Platform.Enumeration.LINUX: return ""
            case Platform.Enumeration.WINDOWS: return ".exe"

if __name__ != "__main__":
    if not Platform.init():
        print(f"{color.makeRed("Error")}: unsupported OS")
        sys.exit(1)