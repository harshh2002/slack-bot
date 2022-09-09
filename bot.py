import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError
import os
import requests
from dotenv import load_dotenv
load_dotenv()

SLACK_TOKEN=os.getenv("SLACK_TOKEN")
SIGNING_SECRET=os.getenv("SIGNING_SECRET")
BOT_ID = os.getenv("BOT_ID")

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(SIGNING_SECRET, "/slack/events", app)

client = slack.WebClient(token=SLACK_TOKEN)
@ slack_event_adapter.on('message')
def message(payload):
    print(payload)
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
 
    if text == "hi":
        try:
            response = client.files_upload(
                file='./files/image/hola.webp',
                initial_comment='Hello!!',
                channels=channel_id
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")
    if text == "video":
        try:
            response = client.files_upload(
                file='./files/video/anya.mp4',
                channels=channel_id
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

    def generate_buttons(files): 
        buttons = []
        for i in range(len(files)):
            buttons.append({
                "text": {
                    "type": "plain_text",
                    "text": files[i],
                    "emoji": True
                },
                "value": f"value-{i}"
            })
        return buttons

    if text == "image":
        dir_path = r'./files/image'
        files = os.listdir(dir_path)
        option_list = generate_buttons(files)
        message_to_send = {"channel" : channel_id, "blocks": [
        {
            "type": "input",
            "element": {
                "type": "radio_buttons",
                "options": option_list,
                "action_id": "radio_buttons-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Images",
                "emoji": True
            }
        }
        ]
        }
        try: 
            return client.chat_postMessage(**message_to_send)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["ok"] is False
            # str like 'invalid_auth', 'channel_not_found'
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

    try:
        file_name = payload['event']['files'][0]['name']
        print("file_name:-->", file_name)
        file_url = payload['event']['files'][0]['url_private']
        print("file_url:-->", file_url)
        user_n = payload['event']['files'][0]['user']
        print("user_n:-->", user_n)
        file_name = file_url.split('/')[-1]
        print("file_name:-->", file_name)
        try:
            json_path = requests.get(file_url)
        except:
            print("nnnn mm ")
        if user_n != BOT_ID:
            with open(file_name, "wb") as f:
                f.write(json_path.content)
    except:
        print("not found 1-->>")

if __name__ == "__main__":
    app.run(debug=True)
