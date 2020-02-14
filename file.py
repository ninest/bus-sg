import os
import json

def write_file(data, folder, filename):
  # create directory if doesm't exist
  if not os.path.exists(f'output/{folder}'):
    os.makedirs(f'output/{folder}')
    
  f = open(f'output/{folder}/{filename}.json', 'w')
  with f as outfile:
    json.dump(data, outfile)

def read_file(folder, filename):
  f = open(f'output/{folder}/{filename}.json', 'r')
  dictionary = json.loads( f.read() )
  return dictionary