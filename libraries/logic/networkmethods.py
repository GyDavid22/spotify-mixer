import requests
import json
import urllib
import socket
import os
import base64

from settings import Settings
from logger import log

class DownloadHelper:
    """Static class to contain a dictionary, not to pollute the global namespace"""
    alreadyDownloaded: dict[str, list[dict]] = dict()
    """Dictionary to keep track of which playlists have been already fetched\n
    Key is the ID of the playlist, value represents a downloaded playlist"""

def upload(uris: list[str], name: str) -> None:
    """Method to upload a new generated playlist using REST API"""
    log(f"Uploading generated playlist: {name}")
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
    id = id[len(id) - 1]
    url = f"https://api.spotify.com/v1/playlists/{id}/tracks?uris="
    bottom: int = 0
    by: int = 100
    if len(uris) < by:
        top: int = len(uris)
    else:
        top: int = by
    while bottom < len(uris):
        sublist: str = ",".join(uris[bottom:top])
        res = requests.post(url + sublist, headers=header)
        if not res.status_code == 201:
            raise ValueError(res.text)
        bottom = top
        if len(uris) < top + by:
            top = len(uris)
        else:
            top += by
    log("Upload successful.")

def authenticate() -> None:
    """Method to authenticate user and get an access token"""
    log("Beginning authentication.")
    response_page = ""
    try:
        f = open("assets/succesful_authentication.html", "rt", encoding="utf-8")
        try:
            response_page = f.read()
        except:
            raise ValueError()
        finally:
            f.close()
    except OSError:
        log("Failed to load successful_authentication.html. Using hardcoded string as a fallback.")
        response_page = "You can close this window now."

     # Phase one
    url: str = "https://accounts.spotify.com/authorize"
    ip: str = "localhost"
    port: int = 54545
    headers: list[str] = [
        f"client_id={Settings.clientId}",
        "response_type=code",
        "redirect_uri=" + urllib.parse.quote(f"http://{ip}:{port}"),
        "scope=" + urllib.parse.quote("playlist-modify-public playlist-modify-private playlist-read-private user-library-read")
    ]
    url = url + "?" + "&".join(headers)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    os.system(f"cmd /c start \"\" \"{url}\"")

    (sock2, addr) = sock.accept()
    sock.close()
    response: list[str] = [ i.rstrip("\r") for i in sock2.recv(1024).decode().split("\n") ]
    sock2.send("HTTP/1.0 200 OK\n".encode())
    sock2.send("Content-Type: text/html;charset=UTF-8\n\n".encode())
    sock2.send(response_page.encode())
    sock2.close()
    get_req: list[str] = response[0].split(" ")
    code: str = get_req[1].lstrip("/?code=")

     # Phase two
    url: str = "https://accounts.spotify.com/api/token"
    data: dict[str, str] = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": f"http://{ip}:{port}"
    }
    headers: dict[str, str] = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic " + base64.b64encode((f"{Settings.clientId}:{Settings.clientSecret}").encode()).decode()
    }
    res = requests.post(url, headers=headers, data=data)
    if not res.status_code == 200:
        raise ValueError(res.text)
    Settings.token = res.json()["access_token"]
    log("Authentication successful.")

def download(playlistId: str) -> tuple[str, list[dict]]:
    """Method to download playlist from Spotify using REST API"""
    log(f"Fetching playlist: {playlistId}")
    if playlistId in DownloadHelper.alreadyDownloaded:
        return (playlistId, DownloadHelper.alreadyDownloaded[playlistId])
    if playlistId.lower() == "liked":
        url: str = "https://api.spotify.com/v1/me/tracks"
    else:
        url: str = f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"
    header: dict[str, str] = {
        "Authorization": f"Bearer {Settings.token}",
        "Content-Type": "application/json"
    }
    results: list = []
    hasNext: bool = True
    while hasNext:
        resp = requests.get(url=url, headers=header)
        if not resp.status_code == 200:
            raise ValueError(resp.text)
        respjson: dict = resp.json()
         # For some reason the responses I got weren't consistent all the time
        if "tracks" in respjson:
            respjson = respjson["tracks"]
        results.append(respjson)
        if not respjson["next"] == None:
            url = respjson["next"]
        else:
            hasNext = False
    DownloadHelper.alreadyDownloaded[playlistId] = results
    log("Fetching successful.")
    return (playlistId, results)