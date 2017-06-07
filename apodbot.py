import urllib2
import json
import uuid
from datetime import date

d = date.today()
date_string = d.isoformat()

date="2017-6-7"
url="https://api.nasa.gov/planetary/apod?api_key=8frhOuCGozXTd7b8Jp8kfP1g9WguYRcEcsp3ET5P&date="+date
js=json.loads(urllib2.urlopen(url).read())
js['explanation']=js['explanation'].split("   ")[0]

from slackclient import SlackClient
slack_token = "xoxb-193605162912-PPDqAs6RRhkeFJNnEcBGBlIu"
sc = SlackClient(slack_token)

if (js['media_type'] == "video"):
    output = sc.api_call(
      "chat.postMessage",
      channel="#apod",
      parse="full",
      unfurl_media="true",
      unfurl_links="true",
      text="https://www.youtube.com/watch?v="+js['url'].split("?")[0].split("/")[-1]+"&"+str(uuid.uuid1()))
else:
    output = sc.api_call(
      "chat.postMessage",
      channel="#apod",
      as_user=True,
      attachments = [{"title": js['title'], \
                      "footer": "Scraped from https://apod.nasa.gov/",\
                      "image_url": js['url'], \
                      "text":js['explanation']}],
      text="KV Testing")

if (output["ok"] == False):
    raise Exception('The slack bot appears to be dead')
