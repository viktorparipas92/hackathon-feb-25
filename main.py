import base64

from fastapi import FastAPI, Form, Request, Response
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


@app.post('/chat/')
async def chat(request: Request):
    data = await request.json()
    if 'challenge' in data:
        return {'challenge': data['challenge']}

    if not 'event' in data:
        return {'ok': True}

    event = data['event']
    if is_sent_by_bot(event):
        return {'ok': True}

    im_channel_id = event.get('channel')
    image_interpretations = []
    print('Files', event.get('files'))
    if files := event.get('files'):
        print(files)

        for file in files:
            image_data = download_image(file.get('url_private_download'))
            if image_data:
                encoded_image = encode_image(image_data)
                print('Encoded image')
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
    print('Original text', text)
    if image_interpretations:
        print()
        text += 'The following are the interpretations of the attached images'
        text += '\n'.join(ii['interpretation'] for ii in image_interpretations)
        print('Augmented text', text)

    messages = format_messages_for_openai(conversation_history, text)
    response = get_chat_completion(messages)

    send_message(im_channel_id, response)
    return Response(status_code=200)


def is_sent_by_bot(event: dict):
    return 'bot_id' in event


def encode_image(image_data):
    return base64.b64encode(image_data).decode('utf-8')


class ResponseFormatForImageInterpretation(BaseModel):
    filename: str
    interpretation: str


