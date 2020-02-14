from pathlib import Path
from pprint import pprint

from bus import Bus
from mrt import MRT
from file import write_file, read_file, exists

b = Bus()
m = MRT()

print("Writing temporary data files ...")

# BUS
# nand because always need to write files unless both are there
if not ( exists('temp/bus', 'services_stops_dict.json') and exists('temp/bus', 'all_stops_dict.json') ):
  print("- Writing BUS files ...")
  all_services = b.get_services()
  services_stops_dict = b.get_stops_for_each_service(all_services)
  write_file(services_stops_dict, 'temp/bus', 'services_stops_dict')

  all_stops_dict = b.get_all_stops()
  write_file(all_stops_dict, 'temp/bus', 'all_stops_dict')
  print("- BUS files written")

# MRT
if not ( exists('temp/mrt', 'stations.json') ):
  print("- Writing MRT files ...")
  mrt_stations = m.get_stations()
  write_file(mrt_stations, 'temp/mrt', 'stations')
  print("- MRT files written")

print("Temporary data files have been written")

# All files have been made if they don't exist

services_stops_dict = read_file('temp/bus', 'services_stops_dict.json')
all_stops_dict = read_file('temp/bus', 'all_stops_dict.json')

combined_stops_and_services_dict = b.combine_stops_and_services(services_stops_dict, all_stops_dict)

mrt_stations = read_file('temp/mrt', 'stations.json')
combined_mrt = b.add_mrt_data(combined_stops_and_services_dict, mrt_stations)
write_file(combined_mrt, 'data', 'all')