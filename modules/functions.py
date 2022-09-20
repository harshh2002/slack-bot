from slack.errors import SlackApiError

def err():
    # You will get a SlackApiError if "ok" is False
    assert SlackApiError.response["ok"] is False
    # str like 'invalid_auth', 'channel_not_found'
    assert SlackApiError.response["error"]
    print(f"Got an error: {SlackApiError.response['error']}")


def hi(client, channel_id):
    try:
        response = client.files_upload(
            file='./files/image/hola.webp',
            initial_comment='Hello!!',
            channels=channel_id
        )
    except:
        err()

def video(client, channel_id):
    try:
        response = client.files_upload(
            file='./files/video/anya.mp4',
            channels=channel_id
        )
    except:
        err()

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