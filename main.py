import requests
import json
from pprint import pprint

from keys import API_KEY
from bus_services import get_services
from bus_stops import get_bus_stops

all_services = get_services()
# returns a list of all bus services [14, 15, 16, ...]

services_stops = get_bus_stops(all_services) 
# {bus_service: [stops they stop on]}

f = open('data/services_stops.json', 'w')
with f as outfile:
  json.dump(services_stops, outfile)