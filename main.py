from networkmethods import *
from songsrelated import *
from settings import *
from mixer import *

def main() -> None:
    try:
        authenticate()
        Mixer.createLists()
    except Exception as e:
        print("Try again later or check if you set everything up correctly.")
        print(e)

main()