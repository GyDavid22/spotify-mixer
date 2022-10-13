from networkmethods import *
from songsrelated import *
from settings import *
from mixer import *

def main() -> None:
    Settings.token = authenticate
    songs: list[Song] = createSongList(req(Settings.pid))
    Mixer.createLists(songs)

main()