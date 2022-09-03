import slack

SLACK_TOKEN="xoxb-4032863284611-4030037183557-ICdmYASAzX9O9qo3zP036jhF"

client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#slack-bot',text='Hello world')
