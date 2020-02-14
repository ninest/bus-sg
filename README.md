# :bus: Singapore Bus Routes
> Getting a list of all bus stops and services

## :school_satchel: Features
- [x] List of all bus services and their respective routes and stops
  - [x] Bus service type (2-way, 1-way, or loop)
- [ ] List of all bus stops and metadata including name, road, coordinates, and respective buses
  - [ ] College bus stops
    - [ ] NUS
    - [ ] NTU

## How it works
Most of the magic happens in `bus.py`. This file contains the following important functions:

1. `get_services`
2. `get_stops_for_each_service`
3. `get_all_stops`

### 1. `get_services`
This function scrapes [LTG](https://landtransportguru.net/bus/bus-services/) and returns a list of all bus services.

Nothing complex.

### 2. `get_stops_for_each_service`
This function takes a list of services and returns all the routes as a dictionary/object.

All the bus stops and information about routes come from LTG.

#### Keys returned
1. `loop`: True or False depending on if the bus route is a loop or not. For example, bus 222 and 228 have loop routes. (When `loop` is True, `type` is `'1'`)
2. `routes`: A list of routes.
   - `name`: The route's name.
   - `stops`: A list of stops in the route 
3. `type`: The route type. `'0'` if it's a loop; `'1'` if it's a 1-way route; and `'2'` is it's a 2-way route. (Most services have 2-way routes)

More data will be added soon:
- MRT stations connections
- Route length  
- ...

Example:
```
get_stops_for_each_service(['14', '15']) => { 
  '14': { 
    'routes': [ 
      { 
        'name': 'Bedok Int → Clementi Int ⇋',
        'stops': [ 
          '84009',
          '84359',
          ...
        ],
      },
      { 
        'name': 'Clementi Int → Bedok Int ⇋',
        'stops': [ 
          '17009',
          '17239',
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

#### Keys returned
1. `code`
2. `name`
3. `road`
4. `coords`

**TODO:** Find MRT stations (if any). This may require a separate function.

### 4. `combine_stops_and_services`
This function takes in 2 parameters:
1. `services_stops_dict`: The output of `get_stops_for_each_service` (function 2).
2. `all_stops_dict`: The output of `get_all_stops` (function 3).

`services_stops_dict` has a structure of bus service to routes (see example above).

`all_stops_dict` is a dictionary of all bus stops with the key being the bus stop code.


## :bookmark_tabs: Data sources
- [Land Transport Guru](https://landtransportguru.net/): It's a site that's beautiful and easy to scrape.
- [Land Transport Authority Datamall](https://www.mytransport.sg/content/mytransport/home/dataMall.html): LTA provides free APIs such as bus arrival timings, and taxi location.

## :question: How do I use this?
Download and use the files in the "output/data" directory. More details coming soon.