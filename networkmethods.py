import requests
import json
import urllib
import socket
import os

from settings import Settings

class PersistentStorage:
    alreadyDownloaded: dict[str, list[dict]] = dict()

def upload(uris: str, name: str):
    url: str = f"https://api.spotify.com/v1/users/{Settings.uid}/playlists"
    data = json.dumps({
        "name": name,
        "description": "Made with Spotify Mixer",
        "public": False
        })
    header: dict[str, str] = {
        "Authorization": f"Bearer {Settings.token}",
        "Content-Type": "application/json"
    }
    res = requests.post(url, headers=header, data=data)
    id: str = res.json()["external_urls"]["spotify"].split("/")
    id: str = id[len(id) - 1]
    url = f"https://api.spotify.com/v1/playlists/{id}/tracks?uris="
    res = requests.post(url + uris, headers=header)
    if not res.status_code == 201:
        raise ValueError(res.text)

def authenticate() -> None:
     # Phase one
    url: str = "https://accounts.spotify.com/authorize"
    ip: str = "localhost"
    port: int = 54545
    headers: list[str] = [
        f"client_id={Settings.clientId}",
        "response_type=code",
        "redirect_uri=" + urllib.parse.quote(f"http://{ip}:{port}"),
        "scope=" + urllib.parse.quote("playlist-modify-public playlist-modify-private playlist-read-private")
    ]
    url = url + "?" + "&".join(headers)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    os.system(f"cmd /c start \"\" \"{url}\"")

    (sock2, addr) = sock.accept()
    sock.close()
    response: list[str] = [ i.rstrip("\r") for i in sock2.recv(1024).decode().split("\n") ]
    code: str = ""
    for i in response:
        try:
            b = i.split(" ")
            if b[0] == "GET":
                code = b[1].lstrip("/?code=")
        except:
            pass
    sock2.send("HTTP/1.0 200 OK\n".encode())
    sock2.send("Content-Type: text/html\n\n".encode())
    sock2.send("You can close this window now.".encode())
    sock2.close()

     # Phase two
    url: str = "https://accounts.spotify.com/api/token"
    data: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"http://{ip}:{port}"
    }
    headers: dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {Settings.magic}"
    }
    res = requests.post(url, headers=headers, data=data)
    if not res.status_code == 200:
        raise ValueError(res.text)
    Settings.token = res.json()["access_token"]
    print()

def download(playlistId: str) -> list[dict]:
    if playlistId in PersistentStorage.alreadyDownloaded:
        return PersistentStorage.alreadyDownloaded[playlistId]
    url: str = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    header: dict[str, str] = {
        "Authorization": f"Bearer {Settings.token}",
        "Content-Type": "application/json"
    }
    results: list = []
    hasNext: bool = True
     # The first response is different for some reason, sometimes
    resp = requests.get(url=url, headers=header)
    if not resp.status_code == 200:
        raise ValueError(resp.text)
    respjson: dict = resp.json()
    try:
        results.append(respjson["tracks"])
        if not respjson["tracks"]["next"] == None:
            url = respjson["tracks"]["next"]
        else:
            hasNext = False
    except:
        results.append(respjson)
        if not respjson["next"] == None:
            url = respjson["next"]
        else:
            hasNext = False
    while hasNext:
        resp = requests.get(url=url, headers=header)
        if not resp.status_code == 200:
            raise ValueError(resp.text)
        respjson: dict = resp.json()
        results.append(respjson)
        if not respjson["next"] == None:
            url = respjson["next"]
        else:
            hasNext = False
    PersistentStorage.alreadyDownloaded[playlistId] = results
    return results