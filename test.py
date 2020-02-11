import requests
import json
from pprint import pprint

from keys import API_KEY

headers = {
  'Accept': 'application/json',
  'AccountKey': API_KEY
}

stops_list = []
stops_dict = {}

for i in range(0,12):
  r = requests.get(f'http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={500*i}', headers=headers)
  if r.status_code == 200:
    dic = json.loads(r.content)
    
    for stop in dic['value']:
      # print(stop['BusStopCode'])
      stops_dict[stop['BusStopCode']] = {
        'stop_code': stop['BusStopCode'],
        'stop_name': stop['Description'],
        'road_name': stop['RoadName'],
        'coords': [stop['Latitude'],stop['Longitude']]
      }

noOfStops = len(stops_dict.keys())

print(noOfStops)
pprint(stops_dict)