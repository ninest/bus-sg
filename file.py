import json

def write_file(name, data):
  f = open(f'data/{name}.json', 'w')
  with f as outfile:
    json.dump(data, outfile)

def read_file(name):
  f = open(f'data/{name}.json', 'r')
  dictionary = json.loads( f.read() )
  return dictionary