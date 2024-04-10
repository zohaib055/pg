from token_manager import TokenManager
import requests,re,json,random,time,sys
from queue import Queue
from threading import Thread
import random
genres = ["Pop","Pop","Pop","Rock","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","EDM","Chill","R&B", "Latin", "Indie", "Heavy Metal", "Rock", "Country", "Soul", "Christian","Reggae", "Classical"]
w_keys = ["placement","buy","promo","instagram","@gmail","man"]

class SinglePlaylistsQuery():
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
        url=f"https://api.spotify.com/v1/playlists/{query}"
        response = requests.get(url, headers=self.headers).json()
        data = {}
        data["image_url"] = "../static/img/404_image.png"
        try:
            data["image_url"] = response["images"][0]["url"]
        except:
            pass
        data["playlist_id"] = response["id"]
        data["playlist_description"] = response["description"]
        data["playlist_reference"] = re.findall(r'[\w\.-]+@[\w\.-]+', data["playlist_description"])
        data["playlist_name"] = response["name"]
        data["playlist_genre"] = random.choice(genres)
        took = 0
        for x in genres:
            for y in data["playlist_name"].split():
                if x.lower() in y.lower():
                    data["playlist_genre"] = x
                    took = 1
                    break
        if not took:
            for x in genres:
                for y in data["playlist_description"].split():
                    if x.lower() in y.lower():
                        data["playlist_genre"] = x
                        break

        data["playlist_owner_id"] = response["owner"]["id"]
        data["playlist_number_of_songs"] = response["tracks"]["total"]
        data["playlist_followers"] = response["followers"]["total"]

        #result["data"] = sorted(self.results, key=lambda d: d['playlist_followers'],reverse=True) 
        print(json.dumps(data), end='', flush=True)


try:
    SinglePlaylistsQuery().make_job(query=sys.argv[1])
except:
    exit(0)