from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from syncano.models import Object
import syncano

# Make google developer account here, follow instructions to get
# the google DEVELOPER_KEY
# https://developers.google.com/youtube/v3/getting-started
DEVELOPER_KEY = "Put your developer key here"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

syncano.connect(api_key="SYNCANO_API_KEY")
query = ARGS.get("query", None)
order = ARGS.get("order", "relevance")      # If you don't specify order, we default the order to 'relevance'
max_results = ARGS.get("max_results", 10)   # Can be 0-10, default is 10
if query is None:
    raise ValueError("You did not pass 'query'")


def youtube_search(query, order, max_results):
    youtube = build(YOUTUBE_API_SERVICE_NAME,
                    YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    # https://developers.google.com/youtube/v3/guides/implementation/search
    # https://developers.google.com/youtube/v3/docs/search/list
    # maxResults can be 0-50
    # order can = date / rating / relevance / title / viewCount
    search_response = youtube.search().list(q=query,
                                            part="id,snippet",
                                            maxResults=max_results,
                                            order=order
                                            ).execute()

    videos = search_response.get('items', [])
    for video in videos:
        if video['id']['kind'] == 'youtube#video':
            title = video['snippet']['title']
            # 'default', 'medium', and 'high' are the resolutions you can pick
            thumbnail = video['snippet']['thumbnails']['medium']
            description = video['snippet']['description']
            video_id = video['id']['videoId']
            video_url = "https://www.youtube.com/watch?v=" + video_id
            Object.please.create(instance_name="youtube_videos",
                                 class_name="video",
                                 title=title,
                                 thumbnail=thumbnail,
                                 description=description,
                                 video_id=video_id,
                                 video_url=video_url,
                                 query=query)
        else:
            pass
    print videos

try:
    youtube_search(query, order, max_results)
except HttpError, e:
    print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)

'''
Make google developer account here, follow instructions to get
the DEVELOPER_KEY
https://developers.google.com/youtube/v3/getting-started


Python example

from syncano.models.base import *
import syncano

syncano.connect(api_key='api_key')

# order can be date / rating / relevance / title / viewCount
# max_results can be 0-50
CodeBox.please.run(id=CODEBOX_ID,
                   instance_name="INSTANCE_NAME",
                   payload={"query":"cat videos", "order": "viewCount", "max_results": 10})
'''