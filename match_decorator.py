import json
import requests

def req(id_game, key):
    first_blood = -1
    yellow_trinket_team_1 = 0
    yellow_trinket_team_2 = 0
    control_ward_team_1 = 0
    control_ward_team_2 = 0
    undefined_ward_team_1 = 0
    undefined_ward_team_2 = 0
    outer_tower_team_1 = 0 ##quantas o time já derrubou
    outer_tower_team_2 = 0
    inner_tower_team_1 = 0
    inner_tower_team_2 = 0
    base_tower_team_1 = 0
    base_tower_team_2 = 0
    inhibitor_team_1 = 0
    inhibitor_team_2 = 0
    dragons_team_1 = 0
    dragons_team_2 = 0

    response = requests.get('https://br1.api.riotgames.com/lol/match/v4/timelines/by-match/'+id_game+'?api_key='+key)
    if response:
        json_response = response.json()
        for x in json_response['frames']:
            if x['timestamp'] < 600276:
                for y in x['events']:
                    if y['type'] == 'CHAMPION_KILL' and first_blood == -1:
                        if y['killerId'] < 6:
                                first_blood = 0
                        else:
                                first_blood = 1
                    if y['type'] == 'WARD_PLACED':
                        if y['wardType'] == 'YELLOW_TRINKET':
                            if y['creatorId'] < 6:
                                yellow_trinket_team_1 += 1
                            else:
                                yellow_trinket_team_2 += 1
                        elif y['wardType'] == 'CONTROL_WARD':
                            if y['creatorId'] < 6:
                                control_ward_team_1 += 1
                            else:
                                control_ward_team_2 +=1
                        elif y['wardType'] == 'UNDEFINED':
                            if y['creatorId'] < 6:
                                undefined_ward_team_1 += 1
                            else:
                                undefined_ward_team_2 +=1
                    if y['type'] == 'BUILDING_KILL':
                        if y['buildingType'] == 'OUTER_TURRET':
                            if y['killer_id'] < 6:
                                outer_tower_team_2 += 1
                            else:
                                outer_tower_team_1 +=1
                        elif y['buildingType'] == 'INNER_TURRET':
                            if y['killer_id'] < 6:
                                inner_tower_team_2 += 1
                            else:
                                inner_tower_team_1 +=1
                        elif y['buildType'] == 'BASE_TURRET':
                            if y['killer_id'] < 6:
                                base_tower_team_2 += 1
                            else:
                                base_tower_team_1 +=1
                        elif y["buildingType"] == "INHIBITOR_BUILDING":
                            if y['killer_id'] < 6:
                                inhibitor_team_2 += 1
                            else:
                                inhibitor_team_1 +=1
                    if y['type'] == 'ELITE_MONSTER_KILL' and y['monsterType'] == 'DRAGON':
                        if y['killer_id'] < 6:
                                dragons_team_1 += 1
                        else:
                                dragons_team_2 +=1

        return {'yellow_trinket_team_1': yellow_trinket_team_1,
                'yellow_trinket_team_2': yellow_trinket_team_2,
                'control_ward_team_1': control_ward_team_1,
                'control_ward_team_2': control_ward_team_2,
                'undefined_ward_team_1': undefined_ward_team_1,
                'undefined_ward_team_2': undefined_ward_team_2,
                'outer_tower_team_1': outer_tower_team_1,
                'outer_tower_team_2': outer_tower_team_2,
                'inner_tower_team_1': inner_tower_team_1,
                'inner_tower_team_2': inner_tower_team_2,
                'base_tower_team_1': base_tower_team_1,
                'base_tower_team_2': base_tower_team_2,
                'inhibitor_team_1': inhibitor_team_1,
                'inhibitor_team_2': inhibitor_team_2,
                'first_blood': first_blood,
                'dragons_team_1': dragons_team_1,
                'dragons_team_2': dragons_team_2}