import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

from tqdm import tqdm

from keys import API_KEY


class Bus:
  """
  Service: 
  A bus service, identified by it's number. 14, 16, 222, 137 are all bus services.

  Stop: 
  A bus stop
    - Stop code (or just code): A bus stop's 6-digit code. 
    - Stop name: A bus stop's name
    - Stop road?: The road on which a stop is

  Route:
  The list of stops a bus takes

  All services and stops will be in the string format here so it can be used as the key in JSON/dictionary.
  """

  def __init__(self):
    # self.headers = 
    pass

  def get_services(self) -> list:
    """ Get a list of bus services and return a list: ["2", "3", "4", "4a", ...] """

    r = requests.get('https://landtransportguru.net/bus/bus-services/')
    if r.status_code == 200:
      soup = BeautifulSoup(r.content, 'lxml')

      services_list = []
      
      for service_soup in soup.find_all("div", class_='vrouterow'):
        service = service_soup.find("span", class_='vnumber').text
        
        # These are not bus stops, they are just the general starting and ending areas
        # starting_point = service_soup.find("span", class_='vdest1').text
        # ending_point = service_soup.find("span", class_='vdest1').text
        # Not sure if we should use them yet

        services_list.append(service)
      
      return services_list
  
  def get_stops_for_each_service(self, services_list):
    """ Long name, but it's descriptive. SELF-DOCUMENTING CODE! """
    """
      Getting a list of routes for each bus service (in order)
        - each route will include only the stop_codes

    """
    # Test data: 14 (2 ways), 222 (loop), nr5 (1 way, not loop)

    services_stops_dict = {}

    for service in services_list:
      r = requests.get(f'https://landtransportguru.net/bus{service}/')
      if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')

        services_stops_dict[service] = {}

        # initialize an empty array for the stops in the service
        services_stops_dict[service]['routes'] = []

        # we can check if the bus service route is a loop (only 1 way) if the "RouteDesti" has "loop" in it
        route_name = soup.find('div', class_='RouteDesti').text
        if "loop" in route_name.lower():
          loop = True  # loops are 222, 228
        else: 
          loop = False
        services_stops_dict[service]['loop'] = loop

        # loop through all routes (dir1, dir2)
        # array 1 and 2 because each bus has a maximum of two routes
        for dir_no, route_soup in zip([1,2], soup.find('div', class_='RouteContainer')):

          route = []
          for stop_soup in route_soup.find_all('div', class_='NodeContainer'):
            stop_code = stop_soup.find('div', class_='NodeID').text
            # stop_name = stop_soup.find('div', 'NodeName').text
            # stop_road = stop_soup.find('div', 'NodeRoadName').text

            route.append(stop_code)
          
          if loop == False:
            # When it's NOT a loop, it's eaither
            try: 
              # (1) A bus with a 2 routes (like 14)
              route_name = soup.find(id=f'navdir{dir_no}').text .split(':')[1]
            except:
              # (2) 1-way, no loop (like NR5)
              route_name = soup.find('div', class_='RouteDesti').text
          
          services_stops_dict[service]['routes'].append({
            'name': route_name,
            'stops': route
          })


    
    return services_stops_dict


# Bus().get_stops_for_each_service(["14", "222", "NR5"])
# pprint(
#   Bus().get_stops_for_each_service(["14", "222", "NR5"])
# )
pprint(
  Bus().get_stops_for_each_service(["14",])
)