import enum
import songMethods

class RuleType(enum.Enum):
    POPULARITY = 1
    YEAR = 2

class Rule:
    class SongWithMetadata:
        def __init__(self, song: songMethods.Songs) -> None:
            self.song: songMethods.Songs = song
            self.wasAlready: bool = False

    def __init__(self, type: RuleType, probability: float, subrules: list = [], popularityMin: int = None,
                popularityMax: int = None, yearMin: int = None, yearMax: int = None) -> None:
        """Min and max values are inclusive!"""
        self.__type: RuleType = type
        self.__probability: float = probability
        self.__songs: list[Rule.SongWithMetadata] = []
        self.__subrules: list[Rule] = subrules
        if self.__type == RuleType.POPULARITY:
            self.__popularityMin: int = popularityMin
            self.__popularityMax: int = popularityMax
        elif self.__type == RuleType.YEAR:
            self.__yearMin: int = yearMin
            self.__yearMax: int = yearMax
        else:
            raise ValueError("Bad rule type")