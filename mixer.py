from playlistsetting import PlaylistSetting
from rulesrelated import *
from songsrelated import Song, createSongList
from networkmethods import *
from settings import loadRules

class Mixer:
    def createLists() -> None:
        resultsOfSettings: list[PlaylistSetting] = loadRules()
        for i in resultsOfSettings:
            songs: list[Song] = createSongList(download(i.getSource()))
            Mixer.prepare(songs, i)
            playlist: list[Song] = Mixer.mix(i.getRulesRoot(), i.getLength())
            upload([ f"spotify:track:{i.getSpotifyId()}" for i in playlist ], i.getName())

    def mix(root: Rule, length: int) -> list[Song]:
        playlist: list[Song] = []
        for _ in range(length):
            playlist.append(root.getNext())
        return playlist

    def prepare(songs: list[Song], setting: PlaylistSetting) -> None:
        if len(setting.getRulesRoot().getSubrules()) == 0:
            raise ValueError("There aren't any rules!")
        Mixer.fillRules(songs, setting.getRulesRoot())
        Mixer.precheck(setting.getRulesRoot())

    def fillRules(songs: list[Song], rulesroot: Rule) -> None:
        for i in songs:
            rulesroot.addSong(i)
        rulesroot.getReady()

    def precheck(rulesroot: Rule) -> None:
        if rulesroot.getType() == RuleType.ROOT:
            if len(rulesroot.getSubrules()) == 0:
                raise ValueError("Root should contain rules!")
        if not len(rulesroot.getSubrules()) == 0:
            if not len(rulesroot.getSongs()) == 0:
                raise ValueError("A rule with subrules should not contain songs!")
            probabilities: int = 0
            for i in rulesroot.getSubrules():
                probabilities += i.getProbability()
                if i.getProbability() < 0 or i.getProbability() > 100:
                    raise ValueError("All probabilities must be between 0 and 100!")
                Mixer.precheck(i)
            if not probabilities == 100:
                raise ValueError("Probabilities should add to 100 in each level of hierarchy!")
        else: 
            if len(rulesroot.getSongs()) == 0:
                raise ValueError("There is a rule for which no songs qualify!")