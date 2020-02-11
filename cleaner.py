"""
We have services_stops.json and stops_dict.json:

services_stops.json:
  {
    "X": [
      "YYYYYY",
      "YYYYYY",
    ]
  }

(X = bus number, YYYYYY = stop code)

stops_dict.json:
  {
    "YYYYYY": {
      stop_code,
      stop_name,
      road_name,
      coords
    }
  }

We want to:
(1) Take stops_dict.json and add another field to each value (bus_services)
(2) Generaate stop_dict, but as an array

Steps:
(1) Load both the json files as dictionaries

"""
import json
from pprint import pprint

from file import read_file

services_stops = read_file('services_stops')
stops_dict = read_file('stops_dict')

for bus_service in services_stops.keys():
  for stop_codes in services_stops[bus_service]:
    
    # new key
    try: 
      if bus_service in stops_dict[stop_codes]['bus_services']:
        pass
      else:
        stops_dict[stop_codes]['bus_services'].append(bus_service)
    except:
      stops_dict[stop_codes]['bus_services'] = [bus_service]
    # try: print(stops_dict[stop_codes])
    # except: print(stops_dict["0" + stop_codes])

pprint(stops_dict)