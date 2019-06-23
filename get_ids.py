import json
import requests
import pandas as pd
from requests import get
import datetime
import time

API_KEY = 'RGAPI-f98ac3a0-c156-4667-90bf-830a711d815b'
BEGIN_TIME = "1557121151000" # May 6, 2019
SERVER = "br1"
params = "api_key=%s&beginTime=%s" %(API_KEY, BEGIN_TIME)

def req_match(game_id, key):
  attributes = {
    "server": SERVER,
  }
  url = 'https://%s.api.riotgames.com/lol/match/v4/matches/%s?api_key=%s' %(SERVER, game_id, key)
  res = requests.get(url)
  if res.status_code != 200:
    print('REQUEST ERROR: %d' %res.status_code)
    print(res.json()['status']['message'])
    if res.status_code == 429:
      time.sleep(100)
      req_match(game_id, key)
    else:
      return None
  else:
    attributes['match_id'] = game_id
    json_response = res.json()
    attributes['game_mode'] = json_response['gameMode']
    attributes['game_type'] = json_response['gameType']
    attributes['participants'] = json_response['participants']
    attributes['participantIdentities'] = json_response['participantIdentities']
    if len(json_response['teams']) == 2:
      attributes['bans_team_1'] = json_response['teams'][0]['bans']
      attributes['bans_team_2'] = json_response['teams'][1]['bans']
      if json_response['teams'][0]['win'] == "Win":
        attributes['winning_team'] = 1
      else:
        attributes['winning_team'] = 2

    return attributes

def request_matches(url):
  res = get(url)
  if res.status_code != 200:
    print('REQUEST ERROR: %d' %res.status_code)
    print(res.json()['status']['message'])
    if res.status_code == 429:
      time.sleep(1000)
      request_matches(url)
  else:
    response = res.json()
    ids = map(lambda m: m['gameId'], response['matches'])
    with open('data/match_ids.json', 'a') as f: f.write(str(ids))
    return response['matches']

id_request = ['LvCtwwSOWuSEr7WcY2wSE7cT2X504Y8Mmwxnzd0wg_yB3fk']
matches_request = []
ds = pd.read_csv("dataset_c_id", sep="\t")
for x in ds['match_id']:
  matches_request.append(x)
i = 1

for id in id_request:
  url = "https://br1.api.riotgames.com/lol/match/v4/matchlists/by-account/%s?%s" %(id, params)
  matches = request_matches(url)
  print('Downloading matches of player %s, %d out of %d' %(id,i,len(id_request)))
  i += 1
  if matches is not None:
    for match in matches:
      gameId = match['gameId']
      if gameId not in matches_request:
        print('Downloading game %s number %d' %(gameId,len(matches_request)))
        attributes = req_match(gameId, API_KEY)
        if attributes is not None:
          matches_request.append(gameId)
          participants = attributes['participantIdentities']
          path = './data/match%s.json' %gameId
          if attributes:
            with open(path, 'w') as f: f.write(json.dumps(attributes))
          for participant in participants:
            if participant['player']['currentAccountId'] not in id_request:
              if len(id_request) < 100:
                id_request.append(participant['player']['currentAccountId'])

with open('data/ids_requested.json', 'w') as f: f.write(str(id_request))

