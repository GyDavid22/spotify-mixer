class Song:
    def __init__(self, title: str, artist: list[str], spotifyId: str, year: int, popularity: int) -> None:
        self.__title: str = title
        self.__artist: list[str] = artist
        self.__spotifyId: str = spotifyId
        self.__year: int = int(year)
        self.__popularity: int = int(popularity)

    def getTitle(self) -> str:
        return self.__title

    def getArtists(self) -> list[str]:
        return self.__artist

    def getSpotifyId(self) -> str:
        return self.__spotifyId

    def getYear(self) -> int:
        return self.__year

    def getPopularity(self) -> int:
        return self.__popularity

    def __str__(self) -> str:
        return f"{', '.join(self.getArtists())} - {self.getTitle()} ({self.getYear()})"

class GenerateHelper:
    alreadyGenerated: dict[str, list[Song]] = dict()

def createSongList(source: tuple[str, list[dict]]) -> list[Song]:
    if source[0] in GenerateHelper.alreadyGenerated:
        return GenerateHelper.alreadyGenerated[source[0]]
    songs: list[Song] = []
    for i in source[1]:
        for j in i["items"]:
            title: str = j["track"]["name"]
            artists: list[str] = []
            for k in j["track"]["artists"]:
                artists.append(k["name"])
            year: int = int(j["track"]["album"]["release_date"].split("-")[0])
            id: str = j["track"]["id"]
            popularity: int = j["track"]["popularity"]
            songs.append(Song(title, artists, id, year, popularity))
    GenerateHelper.alreadyGenerated[source[0]] = songs
    return songs