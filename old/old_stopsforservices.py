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
          route_type = '1'  # route type are 1 or 2 (1 way/loop OR 2 way)
        else: 
          loop = False
          # route_type can be '1' or '2'

        # loop through all routes (dir1, dir2)
        # array 1 and 2 because each bus has a maximum of two routes

        try:
          for dir_no, route_soup in zip([1,2], soup.find('div', class_='RouteContainer')):

            route = []
            # for stop_soup in route_soup.find_all('div', class_='NodeContainer'):
            for stop_soup in route_soup.find_all('div', id='dir1'):
              stop_code = stop_soup.find('div', class_='NodeID').text
              # stop_name = stop_soup.find('div', 'NodeName').text
              # stop_road = stop_soup.find('div', 'NodeRoadName').text

              route.append(stop_code)
            
            if loop == False:
              # When it's NOT a loop, it's eaither
              try: 
                # (1) A bus with a 2 routes (like 14)
                route_name = soup.find(id=f'navdir{dir_no}').text .split(':')[1]
                route_type = '2'
              except:
                # (2) 1-way, no loop (like NR5)
                route_name = soup.find('div', class_='RouteDesti').text
                route_type = '1'
            
            services_stops_dict[service]['routes'].append({
              'name': route_name,
              'stops': route,
            })
          
          services_stops_dict[service]['loop'] = loop
          services_stops_dict[service]['type'] = route_type

        except:
          print("ERROR:", service)

    return services_stops_dict