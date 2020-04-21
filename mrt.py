import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
from tqdm import tqdm

from file import read_file


class MRT:
  """
  Station: An MRT station
    - Name: The name of a station (string)
    - Refs: List of station reference IDs
  """

  def __init__(self):
    self.lines = ['ns', 'ew', 'ne', 'cc', 'dt']  # add LRT later
    # same data for these incomplete so adding them
    self.future_lines = ['te', 'jr', 'cr']
    # self.lines = ['ew']

  def get_stations(self):
    """
    The keys in the stations dictionary will be the ref for that station in that line.
    Yes, there will be repeats (Dhoby Ghaut will be there thrice, for example). Not sure if this is the best way, subject to change

    This function will also find bus stops at/around the station
    """

    stations_dict = {}

    print('Getting all MRT station data (LTG): ')
    for line in tqdm(self.lines):
      r = requests.get(f'https://landtransportguru.net/train/{line}l/')
      if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'lxml')

        list_items_soup = soup.find_all('li')
        for station_soup in list_items_soup:
          # there are various lists, so we need to filter out the text content list from the MRT station list
          if station_soup.find(class_='mrt'):

            # finding the mrt station code (ex: ew5)
            refs_soup = station_soup.find_all(class_='mrt')

            station_refs = []
            for each_ref_soup in refs_soup:
              # lower case for consistency, and remove trailing spaces
              ref = each_ref_soup.text.lower().strip()

              # TODO: change this when the new MRT data is ready
              # for now, while finding all station codes, don't add future lines
              for line in self.future_lines:
                if line in ref:
                  break
                else:
                  # make sure they're not added if already there
                  if (not ref in station_refs):
                    station_refs.append(ref)

            # get station name
            station_name = station_soup.find('a').text

            # find bus stops
            station_bus_stops = self.get_station_bus_stops(station_name)

            stations_dict[station_refs[0]] = {
                'name': station_name,
                'refs': station_refs,
                'bus_stops': station_bus_stops
            }

    return stations_dict

  def get_station_bus_stops(self, station_name):
    # get the bus stop codes
    # get the interchange code (little more tricky because LTG does not provide it)

    bus_stop_codes = []

    slugified_station_name = station_name.replace(' ', '-').lower()

    r = requests.get(
        f'https://landtransportguru.net/{slugified_station_name}-station/')
    if r.status_code == 200:
      soup = BeautifulSoup(r.content, 'lxml')

      table_cell_soup = soup.find_all('td')
      for cell_soup in table_cell_soup:

        # (1) Find bus stop codes. We need to go through all table cells and see if the first 5 digits are numbers
        try:
          # checking if the first 5 digits can be ints. If yes, they are the bus stop codes
          # just for safety, we'll also check that the "–" character is present

          int(cell_soup.text[0:5])

          if "–" in cell_soup.text:
            stop_code = cell_soup.text[0:5]

            # Make sure not to add a None
            # Make sure not to add if it's already there
            if stop_code and stop_code not in bus_stop_codes:
              bus_stop_codes.append(stop_code)

              next

        except:
          pass

        # (2) Find if interchange
        a_soup = cell_soup.find('a')
        if a_soup and "interchange" in a_soup.text .lower():
          bus_stop_name = a_soup.text .lower() .replace("interchange", "int").replace(" bus", "").replace(
              "temporary", "temp").replace("bukit", "bt")  # bukit is hortened to bt in bus stop names

          # print(bus_stop_name)

          # go through temporary/all_stops_dict.json (or combined) and find the code matching the name
          all_bus_stops_dict = read_file('temp/bus', 'all_stops_dict.json')

          for bus_stop in all_bus_stops_dict.keys():
            if bus_stop_name == all_bus_stops_dict[bus_stop]['name'].lower():
              # match found :)
              stop_code = all_bus_stops_dict[bus_stop]['code']
              if stop_code not in bus_stop_codes:
                bus_stop_codes.append(stop_code)

      return bus_stop_codes
    else:
      # return empty list if error
      return []

# pprint(
# MRT().get_stations()
# )
