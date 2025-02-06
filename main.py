import base64

from fastapi import FastAPI, Form, Request, Response, BackgroundTasks
from openai.types import ResponseFormatText
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from ml.openai_completion import (
    generate_chat_completion_stream, get_chat_completion,
    get_image_interpretation,
)
from slack.format import format_messages_for_openai
from slack.requests import send_message, get_im_conversation_history, download_image

app = FastAPI()


@app.post('/')
async def root(
    command: str = Form(...),
    user_name: str = Form(...),
    text: str = Form(...)
):
    response: str = generate_chat_completion_stream(text)
    return StreamingResponse(response, media_type='text/plain')


def process_event(event, im_channel_id, image_interpretations):
    # Handle image interpretation and chat completion asynchronously
    if files := event.get('files'):
        for file in files:
            image_data = download_image(file.get('url_private_download'))
            if image_data:
                encoded_image = encode_image(image_data)
                interpretation = get_image_interpretation(
                    prompt='What is this image about?',
                    base64_image=encoded_image,
                    response_format=ResponseFormatForImageInterpretation,
                )
                image_interpretations.append(
                    {
                        'file_name': file.get('name'),
                        'interpretation': interpretation
                    }
                )

    conversation_history = get_im_conversation_history(im_channel_id, limit=5)
    text = event.get('text')
    if image_interpretations:
        text += 'The following are the interpretations of the attached images'
        text += '\n'.join(ii['interpretation'] for ii in image_interpretations)

    messages = format_messages_for_openai(conversation_history, text)
    response = get_chat_completion(messages)
    send_message(im_channel_id, response)


@app.post('/chat/')
async def chat(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    if 'challenge' in data:
        return {'challenge': data['challenge']}

    if not 'event' in data:
        return {'ok': True}

    event = data['event']
    if not should_respond(event):
        print('Sent by bot')
        return {'ok': True}

    print(f'Not sent by bot: {event["type"]}')
    print(event)

    im_channel_id = event.get('channel')
    image_interpretations = []

    # Add the long-running task to the background
    background_tasks.add_task(
        process_event, event, im_channel_id, image_interpretations
    )

    # Respond immediately
    return Response(status_code=200)


def should_respond(event: dict):
    return (
        not 'bot_profile' in dict(event)
        and event.get('type', '') == 'message'
    )


def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')


class ResponseFormatForImageInterpretation(BaseModel):
    filename: str
    interpretation: str


