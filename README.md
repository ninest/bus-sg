# :bus: Singapore Bus Routes
> Getting a list of all bus stops and services

## :school_satchel: Features
- [x] List of all bus services and their respective routes and stops
  - [x] Bus service type (2-way, 1-way, or loop)
- [x] List of all bus stops and metadata including name, road, coordinates, and respective buses
  - [ ] Exta metadata such as route length and route time/duration
- [x] MRT stations for bus stops
- [ ] College bus stops
  - [ ] NUS
  - [ ] NTU

To add college bus stops, we will have to add all shuttles. However, some bus stops don't have codes, so we'll have to think of ways to create IDs. One idea: Internal buses can be "N" followed by 4 digits (ex: First stop is N0001). Similary, premium stops with no IDs can be of the format PXXXX.

## Getting the data
Most of the magic happens in `bus.py`. This file contains the following important functions:

1. `get_services`
2. `get_stops_for_each_service`
3. `get_all_stops`
4. `combine_stops_and_services`

### 1. `get_services`
This function scrapes [LTG](https://landtransportguru.net/bus/bus-services/) and returns a list of all bus services.

Nothing complex.

### 2. `get_stops_for_each_service`
This function takes a list of services and returns all the routes as a dictionary/object.

All the bus stops and information about routes come from LTG.

This function returns a dictionary with the keys being bus services (as strings). The dictionaries have the following key/values:

1. `loop`: True or False depending on if the bus route is a loop or not. For example, bus 222 and 228 have loop routes. (When `loop` is True, `type` is `'1'`)
2. `routes`: A list of routes.
   - `name`: The route's name.
   - `stops`: A list of stops in the route 
3. `type`: The route type. `'0'` if it's a loop; `'1'` if it's a 1-way route; and `'2'` is it's a 2-way route. (Most services have 2-way routes)

More data will be added soon:
- MRT stations connections (see function 5)
- Route length  
- ...

Example:

```
get_stops_for_each_service(['14', '15']) => { 
  '14': { 
    'routes': [ 
      { 
        'name': 'Bedok Int → Clementi Int',
        'stops': [ 
          '84009',
          ...
        ],
      },
      { 
        'name': 'Clementi Int → Bedok Int',
        'stops': [ 
          '17009',
          ...
        ],
      }
    ],
    "type": '1'
  },
  { '15': { .. } }
}
```

### 3. `get_all_stops`
This function makes use of LTA's DataMall API for Bus Stops. I thought I could do without LTA's API for bus stops, but it's the only source for the longitude and latitude (coordinates) of the bus stops.

This function returns a dictionary with they keys being bus stop codes.
```
{
  code: {
    code,
    name,
    road,
    coords
  },
  ...
}
```


**TODO:** Find MRT stations (if any). This may require a separate function after function 4.

### 4. `combine_stops_and_services`
This function takes in 2 parameters:
1. `services_stops_dict`: The output of `get_stops_for_each_service` (function 2).
2. `all_stops_dict`: The output of `get_all_stops` (function 3).

`services_stops_dict` has a structure of bus service to routes (see example above).

`all_stops_dict` is a dictionary of all bus stops with the key being the bus stop code.

### 5. `MRT.get_stations`
Collecting MRT stations and a list of bus stops near them happens in `mrt.py`. `get_stations` works similarly to `get_services` (function 1). It scrapes LTG for MRT stations. 

There's one more function (`MRT.get_station_bus_stops`) to get the bus stops for the station. It returns a list of of bus stop codes.

`MRT.get_stations` returns a dictionary with MRT station reference IDs as the keys. Note that each reference ID has it's own dictionary, so interchange stations will be in the dictionary twice. Dhoby Ghaut will be there thrice.

```
{
  ref: {
    name,
    refs,
    bus_stops
  }
}
```

`refs` and `bus_stops` are lists. The list `refs` contains `ref` (the key) and reference IDs of the station on other lines. 

This dictionary does store repeats.

**NOTE:** As of now, future MRT stations abd lines have been removed (te, je, ...). This is because the LTG data is incomplete, so it's causing some repeats and dirty data.

### 6. `add_mrt_data`
Add MRT data to `combined_stops_and_services_dict` (the dictionary returned from `combine_stops_and_services`, function 4).

It's all come together in this structure:

```
{
  code: {
    code,
    name,
    road,
    coords: {
      lat, 
      lon
    },
    services: [ ... ],
    mrt_stations: [ ... ]
  }
}
```


## :bookmark_tabs: Data sources
- [Land Transport Guru](https://landtransportguru.net/): It's a site that's beautiful and easy to scrape.
- [Land Transport Authority Datamall](https://www.mytransport.sg/content/mytransport/home/dataMall.html): LTA provides free APIs such as bus arrival timings, and taxi location.

I'd also like to add [cheeaun/busrouter-sg](https://github.com/cheeaun/busrouter-sg) here. While it wasn't a data source, it was really helpful.

## :question: How do I use this?
See the files in the "output/data" directory. More details coming soon.

## Known issues
1. Some stations in the stations list on LTS don't have all stations refs complete. For example, see Marina Bay Financial (a bus stop). The TE line is mentioned even though it is not on the main list, causing duplicates.