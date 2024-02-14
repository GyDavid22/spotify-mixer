import sys

from libraries.logic.networkmethods import *
from libraries.structures.songsrelated import *
from settings import *
from libraries.logic.mixer import *
from libraries.logic.logger import log

def main() -> None:
    """Entry point of the program."""
    try:
        authenticate()
        Mixer.createLists()
    except Exception as e:
        print("Try again later or check if you set everything up correctly.", file=sys.stderr)
        print(e, file=sys.stderr)
    log("Exiting.")

main()