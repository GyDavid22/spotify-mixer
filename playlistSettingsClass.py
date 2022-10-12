import ruleClasses

class PlaylistSetting:
    def __init__(self, name: str, source: str, rules: list[ruleClasses.Rule]) -> None:
        """Give a name to the setting and give it the Spotify ID of the base playlist"""
        self.__name = name
        self.__source = source
        self.__rulesroot = ruleClasses.Rule(ruleClasses.RuleType.ROOT, 100, subrules=rules)

    def getName(self) -> str:
        return self.__name
    
    def getSource(self) -> str:
        return self.__source

    def getRulesRoot(self) -> ruleClasses.Rule:
        return self.__rulesroot