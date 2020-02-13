# :bus: Singapore Bus Routes
> Getting a list of all bus stops and services

## :school_satchel: Features
- [x] List of all bus services and their respective routes and stops
  - [x] Bus service type (2-way, 1-way, or loop)
- [ ] List of all bus stops and metadata including name, road, coordinates, and respective buses
  - [ ] College bus stops
    - [ ] NUS
    - [ ] NTU

## :exclamation: What's this?
- coming soon

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
        ]
      },
      { 
        'name': 'Clementi Int → Bedok Int ⇋',
        'stops': [ 
          '17009',
          '17239',
          ...
        ]
      }
    ]
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
- coming soon