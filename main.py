import sys

from networkmethods import *
from songsrelated import *
from settings import *
from mixer import *
from logger import log

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