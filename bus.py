import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

from tqdm import tqdm

from keys import API_KEY


class Bus:
  def __init__(self):
    self.headers = headers = {
      'Accept': 'application/json',
      'AccountKey': API_KEY
    }

  def get_services(self) -> list:
    r = requests.get('https://www.mytransport.sg/content/mytransport/map.html')
    if r.status_code == 200:
      bus_services = []

      soup = BeautifulSoup(r.content, 'lxml')
      options = soup.find(id='busservice_option')
      for optgroup in options.find_all('optgroup'):
        for option in optgroup.find_all('option'):
          bus_services.append(option.text)
      return bus_services
  
  def get_service_stops(self, bus_services) -> dict:
    stops = {}
    for service in tqdm(bus_services):
      r = requests.get(f'https://www.mytransport.sg/content/mytransport/ajax_lib/map_ajaxlib.getBusRouteByServiceId.{service}.html', headers={'User-Agent': 'request'})
      if r.status_code == 200:
        service_stops = []
        soup = BeautifulSoup(r.content, 'lxml')

        for line in soup.find_all("div", {"class": "bus_stop_code"},):
          try:
            bus_stop_code = int(line.text)
            service_stops.append(bus_stop_code)
          except:
            pass      
        stops[service] = service_stops

    return stops

  def get_stops(self) -> dict:
    # stops_list = []
    stops_dict = {}

    for i in tqdm(range(0,12)):
      r = requests.get(f'http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={500*i}', headers=self.headers)
      if r.status_code == 200:
        dic = json.loads(r.content)
        
        for stop in dic['value']:
          stops_dict[stop['BusStopCode']] = {
            'stop_code': stop['BusStopCode'],
            'stop_name': stop['Description'],
            'road_name': stop['RoadName'],
            'coords': [stop['Latitude'],stop['Longitude']]
          }

    # noOfStops = len(stops_dict.keys())

    return stops_dict


