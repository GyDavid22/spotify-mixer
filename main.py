from networkmethods import *
from songsrelated import *
from settings import *
from mixer import *

def main() -> None:
    authenticate()
    Mixer.createLists()

main()