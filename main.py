from pathlib import Path

from bus import Bus
from file import write_file, read_file

b = Bus()

if not (Path('output/temporary/services_stops_dict.json').is_file() or Path('output/temporary/all_stops.json').is_file()):
  print("Writing temporary data files ...")

  all_services = b.get_services()
  services_stops_dict = b.get_stops_for_each_service(all_services)
  write_file(services_stops_dict, 'temporary', 'services_stops_dict')

  all_stops_dict = b.get_all_stops()
  write_file(all_stops_dict, 'temporary', 'all_stops_dict')

  print("Finished writing temporary data files.")

# All files have been made if they don't exist

# services_stops_dict = read_file('temporary', 'services_stops_dict')
# all_stops_dict = read_file('temporary', 'all_stops_dict')

# combined = b.combine_stops_and_services(services_stops_dict, all_stops_dict)