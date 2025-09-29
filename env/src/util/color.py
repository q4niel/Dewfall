def makeColored(string: str, colorCode: int) -> str:
    return f"\033[{colorCode}m{string}\033[0m"

def makeGreen(string: str) -> str:
    return makeColored(string, 32)

def makeRed(string: str) -> str:
    return makeColored(string, 31)

def makeMagenta(string: str) -> str:
    return makeColored(string, 35)