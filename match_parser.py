import csv
import json
import os

matches = {}

def parse(iterable, key=None, parent_key=None, index=None):
  if isinstance(iterable, dict):
    for k in iterable: parse(iterable[k], k, parent_key, index)
  elif isinstance(iterable, list):
    i = 1
    for value in iterable:
      parse(value, parent_key=key, index=i)
      i += 1
  else:
    attr = ''
    if parent_key == "participantIdentities": attr += "player"
    elif parent_key == "participants": attr += "participant"
    elif parent_key: attr += "%s" %parent_key
    if index: attr += "%d_" %index
    attr += key
    append_if_not_exist(attr, iterable)


def append_if_not_exist(key, value):
  if not value: value = '-'
  matches.setdefault(key, []).append(value)

if __name__ == '__main__':
  matches_dir = 'data/matches/'
  for filename in os.listdir(matches_dir):
    path = matches_dir + filename
    with open(path, 'r') as f: match = json.loads(f.read())
    parse(match)

  csv_path = 'data/matches.csv'

  with open(csv_path, 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(matches.keys())
    writer.writerows(zip(*matches.values()))