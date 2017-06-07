import re
import urllib2
import json
import uuid
import datetime
from datetime import date
import inflect
from slackclient import SlackClient

p = inflect.engine()

d = date.today()            #get today's APOD
#d = datetime.date(2017,6,4) #get a specific day's APOD
date_string = d.isoformat() #create nicely formatted dates

url="https://api.nasa.gov/planetary/apod?api_key=8frhOuCGozXTd7b8Jp8kfP1g9WguYRcEcsp3ET5P&date="+date_string
js=json.loads(urllib2.urlopen(url).read())
js['explanation']=js['explanation'].split("   ")[0]

slack_token = "TOKEN_GOES_HERE"

para = (js['explanation'][:100] + ' ...') if len(js['explanation']) > 100 else js['explanation'][:100] 

sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  as_user="true",
  text = ("*APOD FOR "+d.strftime("%B").upper()+re.sub(' +',' '," "+p.ordinal(d.strftime("%e")))+", "+d.strftime("%Y")+"*")
)

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  as_user="true",
  text = ("*"+js['title'].upper()+"*")
)

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  as_user="true",
  text = (para + " (For full text, click here: https://apod.nasa.gov/apod/ap"+d.strftime("%y%m%d")+".html)")
)

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
      attachments = [{"title": "", \
                      "image_url": js['url']}],
)

if (output["ok"] == False):
    raise Exception('The slack bot appears to be dead')
