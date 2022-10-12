class Songs:
    def __init__(self, title: str, artist: str, spotifyId: str, year: int, popularity: int) -> None:
        self.__title: str = title
        self.__artist: str = artist
        self.__spotifyId: str = spotifyId
        self.__year: int = int(year)
        self.__popularity: int = int(popularity)

    def getTitle(self) -> str:
        return self.__title

    def getArtist(self) -> str:
        return self.__artist

    def getSpotifyId(self) -> str:
        return self.__spotifyId

    def getYear(self) -> int:
        return self.__year

    def getPopularity(self) -> int:
        return self.__popularity

    def __str__(self) -> str:
        return f"{self.getArtist()} - {self.getTitle()} ({self.getYear()})"

def createSongList(source: list[dict]) -> list[Songs]:
    songs: list[Songs] = []
    for i in source:
        for j in i["items"]:
            names = []
            for k in j["track"]["artists"]:
                names.append(k["name"])
            names = ", ".join(names)
            year = int(j["track"]["album"]["release_date"].split("-")[0])
            id = j["track"]["id"]
            title = j["track"]["name"]
            popularity = j["track"]["popularity"]
            songs.append(Songs(title, names, id, year, popularity))
    return songs