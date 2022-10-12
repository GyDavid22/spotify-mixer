from playlistSettingsClass import PlaylistSetting
from ruleClasses import *
from settings import Settings

def loadRules() -> list[PlaylistSetting]:
    return [
        PlaylistSetting("example", Settings.pid, [
            Rule(RuleType.YEAR, 100, [
                Rule(RuleType.POPULARITY, 100)
            ])
        ])
    ]