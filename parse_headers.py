
def in_list(d, l):
  if isinstance(d, dict):
    for v in l:
      if set(d.keys()) == set(d.keys()): return True
    return False
  else: return d in l

def empty_value(value):
  if isinstance(value, dict): return {}
  elif isinstance(value, list): return []
  return '-'

def parse_headers(original, copy):
  if isinstance(original, dict):
    for key, value in original.items():
      if not key in copy: copy[key] = empty_value(value)
      parse_headers(original[key], copy[key])

  elif isinstance(original, list):
    for value in original:
      if not in_list(value, copy): copy.append(empty_value(value))
      parse_headers(value, copy[len(copy)-1])

  else: copy = '-'