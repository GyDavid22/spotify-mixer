from rulesrelated import *

class PlaylistSetting:
    """Class to represent a playlist to make, mostly containing Rules"""
    def __init__(self, name: str, source: str, length: int, rules: list[Rule]) -> None:
        """Give a name to the setting and give it the Spotify ID of the base playlist"""
        self.__name: str = name
        self.__source: str = source
        self.__length = length
        self.__rulesroot: Rule = Rule(RuleType.ROOT, 100, subrules=rules)

    def getName(self) -> str:
        return self.__name
    
    def getSource(self) -> str:
        return self.__source

    def getLength(self) -> int:
        return self.__length

    def getRulesRoot(self) -> Rule:
        return self.__rulesroot
    
    def __str__(self) -> str:
        return f"Setting: name: {self.getName()}, source: {self.getSource()}, length: {self.getLength()}\n{self.getRulesRoot()}"
