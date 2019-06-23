import json
import requests
import pandas as pd
from requests import get
import time

API_KEY = 'RGAPI-94dcd487-383d-4912-8a75-ccf208e64941'
SERVER = "br1"
params = "api_key=%s" %(API_KEY)


def req(game_id, key):
  attributes = {
    "server": SERVER,
    "first_blood": -1,
    "yellow_trinket_team_1": 0,
    "yellow_trinket_team_2": 0,
    "control_ward_team_1": 0,
    "control_ward_team_2": 0,
    "undefined_ward_team_1": 0,
    "undefined_ward_team_2": 0,
    "outer_tower_team_1": 0,
    "outer_tower_team_2": 0,
    "inner_tower_team_1": 0,
    "inner_tower_team_2": 0,
    "base_tower_team_1": 0,
    "base_tower_team_2": 0,
    "inhibitor_team_1": 0,
    "inhibitor_team_2": 0,
    "dragons_team_1": 0,
    "dragons_team_2": 0
  }

  url = 'https://%s.api.riotgames.com/lol/match/v4/timelines/by-match/%s?api_key=%s' %(SERVER, game_id, key)
  res = requests.get(url)

  if res.status_code != 200:
    print('REQUEST ERROR: %d' %res.status_code)
    print(res.json()['status']['message'])
    if res.status_code == 429:
      time.sleep(100)
      req(game_id, key)
    else:
      return None
  else:
    attributes['match_id'] = game_id
    json_response = res.json()
    for x in json_response['frames']:
      if x['timestamp'] < 600276:
        for y in x['events']:
          if y['type'] == 'CHAMPION_KILL' and attributes['first_blood'] == -1:
            if y['killerId'] < 6:
              attributes['first_blood'] = 0
            else:
              attributes['first_blood'] = 1
          if y['type'] == 'WARD_PLACED':
            if y['wardType'] == 'YELLOW_TRINKET':
              if y['creatorId'] < 6:
                attributes['yellow_trinket_team_1'] += 1
              else:
                attributes['yellow_trinket_team_2'] += 1
            elif y['wardType'] == 'CONTROL_WARD':
              if y['creatorId'] < 6:
                attributes['control_ward_team_1'] += 1
              else:
                attributes['control_ward_team_2'] +=1
            elif y['wardType'] == 'UNDEFINED':
              if y['creatorId'] < 6:
                attributes['undefined_ward_team_1'] += 1
              else:
                attributes['undefined_ward_team_2'] +=1
          if y['type'] == 'BUILDING_KILL':
            if y['buildingType'] == 'OUTER_TURRET':
              if y['killer_id'] < 6:
                attributes['outer_tower_team_2'] += 1
              else:
                attributes['outer_tower_team_1'] +=1
            elif y['buildingType'] == 'INNER_TURRET':
              if y['killer_id'] < 6:
                attributes['inner_tower_team_2'] += 1
              else:
                attributes['inner_tower_team_1'] +=1
            elif y['buildingType'] == 'BASE_TURRET':
              if y['killer_id'] < 6:
                attributes['base_tower_team_2'] += 1
              else:
                attributes['base_tower_team_1'] +=1
            elif y["buildingType"] == "INHIBITOR_BUILDING":
              if "killer_id" in y.keys():
                if y['killer_id'] < 6:
                  attributes['inhibitor_team_2'] += 1
                else:
                  attributes['inhibitor_team_1'] +=1
            if y['type'] == 'ELITE_MONSTER_KILL' and y['monsterType'] == 'DRAGON':
              if "killer_id" in y.keys():
                if y['killer_id'] < 6:
                  attributes['dragons_team_1'] += 1
                else:
                  attributes['dragons_team_2'] +=1

    return attributes

matches_request = []
ds = pd.read_csv("dataset_c_id", sep="\t")
for x in ds['match_id']:
  matches_request.append(x)
i = 1

for match in matches_request:
  timeline = req(match, API_KEY)
  print('Downloading matches of %d out of %d' %(i,len(matches_request)))
  if timeline is not None:
    i += 1
    path = './data/Timeline/match_timeline%s.json' %match
    with open(path, 'w') as f: f.write(json.dumps(timeline))

