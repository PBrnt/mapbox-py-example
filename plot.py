#!/usr/bin/python2

import os
import sys
from mapbox import Static
import json
import requests

MAPBOX_TOKEN = "pk.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
JCDECAUX_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


def get_stations():
    # Doc: https://developer.jcdecaux.com/#/opendata/vls?page=getstarted
    url = "https://developer.jcdecaux.com/rest/vls/stations/Toulouse.json"
    data = json.loads(requests.get(url=url).text)
    
    return data


def save_map():
    # Doc: https://github.com/mapbox/mapbox-sdk-py/blob/master/docs/static.md#static-maps
    service = Static(access_token=MAPBOX_TOKEN)
    
    response = service.image('mapbox.satellite', lon=-61.7, lat=12.1, z=12)
    with open('/tmp/map.png', 'wb') as output:
        output.write(response.content)


def main():
    data = get_stations()
    print(data)
    
    save_map()


if __name__ == '__main__':
    main()
