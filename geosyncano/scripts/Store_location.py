# https://developers.google.com/maps/documentation/geocoding/intro
import requests, syncano, json
from syncano.models.base import Object

accesstoken = 'INSERT_GOOGLEMAPS_API_TOKEN_HERE'
connection = syncano.connect(api_key='INSERT_SYNCANO_API_KEY_HERE')

#extract values from the ARGS
#if only lat & lon are passed, the solution will store it
#if an address is provided, the solution will convert it into coordinates and then store it
# you can pass those ARGS e.g. in a webhook by calling:
# https://api.syncano.io/v1/instances/<instance>/webhooks/p/<public_link>/?lat=1234&lon=1234
# or in a direct CodeBox call:
# CodeBox.please.run(instance_name='YOUR_INSTANCE_NAME', id=the_CodeBox_id, payload={'lat': '1234', 'lon': '1234'})

lat = ARGS.get("lat", None)
lon = ARGS.get("lon", None)
address = ARGS.get("address", None)

if address is None:
    if lat is None and lon is None:
        raise ValueError("ERROR: no parameters found")
    if lat is None or lon is None:
        raise ValueError("ERROR: coordinate is invalid")

if address is not None:
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?address="
    accesstoken = '&key=' + accesstoken
    address = address.strip(" ").replace(" ", "+")

    url = base_url + address + accesstoken
    r = requests.get(url)

    print(r.status_code, r.reason)
    response = r.json()['results'][0]['geometry']['location']
    lat = response['lat']
    lon = response['lng']

Object.please.create(lat=float(lat),
                     lon=float(lon),
                     instance_name="INSTANCE_NAME",
                     class_name="location")

'''
Python example to run this codebox

from syncano.models.base import *
import syncano

syncano.connect(api_key='api_key')

CodeBox.please.run(id=CODEBOX_ID,
                   instance_name="INSTANCE_NAME",
                   payload={"lat":"1234", "lon": "1234", "address": 25 Broadway})
'''