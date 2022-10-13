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

def createSongList(source: list[dict]) -> list[Song]:
    songs: list[Song] = []
    for i in source:
        for j in i["items"]:
            title: str = j["track"]["name"]
            artists: list[str] = []
            for k in j["track"]["artists"]:
                artists.append(k["name"])
            year: int = int(j["track"]["album"]["release_date"].split("-")[0])
            id: str = j["track"]["id"]
            popularity: int = j["track"]["popularity"]
            songs.append(Song(title, artists, id, year, popularity))
    return songs