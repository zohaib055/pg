import requests
import base64
import json,random,os
from datetime import datetime,timedelta



class TokenManager():
  def __init__(self):
        self.client = [("c05b705cab814fadabf2dbe62d5ad537","72c994f702ae4e7caf30aca3f17258cc"),("7417cb74e56048d3b7f48d1c27409a99","267627ecd0244bfbbe740082a5c073bf"),("40de8e28b092413e9414d20fcb4f0bad","b0a75ec4fa2e4bddb7a888787545669f"),("ca08ff963b944500b9f1e930c49c5c21","bfe483489116479c9250ad1cc1343446")]
        c = random.choice(self.client)

        self.client_id = c[0]
        self.client_secret = c[1]
        self.mix = self.client_id + ":" + self.client_secret
        self.authorization_token = base64.b64encode(self.mix.encode("ascii")).decode("ascii")


  def get_token(self):
    try:
      with open(os.getcwd()+'/app/spotify_bridge/token/token'+self.client_id) as infile:
        token = json.load(infile)
      if datetime.strptime(token["expiry"],"%Y-%m-%d:%H:%M:%S") > datetime.now():
        return token["token"]
    except:
      pass

    status,token = self.request_new_token()
    if status:
      return token

  def request_new_token(self):
    headers = {
        'Authorization': f'Basic {self.authorization_token}',
    }

    data = {
      'grant_type': 'client_credentials'
    }

    token = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data).json()
    expiry = datetime.now() + timedelta(seconds=token["expires_in"])
    dict = {"token":token["access_token"],"expiry":expiry.strftime("%Y-%m-%d:%H:%M:%S")}
    with open(os.getcwd()+'/app/spotify_bridge/token/token'+self.client_id, 'w+') as outfile:
      json.dump(dict, outfile)

    return (True,token["access_token"])