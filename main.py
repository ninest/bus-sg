import requests
import json
from pprint import pprint

from keys import API_KEY
from bus import Bus
from file import write_file
# from bus_services import get_services
# from bus_stops import get_bus_stops

bus = Bus()

all_services = bus.get_services()
# returns a list of all bus services [14, 15, 16, ...]

services_stops = bus.get_service_stops(all_services) 
# {bus_service: [stops they stop on]}

stops_dict = bus.get_stops()

# print(stops_dict)

write_file('services_stops', services_stops)
write_file('stops_dict', stops_dict)
print('Files written.')