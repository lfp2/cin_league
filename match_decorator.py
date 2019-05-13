import json
import requests

API_KEY = 'RGAPI-a5801ac5-8327-4d95-98f3-4d2906885eca'
SERVER = "br1"

def req(game_id, key):
  attributes = {
    "server": SERVER,
    "first_blood": 1,
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
              if y['killer_id'] < 6:
                attributes['inhibitor_team_2'] += 1
              else:
                attributes['inhibitor_team_1'] +=1
            if y['type'] == 'ELITE_MONSTER_KILL' and y['monsterType'] == 'DRAGON':
              if y['killer_id'] < 6:
                attributes['dragons_team_1'] += 1
              else:
                attributes['dragons_team_2'] +=1

    return attributes

with open('./data/match_ids.json') as f: ids = json.load(f)

i = 1
for id in ids:
  print('Downloading match %d out of %d' %(i,len(ids)))
  match = req(str(id), API_KEY)
  path = './data/match%d.json' %i
  if match:
    with open(path, 'w') as f: f.write(json.dumps(match))
  i += 1

# TEST ID: '1649289144'