import urllib2
import json

date="2017-6-5"
url="https://api.nasa.gov/planetary/apod?api_key=8frhOuCGozXTd7b8Jp8kfP1g9WguYRcEcsp3ET5P&date="+date
js=json.loads(urllib2.urlopen(url).read())
js['explanation']='This is an APOD image. We are awesome!'
js['explanation']=js['explanation'].split("   ")[0]

from slackclient import SlackClient
slack_token = "xoxb-193605162912-j5LVCj5erhlsNvd4gpBok0JF"
sc = SlackClient(slack_token)
sc.api_call(
  "chat.postMessage",
  channel="#apod",
  attachments = [{"title": js['title'], \
                  "footer": "Scraped from https://apod.nasa.gov/",\
                  "image_url": js['url'], \
                  "text":js['explanation']}],
  text="KV Testing"
)

