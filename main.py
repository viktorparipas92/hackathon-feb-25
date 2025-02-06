import redis as redis
from fastapi import FastAPI, Form, Request, Response
from starlette.responses import StreamingResponse

from ml.openai_completion import generate_chat_completion_stream, get_chat_completion
from slack.send_message import send_message

app = FastAPI()

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

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

    user_id = event.get('user')
    text = event.get('text')
    channel_id = event.get('channel')

    conversation_context = redis_client.get(f'conversation:{user_id}') or ''
    # openai_response = generate_chat_completion_stream(conversation_context + text)
    openai_response = get_chat_completion(conversation_context + text)

    new_conversation_context = f'{conversation_context}{text}\n{openai_response}\n'
    redis_client.set(f'conversation:{user_id}', new_conversation_context)

    send_message(channel_id, openai_response)

    return Response(status_code=200)


def is_sent_by_bot(event: dict):
    return 'bot_id' in event



