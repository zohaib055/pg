from token_manager import TokenManager
import requests,re,json,random,time,sys
from queue import Queue
from threading import Thread
import random
genres = ["Pop","Rock","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","Rap","Hip-Hop","Trap","EDM","Chill","R&B", "Latin", "Indie", "Heavy Metal", "Rock", "Country", "Soul", "Christian","Reggae", "Classical"]
w_keys = ["placement","buy","promo","instagram","@gmail","man","submission","promotion","songs","viral","music"]

class SearchQuery():
    def __init__(self, query=""):
        self.query = query
        self.results = []
    
    def make_job(self,query=""):
        result = {}
        result["data"] = []
        words = [query] 
        random.shuffle(w_keys)
        for x in w_keys:
            words.append(query + " " + x)

        
        if len(query.split()) > 1:
            words += [query]

        words = list(set(words))
        
        print(words, end='',file = sys.stderr, flush=True)
        q = Queue()
        for word in words:
            for x in range(0,5):
                if x == 0:
                    offset=str(0)
                else:
                    offset=str((50*x))
                url=f"https://api.spotify.com/v1/search?query={word}&type=playlist&offset={offset}&limit=49"
                q.put(url)
        print(len(list(q.queue)), end='',file = sys.stderr, flush=True)
        num_theads = 5
        for i in range(num_theads):
            worker = Thread(target=self.make_search_request, args=(q,))
            worker.setDaemon(True)
            worker.start()
        q.join()
        return

    def make_search_request(self,queue):
        while not queue.empty():
            print("LEN:",len(list(queue.queue)),"\n", end='',file = sys.stderr, flush=True)
            try:
                url = queue.get()

                temp_result = []
                response = None
                time.sleep(random.randrange(10))
                token = TokenManager().get_token()
                print(token, end='',file = sys.stderr, flush=True)

                headers = {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {token}',
                }
                response = requests.get(url, headers=headers).json()
                print("LIST:",len(response["playlists"]["items"]), end='',file = sys.stderr, flush=True)
                for list2 in response["playlists"]["items"]:
                    data = {}
                    data["image_url"] = "../static/img/404_image.png"
                    try:
                        data["image_url"] = list2["images"][0]["url"]
                    except:
                        pass
                    data["playlist_id"] = list2["id"]
                    data["playlist_description"] = list2["description"]
                    data["playlist_name"] = list2["name"]
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
                    data["playlist_owner_id"] = list2["owner"]["id"]
                    data["playlist_reference"] = re.findall(r'[\w\.-]+@[\w\.-]+', data["playlist_description"])
                    data["playlist_number_of_songs"] = list2["tracks"]["total"]
                    if self.check_active_list(data):
                        data.update(self.get_playlist_info(data["playlist_id"],headers))
                        temp_result.append(data)
                        print(json.dumps(data), end='', flush=True)
                self.results += temp_result
                queue.task_done()
            except Exception as e:
                print(e, end='',file = sys.stderr, flush=True)
                continue
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

try:
    SearchQuery().make_job(query=sys.argv[1])
except Exception as e:
    print(e, end='',file = sys.stderr, flush=True)
    exit(0)