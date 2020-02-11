import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_bus_stops(bus_services):
  stops = {}
  for service in bus_services:
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

