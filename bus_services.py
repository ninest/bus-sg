import requests
from bs4 import BeautifulSoup

# get all bus services nos from https://www.mytransport.sg/content/mytransport/map.html
def get_services():
  r = requests.get('https://www.mytransport.sg/content/mytransport/map.html')
  if r.status_code == 200:
    bus_services = []

    soup = BeautifulSoup(r.content, 'lxml')
    options = soup.find(id='busservice_option')
    for optgroup in options.find_all('optgroup'):
      for option in optgroup.find_all('option'):
        bus_services.append(option.text)
    return bus_services
