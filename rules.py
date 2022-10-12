from playlistSettingsClass import PlaylistSetting
from ruleClasses import *
from settings import Settings

def loadRules() -> list[PlaylistSetting]:
    return [
        PlaylistSetting("Min90pop", Settings.pid, [
            Rule(RuleType.POPULARITY, 100, minValue=90)
        ]),
        PlaylistSetting("Only2022", Settings.pid, [
            #more rules don't get done
            Rule(RuleType.YEAR, 50, minValue=2022, maxValue=2022),
            Rule(RuleType.YEAR, 50, minValue=2021, maxValue=2021)
        ])
    ]