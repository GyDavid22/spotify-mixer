import enum
import songMethods
import random

class RuleType(enum.Enum):
    ROOT = 0 # Don't use in your own rules!
    POPULARITY = 1
    YEAR = 2

class Rule:
    def __init__(self, type: RuleType, probability: float, subrules: list = [], popularityMin: int = None,
                popularityMax: int = None, yearMin: int = None, yearMax: int = None, finishBeforeRepeat: bool = True) -> None:
        """Min and max values are inclusive!"""
        self.__type: RuleType = type
        self.__probability: int = probability # A number between 0 and 100 (percent value)
        self.__songs: list[songMethods.Songs] = []
        self.__playedSongs: list[songMethods.Songs] = []
        self.__songsToPlay: list[songMethods.Songs] = []
        self.__subrules: list[Rule] = sorted(subrules, key=Rule.getProbability)
        self.__finishBeforeRepeat = True
        if self.__type == RuleType.POPULARITY:
            self.__popularityMin: int = popularityMin
            self.__popularityMax: int = popularityMax
        elif self.__type == RuleType.YEAR:
            self.__yearMin: int = yearMin
            self.__yearMax: int = yearMax
        else:
            raise ValueError("Bad rule type")

    def getProbability(self) -> int:
        return self.__probability

    def addSong(self, song: songMethods.Songs) -> None:
        if not len(self.__subrules) == 0:
            for i in self.__subrules:
                i.addSong(song)
        else:
            if self.__type == RuleType.POPULARITY:
                minToCompare: int = self.__popularityMin
                maxToCompare: int = self.__popularityMax
            elif self.__type == RuleType.YEAR:
                minToCompare: int = self.__yearMin
                maxToCompare: int = self.__yearMax
            elif self.__type == RuleType.ROOT:
                raise ValueError("Don't add songs to root!")

            if ((minToCompare == None and maxToCompare == None)
                or (minToCompare == None and song.getPopularity() <= maxToCompare)
                or (maxToCompare == None and minToCompare >= song.getPopularity())
                or (minToCompare >= song.getPopularity() and maxToCompare <= song.getPopularity())):
                self.__songs.append(song)

    def getReady(self):
        self.__songsToPlay = self.__songs
        random.shuffle(self.__songsToPlay)
        self.__playedSongs.clear()

    def allSongsSelected(self) -> bool:
        if not len(self.__subrules) == 0:
            for i in self.__subrules:
                if not i.allSongsSelected():
                    return False
            return True
        else:
            return len(self.__playedSongs) == len(self.__songs)

    def getNext(self) -> songMethods.Songs:
        if not len(self.__subrules) == 0:
            selectedSubRule: int = random.randint(1, 100)
            for i in self.__subrules:
                if i.getProbability() >= selectedSubRule:
                    return i.getNext()
        else:
            if self.__finishBeforeRepeat:
                selected: songMethods.Songs = self.__songsToPlay.pop(0)
                self.__playedSongs.append(selected)
                if len(self.__songsToPlay) == 0:
                    self.getReady()
                return selected
            else:
                return self.__songsToPlay[random.randint(0, len(self.__songsToPlay) - 1)]

