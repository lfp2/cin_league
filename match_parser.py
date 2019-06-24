import csv
import json
import os

matches = {}
headers = {}

def parse_body(original, headers, attr='', key=''):
  if isinstance(original, dict):
    for k, v in headers.items():
      if k not in original: original[k] = v
      if attr: new_attr = '%s_%s' %(attr, k)
      else: new_attr = '%s' %(k)
      parse_body(original[k], headers[k], new_attr, k)

  elif isinstance(original, list):
    i = 0
    if ('bans_team_1' in attr or 'bans_team_2' in attr):
      diff =  5 - len(original)
      for j in range(0, diff):
          original.append(headers[0])

    if (attr == 'participantIdentities' or attr == 'participants'):
      diff = 10 - len(original)
      if diff > 0:
        for j in range(0, diff):
          original.append(headers[0])

    for v in original:
      new_attr = '%s%d' %(attr, i)
      parse_body(v, headers[0], new_attr)
      i += 1

  else: append_if_not_exist(attr, original)

def append_if_not_exist(key, value):
  if not value: value = '-'
  matches.setdefault(key, []).append(value)

if __name__ == '__main__':
  matches_dir = 'data/matches/'

  with open('data/headers.json', 'r') as f:
    headers = json.loads(f.read())

  print('Parsing values')
  i = 0
  for filename in os.listdir(matches_dir):
    # if i > 9: break
    path = matches_dir + filename
    with open(path, 'r') as f: match = json.loads(f.read())
    parse_body(match, headers)
    i += 1

  csv_path = 'data/matches.csv'

  with open(csv_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(matches.keys())
    writer.writerows(zip(*matches.values()))