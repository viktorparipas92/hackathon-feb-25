from fastapi import FastAPI, Form
from starlette.responses import StreamingResponse

from ml.openai_completion import generate_chat_completion_stream

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
