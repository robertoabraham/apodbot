from slackclient import SlackClient

slack_token = 'xoxb-193605162912-GHtreKXdKP3vzkBcdiEtA7Oo'
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  text="Please bring me back from the dead!"
)
