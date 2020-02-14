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

### `get_services`
This function scrapes [LTG](https://landtransportguru.net/bus/bus-services/) and returns a list of all bus services.

Nothing complex.

### `get_stops_for_each_service`
This function takes a list of services and returns all the routes as a dictionary/object.

All the bus stops and information about routes come from LTG.

### Keys returned
1. `loop`: True or False depending on if the bus route is a loop or not. For example, bus 222 and 228 have loop routes. (When `loop` is True, `type` is `'1'`)
2. `routes`: A list of routes.
   - `name`: The route's name.
   - `stops`: A list of stops in the route 
3. `type`: The route type. `'1'` if it's a 1-way route or loop route; `'2'` is it's a 2-way route. (Most services have 2-way routes)

Example:
```
get_stops_for_each_service(['14', '15']) => { 
  '14': { 
    'loop': False,
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

### `get_all_stops`
- coming soon


## :bookmark_tabs: Data sources
- [Land Transport Guru](https://landtransportguru.net/): It's a site that's beautiful and easy to scrape.
- [Land Transport Authority Datamall](https://www.mytransport.sg/content/mytransport/home/dataMall.html): LTA provides free APIs such as bus arrival timings, and taxi location.

## :question: How do I use this?
Download and use the files in the "output/data" directory. More details coming soon.