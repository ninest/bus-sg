import os
import json
from pathlib import Path


def write_file(data, folder, filename):
  # create directory if doesm't exist
  if not os.path.exists(f'output/{folder}'):
    os.makedirs(f'output/{folder}')

  f = open(f'output/{folder}/{filename}.json', 'w')
  with f as outfile:
    json.dump(data, outfile)


def read_file(folder, filename):
  f = open(f'output/{folder}/{filename}', 'r')
  dictionary = json.loads(f.read())
  return dictionary


def exists(folder, filename):
  p = Path(f'output/{folder}/{filename}').is_file()
  return p
