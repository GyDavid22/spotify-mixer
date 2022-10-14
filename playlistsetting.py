from rulesrelated import *

class PlaylistSetting:
    def __init__(self, name: str, source: str, rules: list[Rule]) -> None:
        """Give a name to the setting and give it the Spotify ID of the base playlist"""
        self.__name: str = name
        self.__source: str = source
        self.__rulesroot: Rule = Rule(RuleType.ROOT, 100, subrules=rules)

    def getName(self) -> str:
        return self.__name
    
    def getSource(self) -> str:
        return self.__source

    def getRulesRoot(self) -> Rule:
        return self.__rulesroot