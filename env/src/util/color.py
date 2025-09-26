def makeSuccessGreen(string: str) -> str:
    return f"\033[32m{string}\033[0m"

def makeFailureRed(string: str) -> str:
    return f"\033[31m{string}\033[0m"