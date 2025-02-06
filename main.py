from fastapi import FastAPI, Form, Request, Response
from starlette.responses import StreamingResponse

from ml.openai_completion import generate_chat_completion_stream, get_chat_completion
from slack.format import format_messages_for_openai
from slack.requests import send_message, get_im_conversation_history

app = FastAPI()


@app.post('/')
async def root(
    command: str = Form(...),
    user_name: str = Form(...),
    text: str = Form(...)
):
    # response_message = f'@{user_name} used {command} with args: {text}'
    response: str = generate_chat_completion_stream(text)

    return StreamingResponse(response, media_type='text/plain')


@app.post('/chat/')
async def chat(request: Request):
    data = await request.json()
    if 'challenge' in data:
        return {'challenge': data['challenge']}

    if not 'event' in data:
        return {'ok': True}

    event = data['event']
    print('Event:', event)
    if is_sent_by_bot(event):
        print('Bot message')
        return {'ok': True}

    im_channel_id = event.get('channel')
    conversation_history = get_im_conversation_history(im_channel_id, limit=5)

    text = event.get('text')
    messages = format_messages_for_openai(conversation_history, text)
    print('Messages:', messages)
    openai_response = get_chat_completion(messages)
    send_message(im_channel_id, openai_response)
    return Response(status_code=200)


def is_sent_by_bot(event: dict):
    return 'bot_id' in event



