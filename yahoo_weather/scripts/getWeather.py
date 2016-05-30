import urllib2, urllib, json

# merging GET and POST args
GET = ARGS.get("GET", {})
POST = ARGS.get("POST", {})
ARGS.update(GET)
ARGS.update(POST)

# extract city and state from the ARGS
# if none are passed, it will raise an error
# you can pass those ARGS e.g. in a webhook by calling
# https://api.syncano.io/v1/instances/<instance>/webhooks/p/<public_link>/?city=brooklyn&state=ny
# or in a direct CodeBox call: CodeBox.please.run(instance_name='YOUR_INSTANCE_NAME', id=the_CodeBox_id, payload={'city': 'Burlington', 'state': 'VT'})
city = ARGS.get("city", None)
state = ARGS.get("state", None)

if city is None and state is None:
    raise ValueError("Parameters 'city' and 'state' were not found")
elif city is None:
    raise ValueError("Parameter 'city' was not found")
elif state is None:
    raise ValueError("Parameter 'state' was not found")

# base url of Yahoo Weather API
base_url = "https://query.yahooapis.com/v1/public/yql?"

# query to perform on the Yahoo Weather API
# if you're not interested in getting the full response
# replace "select *" with a more detailed query
# e.g. "select item.condition.text" to get a one word forecast
yql_query = "select item.forecast from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"{city}, {state}\")".format(city=city, state=state)
url_with_query = base_url + urllib.urlencode({'q':yql_query}) + "&format=json"
result = urllib2.urlopen(url_with_query).read()

# we want to extract the forecast from weather data
data = json.loads(result)
forecasts = []
channels = data['query']['results']['channel']
for channel in channels:
 forecasts.append(channel['item']['forecast'])

print json.dumps(forecasts)

'''sample usage in python

from syncano.models.base import *
import syncano

syncano.connect(api_key='API KEY')
CodeBox.please.run(instance_name='YOUR_INSTANCE_NAME',
                   id=the_CodeBox_id,
                   payload={'city': 'Houston', 'state': 'TX'})
'''