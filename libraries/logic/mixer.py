from libraries.structures.playlistsetting import PlaylistSetting
from libraries.structures.rulesrelated import *
from libraries.structures.songsrelated import Song, createSongList
from libraries.logic.networkmethods import *
from settings import loadRules
from libraries.logic.logger import log

class Mixer:
    """Class to contain mixing related stuff"""
    def createLists() -> None:
        """Method to generate all playlists according to PlaylistSettings"""
        resultsOfSettings: list[PlaylistSetting] = loadRules()
        for i in resultsOfSettings:
            songs: list[Song] = createSongList(download(i.getSource()))
            Mixer.prepare(songs, i)
            playlist: list[Song] = Mixer.mix(i.getRulesRoot(), i.getLength())
            upload([ f"spotify:track:{i.getSpotifyId()}" for i in playlist ], i.getName())

    def mix(root: Rule, length: int) -> list[Song]:
        """Method to generate the new playlist"""
        playlist: list[Song] = []
        i: int = 0
        while (length == -1 and (not root.allSongsSelected())) or i < length:
            playlist.append(root.getNext())
            i += 1
        return playlist

    def prepare(songs: list[Song], setting: PlaylistSetting) -> None:
        """Preparing a PlaylistSetting"""
        if len(setting.getRulesRoot().getSubrules()) == 0:
            raise ValueError("There aren't any rules!")
        Mixer.fillRules(songs, setting.getRulesRoot())
        Mixer.precheck(setting)
        log(setting)

    def fillRules(songs: list[Song], rulesroot: Rule) -> None:
        """Fill up Rule leaves with songs"""
        for i in songs:
            rulesroot.addSong(i)
        rulesroot.getReady()

    def precheck(setting: PlaylistSetting, rulesroot: Rule = None) -> None:
        """Method to validate a PlaylistSetting"""
        if rulesroot == None:
            rulesroot: Rule = setting.getRulesRoot()
        if setting.getLength() == -1 and (not rulesroot.shouldBeFinishedBeforeRepeat()):
            raise ValueError("If playlist length is -1, then finishBeforeRepeat should be True for all rules!")
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
                Mixer.precheck(setting, i)
            if not probabilities == 100:
                raise ValueError("Probabilities should add up to 100 in each level of hierarchy!")
        else: 
            if len(rulesroot.getSongs()) == 0:
                raise ValueError("There is a rule for which no songs qualify!")