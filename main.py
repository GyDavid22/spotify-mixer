from statistics import mean
from networkAndFileMethods import loadResps
from songMethods import *

def main() -> None:
    songs: list[Songs] = createSongList(loadResps())
    yearsCount: dict[int, int] = dict()
    for i in songs:
        if i.year in yearsCount:
            yearsCount[i.year] += 1
        else:
            yearsCount[i.year] = 1
    years = sorted(list(yearsCount.keys()))
    for year in years:
        print(f"{year}: {yearsCount[year]}")
    popurarityies = [ i.popularity for i in songs ]
    print(f"{mean(popurarityies)}, {min(popurarityies)}, {max(popurarityies)}")
    songs.sort(key=Songs.temppop, reverse=True)
    for i in songs:
        print(f"{i}, {i.popularity}")


main()