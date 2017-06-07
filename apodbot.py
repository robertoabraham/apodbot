from slackclient import SlackClient

slack_token = 'xoxb-193605162912-Q54h4FX3GZ1vjpKZVRjCnhNS'
sc = SlackClient(slack_token)

sc.api_call(
  "chat.postMessage",
  channel="#apod",
  text="Hello from Python! :tada:"
)
