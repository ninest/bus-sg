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

from file import read_file

services_stops = read_file('services_stops')
stops_dict = read_file('stops_dict')

for key in services_stops.keys():
  for stop_codes in services_stops[key]:
    print(stop_codes)