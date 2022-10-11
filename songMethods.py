class Songs:
    def __init__(self, title: str, artist: str, spotifyId: str, year: int, popularity: int) -> None:
        self.__title: str = title
        self.__artist: str = artist
        self.__spotifyId: str = spotifyId
        self.__year: int = int(year)
        self.__popularity: int = int(popularity)

    def __getTitle(self) -> str:
        return self.__title

    def __getArtist(self) -> str:
        return self.__artist

    def __getSpotifyId(self) -> str:
        return self.__spotifyId

    def __getYear(self) -> int:
        return self.__year

    def __getPopularity(self) -> int:
        return self.__popularity

    def __str__(self) -> str:
        return f"{self.artist} - {self.title} ({self.year})"

    title = property(fget=__getTitle)
    artist = property(fget=__getArtist)
    spotifyId = property(fget=__getSpotifyId)
    year = property(fget=__getYear)
    popularity = property(fget=__getPopularity)

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