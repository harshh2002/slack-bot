import slack
from flask import Flask
from slackeventsapi import SlackEventAdapter
from slack.errors import SlackApiError
import os
from dotenv import load_dotenv
load_dotenv()

SLACK_TOKEN=os.getenv("SLACK_TOKEN")
SIGNING_SECRET=os.getenv("SIGNING_SECRET")

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


if __name__ == "__main__":
    app.run(debug=True)
