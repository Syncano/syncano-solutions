import requests, syncano, json, math
from syncano.models.base import Object

connection = syncano.connect(api_key='INSERT_SYNCANO_API_KEY_HERE')

# The Earth is a spheroid, and thus the lengths of latitude and longitude vary on location
# This solution calculates those lengths and returns all the stored
# locations in a given radius

# Compute length of degrees in meters
def compute(latitude):
    rLat = math.radians(latitude)
    # constants
    m1 = 111132.92      # latitude calculation term 1
    m2 = -559.82        # latitude calculation term 2
    m3 = 1.175          # latitude calculation term 3
    m4 = -0.0023        # latitude calculation term 4
    p1 = 111412.84      # longitude calculation term 1
    p2 = -93.5          # longitude calculation term 2
    p3 = 0.118          # longitude calculation term 3
    # calculate the length of a degree of latitude and longitude in meters
    latLength = m1 + (m2 * math.cos(2 * rLat)) + \
        (m3 * math.cos(4 * rLat)) + (m4 + math.cos(6 * rLat))
    latLength /= 1000

    lonLength = (p1 * math.cos(rLat)) + \
        (p2 * math.cos(3 * rLat)) + (p3 * math.cos(5 * rLat))
    lonLength /= 1000

    return {'latLength': latLength, 'lonLength': lonLength}

# If lat, lon, or radius is missing in the ARGS it will raise an error
# you can pass those ARGS e.g. in a webhook by calling:
# https://api.syncano.io/v1/instances/<instance>/webhooks/p/<public_link>/?lat=1234&lon=1234&radius=50
# or in a direct CodeBox call:
# CodeBox.please.run(instance_name='YOUR_INSTANCE_NAME', id=the_CodeBox_id, payload={'lat': '1234', 'lon': '1234', 'radius': '50'})
data = {
    'lat': ARGS.get("lat", None),
    'lon': ARGS.get("lon", None),
    'radius': ARGS.get("radius", None)
}

missing = []
for key in data:
    if data[key] is None:
        missing.append(key)
if len(missing) > 0:
    parameters = ""
    for param in missing:
        parameters += ", " + param
    raise ValueError("Parameters not found: " + parameters[2:])

conv = compute(data['lat'])
highLat = data['lat'] + data['radius'] / conv['latLength']
lowLat = data['lat'] - data['radius'] / conv['latLength']
highLon = data['lon'] + data['radius'] / conv['lonLength']
lowLon = data['lon'] - data['radius'] / conv['lonLength']

locations = Object.please.list(instance_name="INSTANCE_NAME", class_name="location").filter(
    lat__gt=lowLat, lat__lte=highLat, lon__gt=lowLon, lon__lte=highLon)

response = []
for l in locations:
    response.append({'id': l.id, 'lat':l.lat, 'lon': l.lon})
print(response)