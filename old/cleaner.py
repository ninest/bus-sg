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
(2) Loop through the bus services (services.stops.keys())
(3) Loop through each of the stations codes of the bus services (see services_stops.json)
(4) Edit the stops dictionary, and append the bus service in the "bus_services" list

It is more than likely that the same bus will be added to a stop multiple times (eg: Both 14 and 16 go to Bedok Interchange).

Therefore we must check if the bus stop has ALREADY been added to the bus_services list (if statement used).
"""
import json
from pprint import pprint

from file import read_file

services_stops = read_file('services_stops')
stops_dict = read_file('stops_dict')

for bus_service in services_stops.keys():
  for stop_code in services_stops[bus_service]:
    
    try: 
      # only add the bus service if it hasn't already been added
      if not bus_service in stops_dict[stop_code]['bus_services']:
        stops_dict[stop_code]['bus_services'].append(bus_service)
      else:
        print('ALREADY THERE')
        print(bus_service)
        print(stop_code)
        print()
    except:
      # new key being created if it doesn't exist
      stops_dict[stop_code]['bus_services'] = [bus_service]

pprint(stops_dict)