import urllib2
import json
import uuid
import datetime
from datetime import date
import inflect
from slackclient import SlackClient

p = inflect.engine()

# Create nicely formatted dates
d = date.today()
d = datetime.date(2017,6,4)
date_string = d.isoformat()
my_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")

url="https://api.nasa.gov/planetary/apod?api_key=8frhOuCGozXTd7b8Jp8kfP1g9WguYRcEcsp3ET5P&date="+date_string
js=json.loads(urllib2.urlopen(url).read())
js['explanation']=js['explanation'].split("   ")[0]

slack_token = "FILL_ME_WITH_TOKEN"
sc = SlackClient(slack_token)

if (js['media_type'] == "video"):
    output = sc.api_call(
      "chat.postMessage",
      channel="#apod",
      as_user=True,
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
      text = ("*APOD FOR "+my_date.strftime("%B").upper()+" "+p.ordinal(my_date.strftime("%e"))+", "+my_date.strftime("%Y")+"*"))

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  as_user="true",
  text = ("*"+js['title'].upper()+"*")
)

if (output["ok"] == False):
    raise Exception('The slack bot appears to be dead')
