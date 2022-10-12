import json
import requests
from settings import Settings

def upload(uris: str, name: str):
    url: str = f"https://api.spotify.com/v1/users/{Settings.uid}/playlists"
    data = json.dumps({
        "name": name,
        "description": "Made by PyMixer!",
        "public": False
        })
    header: dict[str, str] = {
        "Authorization": f"Bearer {Settings.wtoken}",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=header, data=data)
    id = res.json()["external_urls"]["spotify"].split("/")
    id = id[len(id) - 1]
    url = f"https://api.spotify.com/v1/playlists/{id}/tracks?uris="
    res = requests.post(url + uris, headers=header)

def getToken() -> str:
    return Settings.rtoken
    url: str = "https://accounts.spotify.com/api/token"
    headers: dict[str, str] = {
        'grant_type': 'client_credentials',
        'client_id': Settings.clientId,
        'client_secret': Settings.clientSecret,
    }
    res: dict = requests.post(url, headers).json()
    return res["access_token"]

def req(playlistId: str) -> list[dict]:
    token: str = getToken()
    url: str = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    header: dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    results: list = []
    hasNext: bool = True
    query: str = f"?offset=0&limit=50"
    dynamicUrl: str = url + query
    while hasNext:
        resp = requests.get(url=dynamicUrl, headers=header)
        if not resp.status_code == 200:
            raise ValueError(resp.text)
        respjson: dict = resp.json()
        results.append(respjson)
        if not respjson["next"] == None:
            dynamicUrl = respjson["next"]
        else:
            hasNext = False
    return results

def loadResps() -> list[dict]:
    filenums: int = 24
    resps = []
    for i in range(filenums):
        with open(f"resps\\{i}.json", "rt", encoding="utf-8") as f:
            resps.append(json.loads(f.read()))
    return resps

def toFile(results: list[dict]):
    for i in range(len(results)):
        with open(f"resps\\{i}.json", "wt", encoding="utf-8") as f:
            f.write(json.dumps(results[i]))