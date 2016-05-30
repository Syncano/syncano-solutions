# If you want to restore an article, choose the data object from readme_backup
# class and paste it's id in Config tab.
# Next uncomment the appropriate lines to get what you want

import syncano
import requests
from syncano.models.base import Class, Object

connection = syncano.connect_instance(META['instance'],
                                      api_key=CONFIG['account_key'])
obj = Object.please.get(class_name="readme_backup", id=CONFIG['id'])
url = str(obj.file)

requests.packages.urllib3.disable_warnings()
r = requests.get(url, verify=False)


docs = json.loads(r.content)

# uncomment the lines below to print article titles for the
# first version and first category
# pages = len(docs[0]['categories'][0]["pages"])
# print [docs[0]['categories'][0]['pages'][i]['title'] for i in xrange(pages)]

# print first article in first category of the first version
print docs[0]['categories'][0]['pages'][0]['body']