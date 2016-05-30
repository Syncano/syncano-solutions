# https://developer.venmo.com/docs/quickstart
import requests, syncano, json
from syncano.models.base import Object

# extract phone, note, and amount from the ARGS
# if none are passed, it will raise an error
# you can pass those ARGS e.g. in a webhook by calling:
# https://api.syncano.io/v1/instances/<instance>/webhooks/p/<public_link>/?phone=1234&note=helloworld&amount=0.01
# or in a direct CodeBox call:
# CodeBox.please.run(instance_name='YOUR_INSTANCE_NAME', id=the_CodeBox_id, payload={'phone': '1234', 'note': 'helloworld', 'amount': '0.01'})

accesstoken = 'INSERT_VENMO_ACCESS_TOKEN_HERE'
connection = syncano.connect(api_key='SYNCANO_API_KEY')

# a valid US 'phone', 'email' or Venmo 'user_id' is required
phone = ARGS.get("phone", None)
note = ARGS.get("note", None)
amount = ARGS.get("amount", None)

data = {}
data['access_token'] = accesstoken
data['phone'] = phone
data['note'] = note
data['amount'] = amount

missing = []
for key in data:
    if data[key] is None:
        missing.append(key)
if len(missing) > 0:
    parameters = ""
    for param in missing:
        parameters += ", " + param
    raise ValueError("Parameters not found: " + parameters[2:])

# base url of Venmo payment API
base_url = "https://api.venmo.com/v1/payments"

# send POST request to pay amount
r = requests.post(base_url, data=data)

print(r.status_code, r.reason)
print(r.text)

balance = r.json()

Object.please.create(balance=float(balance['data']['balance']),
                     amount=float(amount),
                     note=note,
                     phone=phone,
                     instance_name="INSTANCE_NAME",
                     class_name="venmo_payment")