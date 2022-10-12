import enum
import songMethods
import random

class RuleType(enum.Enum):
    ROOT = 0 # Don't use in your own rules!
    POPULARITY = 1
    YEAR = 2

class Rule:
    def __init__(self, type: RuleType, probability: int, subrules: list = [], minValue: int = None, maxValue: int = None,
                 finishBeforeRepeat: bool = True) -> None:
        """Min and max values are inclusive!"""
        self.__type: RuleType = type
        self.__probability: int = probability # A number between 0 and 100 (percent value)
        self.__songs: list[songMethods.Songs] = []
        self.__playedSongs: list[songMethods.Songs] = []
        self.__songsToPlay: list[songMethods.Songs] = []
        self.__subrules: list[Rule] = sorted(subrules, key=Rule.getProbability)
        self.__finishBeforeRepeat: bool = finishBeforeRepeat
        self.__minValue: int = minValue
        self.__maxValue: int = maxValue
        self.__onRepeat = False
        if self.__type == RuleType.YEAR:
            self.__comparefunc = songMethods.Songs.getYear
        elif self.__type == RuleType.POPULARITY:
            self.__comparefunc = songMethods.Songs.getPopularity

    def getProbability(self) -> int:
        return self.__probability

    def getSubrules(self) -> list:
        return self.__subrules

    def getSongs(self) -> list[songMethods.Songs]:
        return self.__songs

    def getType(self) -> RuleType:
        return self.__type

    def addSong(self, song: songMethods.Songs) -> None:
        qualifying: bool = ((self.__minValue == None and self.__maxValue == None)
                or (self.__minValue == None and self.__comparefunc(song) <= self.__maxValue)
                or (self.__maxValue == None and self.__minValue <= self.__comparefunc(song))
                or (self.__minValue <= self.__comparefunc(song) and self.__maxValue >= self.__comparefunc(song)))

        if (not len(self.__subrules) == 0) and qualifying:
            for i in self.__subrules:
                i.addSong(song)
        else:
            if self.__type == RuleType.ROOT:
                raise ValueError("Don't add songs to root!")

            if qualifying:
                self.__songs.append(song)

    def getReady(self):
        if not len(self.__subrules) == 0:
            for i in self.__subrules:
                i.getReady()
        else:
            self.__songsToPlay = list(self.__songs)
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
            bottom: int = 1
            top: int = 0
            for i in self.__subrules:
                top += i.getProbability()
                if selectedSubRule >= bottom and selectedSubRule <= top:
                    return i.getNext()
                bottom = top + 1
        else:
            if self.__finishBeforeRepeat:
                selected: songMethods.Songs = self.__songsToPlay.pop(0)
                self.__playedSongs.append(selected)
                if len(self.__songsToPlay) == 0:
                    self.getReady()
                return selected
            else:
                return self.__songsToPlay[random.randint(0, len(self.__songsToPlay) - 1)]

