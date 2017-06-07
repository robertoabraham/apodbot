import urllib2
import json
from datetime import date

d = date.today()
date_string = d.isoformat()

date_string = "2017-6-5"

url="https://api.nasa.gov/planetary/apod?api_key=8frhOuCGozXTd7b8Jp8kfP1g9WguYRcEcsp3ET5P&date="+date_string
js=json.loads(urllib2.urlopen(url).read())
js['explanation']=js['explanation'].split("   ")[0]

from slackclient import SlackClient
slack_token = "xoxb-193605162912-LvckHKGHGaKESgkNeCp7EHMg"
sc = SlackClient(slack_token)
output = sc.api_call(
  "chat.postMessage",
  channel="#apod",
  attachments = [{"title": js['title'], \
                  "footer": "Scraped from https://apod.nasa.gov/",\
                  "image_url": js['url'], \
                  "text":js['explanation']}],
  text="KV Testing"
)

if (output["ok"] == False):
    raise Exception('The slack bot appears to be dead')
