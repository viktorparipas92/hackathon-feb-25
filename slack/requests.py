import requests

from slack.settings import SLACK_BOT_TOKEN


POST_MESSAGE_URL = 'https://slack.com/api/chat.postMessage'
CONVERSATION_HISTORY_URL = 'https://slack.com/api/conversations.history'


def send_message(channel_id: str, message: str):
    data = {
        'channel': channel_id,
        'text': message
    }
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(POST_MESSAGE_URL, json=data, headers=headers)
    result = response.json()
    if not result.get('ok'):
        print('Failed to send message:', result)  # Debugging

    return result


def get_im_conversation_history(im_channel_id, limit=5):
    """
    Fetch the last `limit` messages from a direct message (IM) conversation.
    """
    headers = {'Authorization': f"Bearer {SLACK_BOT_TOKEN}"}
    params = {'channel': im_channel_id, 'limit': limit}

    response = requests.get(CONVERSATION_HISTORY_URL, headers=headers, params=params)
    data = response.json()

    if not data.get('ok'):
        print('Error fetching IM conversation history:', data)
        return []

    return data.get('messages', [])


def download_image(image_url):
    headers = {
        'Authorization': f'Bearer {SLACK_BOT_TOKEN}'
    }
    response = requests.get(image_url, headers=headers)

    if response.status_code == 200:
        return response.content
    else:
        raise Exception(
            f"Failed to download image from Slack. Status code: {response.status_code}"
        )