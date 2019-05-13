import json

# Change the files list here!
files = map(lambda i: 'data/seeded_matches%d.json' %i, range(1,11))

def get_json(file):
  with open(file) as f: return json.load(f)

def get_matches_ids():
  for file in files:
    hash = get_json(file)
    ids = map(lambda m: m['gameId'], hash['matches'])
  with open('data/seed_ids.json', 'w') as f: f.write(str(ids))

  print("ID's collected successfully")

get_matches_ids()