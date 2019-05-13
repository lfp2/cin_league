from requests import get
import datetime

API_KEY = "RGAPI-8aeaca9b-6e1a-4bbc-b64b-99215ab1153"
BEGIN_TIME = "1557121151000" # May 6, 2019
ACCOUNT_ID = "1649289144"

params = "api_key=%s&beginTime=%s" %(API_KEY, BEGIN_TIME)
url = "https://br1.api.riotgames.com/lol/match/v4/matchlists/by-account/%s?%s" %(ACCOUNT_ID, params)

def request_matches():
  res = get(url)
  if res.status_code != 200:
    print('REQUEST ERROR: %d' %res.status_code)
    print(res.json()['status']['message'])
  else:
    response = res.json()
    ids = map(lambda m: m['gameId'], hash['matches'])
    with open('data/match_ids.json', 'w') as f: f.write(str(ids))

request_matches()