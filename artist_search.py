from token_manager import TokenManager
import requests,re,json,random,time,sys
from queue import Queue
from threading import Thread
import random
genres = ["Pop","Pop","Pop","Rock","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","EDM","Chill","R&B", "Latin", "Indie", "Heavy Metal", "Rock", "Country", "Soul", "Christian","Reggae", "Classical"]
w_keys = ["placement","buy","promo","instagram","@gmail","man"]


class ArtistQuery():
    def __init__(self, query=""):
        self.query = query
        self.token = TokenManager().get_token()
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }
        self.results = []
    
    def make_job(self,query=""):

        url=f"https://api.spotify.com/v1/search?query={query}&type=artist&limit=5"
        response = requests.get(url, headers=self.headers).json()
        for list in response["artists"]["items"]:
            data = {}
            data["image_url"] = "../static/img/404_image.png"
            try:
                data["image_url"] = list["images"][0]["url"]
            except:
                pass
            data["artist_id"] = list["id"]
            data["artist_name"] = list["name"]
            data["followers"] = list["followers"]["total"]
            data["genres"] = list["genres"]
            self.results.append(data)

        #result["data"] = sorted(self.results, key=lambda d: d['playlist_followers'],reverse=True) 
        print(json.dumps(self.results), end='', flush=True)
try:
    ArtistQuery().make_job(query=sys.argv[1])
except:
    exit(0)