from playlistSettingsClass import PlaylistSetting
from ruleClasses import *
from settings import Settings

def loadRules() -> list[PlaylistSetting]:
    return [
        PlaylistSetting("HotAC", Settings.pid, [
            Rule(RuleType.YEAR, 50, minValue=2020, subrules=[
                Rule(RuleType.POPULARITY, 75, minValue=70),
                Rule(RuleType.POPULARITY, 25, maxValue=69)
            ]),
            Rule(RuleType.YEAR, 18, minValue=2010, maxValue=2019, subrules=[
                Rule(RuleType.POPULARITY, 75, minValue=70),
                Rule(RuleType.POPULARITY, 25, maxValue=69)
            ]),
            Rule(RuleType.YEAR, 18, minValue=2000, maxValue=2009, subrules=[
                Rule(RuleType.POPULARITY, 75, minValue=70),
                Rule(RuleType.POPULARITY, 25, maxValue=69)
            ]),
            Rule(RuleType.YEAR, 14, maxValue=1999, subrules=[
                Rule(RuleType.POPULARITY, 75, minValue=70),
                Rule(RuleType.POPULARITY, 25, maxValue=69)
            ])
        ])
    ]