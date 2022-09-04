import slack
import os
from dotenv import load_dotenv
load_dotenv()

SLACK_TOKEN=os.getenv("SLACK_TOKEN")
client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#slack-bot',text='Hello world')
