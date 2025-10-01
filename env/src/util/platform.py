import os
from enum import Enum

class Platform:
    class Enumeration(Enum):
        INVALID = 1
        LINUX = 2
        WINDOWS = 3

    def __init__(self):
        self.enum: Platform.Enumeration
        match os.name:
            case "posix": self.enum = Platform.Enumeration.LINUX
            case "nt": self.enum =  Platform.Enumeration.WINDOWS
            case _: self.enum = Platform.Enumeration.INVALID

    def getEnum(self): return self.enum

    def isValid(self) -> bool:
        return Platform.Enumeration.INVALID != self.getEnum()

    def getString(self):
        match self.enum:
            case Platform.Enumeration.INVALID: return "invalid"
            case Platform.Enumeration.LINUX: return "linux"
            case Platform.Enumeration.WINDOWS: return "windows"