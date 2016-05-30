import requests
import json
import syncano
from datetime import datetime
from syncano.models import Object

url = "https://dash.readme.io/api/projects/" + CONFIG["project"] + "/" \
      + CONFIG["version"] + "/export"
headers = {"Cookie": CONFIG["cookie"]}

r = requests.get(url, headers=headers)
parsed = json.loads(r.content)

file_path = "/tmp/backup"
with open(file_path, "w") as f:
    json.dump(parsed, f)

f.close()

connection = syncano.connect(api_key=CONFIG["account_key"])

file = open(file_path, "r")
Object.please.create(instance_name=META["instance"],
                     class_name="readme_backup",
                     file=file)