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
    def getExecutableBinaryExtension() -> str: #type: ignore[return]
        match Platform.enum:
            case Platform.Enumeration.LINUX: return ""
            case Platform.Enumeration.WINDOWS: return ".exe"

    @staticmethod
    def getDynamicBinaryExtension() -> str: #type: ignore[return]
        match Platform.enum:
            case Platform.Enumeration.LINUX: return ".so"
            case Platform.Enumeration.WINDOWS: return ".dll"

    @staticmethod
    def getStaticBinaryExtension() -> str: #type: ignore[return]
        match Platform.enum:
            case Platform.Enumeration.LINUX: return ".a"
            case Platform.Enumeration.WINDOWS: return ".lib"

if __name__ != "__main__":
    if not Platform.init():
        print(f"{color.makeRed("Error")}: unsupported OS")
        sys.exit(1)