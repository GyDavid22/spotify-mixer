import json
import requests
from settings import Settings

def loadResps() -> list[dict]:
    filenums: int = 24
    resps = []
    for i in range(filenums):
        with open(f"resps\\{i}.json", "rt", encoding="utf-8") as f:
            resps.append(json.loads(f.read()))
    return resps

def getToken() -> str:
    url: str = "https://accounts.spotify.com/api/token"
    headers: dict[str, str] = {
        'grant_type': 'client_credentials',
        'client_id': Settings.clientId,
        'client_secret': Settings.clientSecret,
    }
    res: json = requests.post(url, headers).json()
    return res["access_token"]

def req() -> list[dict]:
    token: str = getToken()
    url: str = f"https://api.spotify.com/v1/playlists/{Settings.pid}/tracks"
    header: dict[str, str] = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    results: list = []
    hasNext: bool = True
    query: str = f"?offset={0}&limit={50}"
    dynamicUrl: str = url + query
    while hasNext:
        resp = requests.get(url=dynamicUrl, headers=header)
        if not resp.status_code == 200:
            raise ValueError(resp.text)
        respjson = resp.json()
        results.append(respjson)
        if not respjson["next"] == None:
            dynamicUrl = respjson["next"]
        else:
            hasNext = False
    return results

def toFile(results: list[dict]):
    for i in range(len(results)):
        with open(f"resps\\{i}.json", "wt", encoding="utf-8") as f:
            f.write(json.dumps(results[i]))