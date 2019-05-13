from requests import get

for i in range(1,11):
  print('Downloading JSON: %d of 10' %i)

  url = 'https://s3-us-west-1.amazonaws.com/riot-developer-portal/seed-data/matches%d.json' %i
  req = get(url)
  if req.status_code >= 400 and req.status_code < 500: print("Bad request")
  elif req.status_code >= 500: print("Server error")
  else:
    filename = 'data/matches%d.json' %i
    with open(filename, 'w') as f: f.write(req.text)

print("All JSON downloaded successfully!")
