from token_manager import TokenManager
import requests,re,json,random,time
from queue import Queue
from threading import Thread
import random
genres = ["Pop","Pop","Pop","Rock","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","EDM","Chill","R&B", "Latin", "Indie", "Heavy Metal", "Rock", "Country", "Soul", "Christian","Reggae", "Classical"]
w_keys = ["placement","buy","promo","instagram","@gmail","man","vibes","promotion","submission"]

class SearchQuery():
    def __init__(self, query=""):
        self.query = query
        self.results = []
    
    def make_job(self,query=""):
        result = {}
        result["data"] = []
        words = query.split().extend(w_keys)
        if len(query.split()) > 1:
            words += [query]

        words = list(set(words))
        

        for word in words:
            num_theads = 5
            q = Queue()
            floor = random.randrange(50)
            for x in range(0,(num_theads+1)//2):
                if x == 0:
                    offset=str(0)
                else:
                    offset=str(floor+(50*x))
                url=f"https://api.spotify.com/v1/search?query={word}&type=playlist&offset={offset}&limit=49"
                q.put(url)
            for i in range(num_theads):
                worker = Thread(target=self.make_search_request, args=(q,))
                worker.setDaemon(True)
                worker.start()
            q.join()

        res_list = []
        for i in range(len(self.results)):
            if self.results[i] not in self.results[i + 1:]:
                res_list.append(self.results[i])
        result["data"] = sorted(res_list, key=lambda d: d['playlist_followers'],reverse=True) 
        return result["data"]

    def make_search_request(self,queue):
        while not queue.empty():
            url = queue.get()
            temp_result = []
            response = None
            time.sleep(random.randrange(10))
            token = TokenManager().get_token()
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}',
            }
            response = requests.get(url, headers=headers).json()
            for list in response["playlists"]["items"]:
                data = {}
                data["image_url"] = "../static/img/404_image.png"
                try:
                    data["image_url"] = list["images"][0]["url"]
                except:
                    pass
                data["playlist_id"] = list["id"]
                data["playlist_description"] = list["description"]
                data["playlist_name"] = list["name"]
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
                data["playlist_owner_id"] = list["owner"]["id"]
                data["playlist_reference"] = re.findall(r'[\w\.-]+@[\w\.-]+', data["playlist_description"])
                data["playlist_number_of_songs"] = list["tracks"]["total"]
                if self.check_active_list(data):
                    data.update(self.get_playlist_info(data["playlist_id"],headers))
                    temp_result.append(data)
            self.results += temp_result
            queue.task_done()
        return

    def check_active_list(self,data):
        if data["playlist_description"] == "" or data["playlist_reference"] == [] or data["playlist_name"] == "" or data["playlist_number_of_songs"] == 0:
            return False
        return True

    def get_playlist_info(self,id,headers):
        params = (
            ('fields','followers'),#,tracks.items(track(id))'),
        )
        response = requests.get(f'https://api.spotify.com/v1/playlists/{id}', headers=headers,params=params).json()
        # data = []
        # for track in response["tracks"]["items"]:
        #     t = {}
        #     try:
        #         t["id"] = track["track"]["id"]
        #         data.append(t)
        #     except:
        #         pass

        json = {"playlist_followers":response["followers"]["total"]}#,"playlist_tracks":data}
        return json


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
        return self.results


class SingleArtistQuery():
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
        url=f"https://api.spotify.com/v1/artists/{query}"
        response = requests.get(url, headers=self.headers).json()
        data = {}
        data["image_url"] = "../static/img/404_image.png"
        try:
            data["image_url"] = response["images"][0]["url"]
        except:
            pass
        data["artist_id"] = response["id"]
        data["artist_name"] = response["name"]
        data["followers"] = response["followers"]["total"]
        data["genres"] = response["genres"]

        #result["data"] = sorted(self.results, key=lambda d: d['playlist_followers'],reverse=True) 
        print(json.dumps(data), end='', flush=True)

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
        return data


print(SearchQuery().make_job(query="prova"))