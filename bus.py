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
    - Stop road: The road on which a stop is

  Route:
  The list of stops a bus takes

  All services and stops will be in the string format here so it can be used as the key in JSON/dictionary.
  """

  def __init__(self):
    self.headers = { 'Accept': 'application/json', 'AccountKey': API_KEY }

  
  def get_services(self) -> list:
    """ Get a list of bus services and return a list: ["2", "3", "4", "4a", ...] """

    r = requests.get('https://landtransportguru.net/bus/bus-services/')
    if r.status_code == 200:
      soup = BeautifulSoup(r.content, 'lxml')

      services_list = []
      
      print('Getting all bus services (LTG):')
      for service_soup in tqdm(soup.find_all("div", class_='vrouterow')):
        service = service_soup.find("span", class_='vnumber').text
        
        # These are not bus stops, they are just the general starting and ending areas
        # starting_point = service_soup.find("span", class_='vdest1').text
        # ending_point = service_soup.find("span", class_='vdest1').text
        # Not sure if we should use them yet

        services_list.append(service)
      
      return services_list
  
  
  def get_stops_for_each_service(self, services_list) -> dict:
    """ Long name, but it's descriptive. SELF-DOCUMENTING CODE! """
    """
      Getting a list of routes for each bus service (in order)
        - each route will include only the stop_codes

    """
    # Test data: 14 (2 ways), 222 (loop), nr5 (1 way, not loop)

    services_stops_dict = {}

    print('Getting all bus stops for each bus service (LTG):')
    for service in tqdm(services_list):
      r = requests.get(f'https://landtransportguru.net/bus{service}/')
      if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')

        services_stops_dict[service] = {}

        # initialize an empty array for the stops in the service
        services_stops_dict[service]['routes'] = []

        # we can check if the bus service route is a loop (only 1 way) if the "RouteDesti" has "loop" in it
        route_name = soup.find('div', class_='RouteDesti').text
        if "loop" in route_name.lower():
          route_type = '0'  # route type are 0 or 1 or 2 (loop, 1 way OR 2 way)
          dirs = [1]
        else: 
          # route name has to be set differently
          # route type can be '1' or '2'
          # dirs can be [1] or [1,2]

          # check if the navswitch button exists
          if soup.find(id='navswitch2'):
            route_type = '2'
            dirs = [1,2]
          else:
            # navswitch does NOT exist, so it's 1-way
            route_type = '1'
            dirs = [1]

          # also need to change the name accordingly
          # this will be done in the loop

        for dir_no in dirs:
          dir_soup = soup.find(id=f'dir{dir_no}')
          stop_soup = dir_soup.find_all(class_='NodeContainer')
          
          route = []  # contains a list of stop codes

          for stop in stop_soup:
            stop_code = stop.find(class_='NodeID').text
            route.append(stop_code)

          
          # fix the route name when there are 2 dirs
          if dirs == [1,2]: 
            # Getting the text on the right of "Direction X:"
            route_name = soup.find(id=f'navdir{dir_no}').text .split(':')[1]

            # remove the last 2 chars (" ⇋")
            route_name = route_name[0:-2]

          services_stops_dict[service]['routes'].append({
            'name': route_name,
            'stops': route
          })

        services_stops_dict[service]['type'] = route_type

    return services_stops_dict

  
  def get_all_stops(self) -> dict:
    all_stops_dict = {}

    # Use LTA API
    print('Getting all bus stop data (LTA):')
    for i in tqdm(range(0,11)):
      r = requests.get(f"http://datamall2.mytransport.sg/ltaodataservice/BusStops?$skip={i*500}", headers=self.headers)
      if r.status_code == 200:
        stop_list = json.loads(r.content)['value']  # this does not contain ALL stops, just 500

        for stop_dict in stop_list:
          stop_code = stop_dict['BusStopCode']
          stop_road = stop_dict['RoadName']
          stop_name = stop_dict['Description']
          stop_coords = {
            'lat': stop_dict['Latitude'],
            'lon': stop_dict['Longitude'],
          }

          all_stops_dict[stop_code] = {
            'code': stop_code,
            'name': stop_name,
            'road': stop_road,
            'coords': stop_coords,
            'mrt_stations': []  # this will be populated later or left empty
          }

    print('Number of bus stops: ')
    print(len(all_stops_dict.keys()))

    return all_stops_dict

  
  def combine_stops_and_services(self, services_stops_dict, all_stops_dict) -> dict:
    """
    example data
    services_stops_dict = {'14': {'routes': [{'name': ' Bedok Int → Clementi Int ⇋', 'stops': ['84009', '84359', '84211', '84221', '84231', '84241', '84281', '84061', '85091', '85049', '85039', '85029', '85019', '94079', '94069', '94059', '94049', '94089', '94039', '94029', '94019', '93099', '93089', '93079', '93069', '93059', '92159', '92149', '92139', '92129', '92119', '92109', '92099', '91079', '91069', '91059', '91049', '91091', '80271', '80141', '80219', '80169', '80159', '04111', '04121', '08041', '08031', '08111', '08121', '09059', '09022', '13199', '13159', '13069', '13059', '10519', '10389', '10379', '10081', '10091', '10101', '10111', '10131', '11519', '18041', '18131', '18101', '18121', '18141', '11361', '11191', '19011', '19021', '19031', '19041', '17151', '17161', '17171', '17009']}, {'name': ' Clementi Int → Bedok Int ⇋', 'stops': ['17009', '17239', '17159', '19049', '19039', '19029', '19019', '11199', '11369', '18149', '18129', '18109', '18049', '11511', '11019', '10139', '10119', '10109', '10099', '10089', '10371', '10381', '13051', '13063', '13141', '13191', '09048', '09038', '08138', '08057', '08069', '04179', '02049', '80151', '80161', '80211', '80149', '80279', '91099', '91041', '91051', '91061', '91071', '92091', '92101', '92111', '92121', '92131', '92141', '92151', '93051', '93061', '93071', '93081', '93091', '94011', '94021', '94031', '94041', '94051', '94061', '94071', '85021', '85031', '85041', '85099', '84069', '84289', '84249', '84239', '84229', '84219', '84351', '84009']}], 'loop': False, 'type': '2'}, '222': {'routes': [{'name': 'Bedok Int ↺ Chai Chee Dr (Loop)', 'stops': ['84009', '84359', '84211', '84221', '84231', '84241', '84281', '84059', '84049', '84039', '84029', '84641', '84559', '84569', '84579', '84589', '84011', '84021', '84031', '84041', '84051', '84289', '84249', '84239', '84229', '84219', '84351', '84009']}], 'loop': True, 'type': '1'}}
    {'14': {'routes': [['stop': [1,2,3]],[['stop': [4,5,6]]]}}
    all_stops = {'01012': {'code': '01012', 'name': 'Hotel Grand Pacific', 'road': 'Victoria St', 'coords': {'lat': 1.29684825487647, 'lon': 103.85253591654006}}, '01013': {'code': '01013', 'name': "St. Joseph's Ch", 'road': 'Victoria St', 'coords': {'lat': 1.29770970610083, 'lon': 103.8532247463225}},}
    """

    for service in services_stops_dict.keys():
      routes = services_stops_dict[service]['routes']
      for route in routes:
        for stop in route['stops']:

          if stop in all_stops_dict.keys():
            # one of the stops seems to be null, so add this for safety

            # we have the `stop`, so now add this bus service to the stop's 'services' list through the key 'services
            # print(all_stops[stop])
            try:
              # Don't want to add doubles
              if not service in all_stops_dict[stop]['services']:
                all_stops_dict[stop]['services'].append(service)
            
            except:
              all_stops_dict[stop]['services'] = [service]

    combined_stops_and_services_dict = all_stops_dict
    return combined_stops_and_services_dict

  
  def add_mrt_data(self, combined_stops_and_services_dict, mrt_stations) -> dict:
    """
    (1) Go through all mrt_lines
    (2) Go through each station
      - scrape bus interchange if available (on LTG) – this requires a little extra work, possibly some string operations :/
      - scrape other bus codes
      DONE IN MRT.py
    """

    all_bus_stops = combined_stops_and_services_dict  # to make it easier to read

    for station in mrt_stations.keys():
      # sorting it so we can do some checking and make sure doubles are not added
      station_refs = sorted(mrt_stations[station]['refs'])  

      for bus_stop_code in mrt_stations[station]['bus_stops']:
        try: 
          # don't want to add doubles
          if not station_refs in all_bus_stops[bus_stop_code]['mrt_stations']:
            all_bus_stops[bus_stop_code]['mrt_stations'].append(station_refs)
        except:
          try: 
            all_bus_stops[bus_stop_code]['mrt_stations'] = [station_refs]

          except: 
            # GHOST BUS STOP ERROR?
            # 22579, 65211, 22579
            print(f'Error with {bus_stop_code} at {station}')

    return all_bus_stops