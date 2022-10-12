from statistics import mean
import networkAndFileMethods
from settings import Settings
from songMethods import *
import mixer

def main() -> None:
    songs: list[Songs] = createSongList(networkAndFileMethods.req(Settings.pid))
    mixer.Mixer.createLists(songs)
    # yearsCount: dict[int, int] = dict()
    # for i in songs:
    #     if i.getYear() in yearsCount:
    #         yearsCount[i.getYear()] += 1
    #     else:
    #         yearsCount[i.getYear()] = 1
    # years = sorted(list(yearsCount.keys()))
    # for year in years:
    #     print(f"{year}: {yearsCount[year]}")
    # popurarityies = [ i.getPopularity() for i in songs ]
    # print(f"{mean(popurarityies)}, {min(popurarityies)}, {max(popurarityies)}")
    # songs.sort(key=Songs.getPopularity, reverse=True)
    # for i in songs:
    #     print(f"{i}, {i.getPopularity()}")


main()