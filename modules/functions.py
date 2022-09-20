from slack.errors import SlackApiError

def hi():
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

def video():
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