from settings import Settings

def log(message: str) -> None:
    if Settings.verbose:
        print(message)