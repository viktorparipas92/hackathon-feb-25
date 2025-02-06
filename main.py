from fastapi import FastAPI, Form

app = FastAPI()


@app.post('/')
async def root(
    command: str = Form(...),
    user_name: str = Form(...),
    text: str = Form(...)
):
    response_message = f'@{user_name} used {command} with args: {text}'
    return {'text': response_message}
