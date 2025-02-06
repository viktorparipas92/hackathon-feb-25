import requests

from slack.settings import SLACK_BOT_TOKEN

POST_MESSAGE_URL = 'https://slack.com/api/chat.postMessage'


def send_message(channel_id: str, message: str):
    data = {
        'channel': channel_id,
        'text': message
    }
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }
    requests.post(POST_MESSAGE_URL, data=data, headers=headers)