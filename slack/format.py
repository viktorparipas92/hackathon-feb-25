def format_messages_for_openai(conversation_history, user_message):
    """
    Format Slack messages into OpenAI's chat completion format.
    """
    messages = [
        {
            'role': 'assistant' if 'bot_id' in message else 'user',
            'content': message['text'],
        }
        for message in reversed(conversation_history)
    ]
    messages.append({
        'role': 'user',
        'content': f'Please answer briefly: {user_message}'
    })
    return messages
