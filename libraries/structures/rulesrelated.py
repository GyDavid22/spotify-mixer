import enum
import random
from songsrelated import Song

class RuleType(enum.Enum):
    ROOT = 0 # Don't use in your own rules!
    POPULARITY = 1
    YEAR = 2

class Rule:
    """Class to represent a Rule"""
    def __init__(self, type: RuleType, probability: int, subrules: list = [], minValue: int = None, maxValue: int = None,
                 finishBeforeRepeat: bool = True) -> None:
        """Min and max values are inclusive!"""
        self.__type: RuleType = type
        self.__probability: int = probability
        """A number between 0 and 100 (percent value)"""
        self.__songs: list[Song] = []
        """All songs which fit this rule"""
        self.__playedSongs: list[Song] = []
        """Songs which are already selected"""
        self.__songsToPlay: list[Song] = []
        """Songs which wait to get selected"""
        self.__subrules: list[Rule] = sorted(subrules, key=Rule.getProbability)
        self.__finishBeforeRepeat: bool = finishBeforeRepeat # Don't repeat songs in/under this rule until all songs are used
        self.__minValue: int = minValue
        self.__maxValue: int = maxValue
        self.__onRepeat = False
        if self.__type == RuleType.YEAR:
            self.__comparefunc = Song.getYear
        elif self.__type == RuleType.POPULARITY:
            self.__comparefunc = Song.getPopularity

    def getProbability(self) -> int:
        return self.__probability

    def getSubrules(self) -> list:
        return self.__subrules

    def getSongs(self) -> list[Song]:
        return self.__songs

    def getType(self) -> RuleType:
        return self.__type

    def shouldBeFinishedBeforeRepeat(self) -> bool:
        return self.__finishBeforeRepeat

    def addSong(self, song: Song) -> None:
        qualifying: bool
        try:
            qualifying = ((self.__minValue == None and self.__maxValue == None)
                or (self.__minValue == None and self.__comparefunc(song) <= self.__maxValue)
                or (self.__maxValue == None and self.__minValue <= self.__comparefunc(song))
                or (self.__minValue <= self.__comparefunc(song) and self.__maxValue >= self.__comparefunc(song)))
        except:
            qualifying = False

        if (not len(self.__subrules) == 0) and qualifying:
            for i in self.__subrules:
                i.addSong(song)
        else:
            if self.__type == RuleType.ROOT:
                raise ValueError("Don't add songs to root!")

            if qualifying:
                self.__songs.append(song)

    def getReady(self):
        """Prepare Rule and subrules to mixing"""
        if not len(self.__subrules) == 0:
            for i in self.__subrules:
                i.getReady()
        else:
            self.__songsToPlay = list(self.__songs)
            random.shuffle(self.__songsToPlay)
            self.__playedSongs.clear()

    def allSongsSelected(self) -> bool:
        """Are we just repeating as there are no unselected songs?"""
        if not len(self.__subrules) == 0:
            for i in self.__subrules:
                if not i.allSongsSelected():
                    return False
            return True
        else:
            return self.__onRepeat

    def getNext(self) -> Song:
        """Get the next song from this rule/subrules"""
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
                selected: Song = self.__songsToPlay.pop(0)
                self.__playedSongs.append(selected)
                if len(self.__songsToPlay) == 0:
                    self.getReady()
                    self.__onRepeat = True
                return selected
            else:
                return self.__songsToPlay[random.randint(0, len(self.__songsToPlay) - 1)]
            
    def __str__(self) -> str:
        returnValue: str = f"Rule: probability: {self.getProbability()}, type: {self.getType().name}, min: {self.__minValue}, max: {self.__maxValue}, finishBeforeRepeat: {self.__finishBeforeRepeat}{f', qualified songs: {len(self.__songs)}' if len(self.__songs) > 0 else ''}\n"
        subrules: str = ""
        for i in self.getSubrules():
            subrules += str(i)
        if not subrules == "":
            returnValue += "".join([ f"    {i}\n" for i in subrules.split("\n")])
        return returnValue