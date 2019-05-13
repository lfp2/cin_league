import json

# Change the files list here!
files = map(lambda i: 'data/matches%d.json' %i, range(1,11))

def get_json(file):
  with open(file) as f: return json.load(f)

ids = []
for file in files:
  hash = get_json(file)

  for match in hash['matches']:
    ids.append(match['gameId'])

with open('data/ids.json', 'w') as f: f.write(str(ids))

print("ID's collected successfully")