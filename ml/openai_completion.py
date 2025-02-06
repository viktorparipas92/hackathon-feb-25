import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, LengthFinishReasonError
from openai.resources.chat.completions import completion_create_params

load_dotenv()

OPENAI_API_TOKEN = os.getenv('OPENAI_TOKEN')
COMPLETION_MODEL = 'gpt-4o-mini'

MAX_TOKENS = 300
TOO_LONG_RESPONSE = 'The response is too long.'
REFUSED_IMAGE = 'Could not interpret image.'


@lru_cache
def _get_openai_client():
    openai_client = OpenAI(api_key=OPENAI_API_TOKEN)
    return openai_client


def generate_chat_completion_stream(prompt: str):
    openai = _get_openai_client()
    messages = [{'role': 'user', 'content': prompt}]
    try:
        stream = openai.chat.completions.create(
            messages=messages,
            model=COMPLETION_MODEL,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    except AuthenticationError:
        return ''


def get_chat_completion(messages: list):
    openai = _get_openai_client()
    try:
        completion = openai.chat.completions.create(
            messages=messages,
            model=COMPLETION_MODEL,
        )
    except AuthenticationError:
        return ''

    response = completion.choices[0].message
    return response.content if not response.refusal else 'No response.'


def get_image_interpretation(
    prompt: str,
    base64_image,
    response_format: completion_create_params.ResponseFormat,
):
    openai_client = _get_openai_client()
    content = [
        {'type': 'text', 'text': prompt},
        {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{base64_image}"}},
    ]
    try:
        completion = openai_client.beta.chat.completions.parse(
            model=COMPLETION_MODEL,
            messages=[{'role': 'user', 'content': content}],
            response_format=response_format,
            max_completion_tokens=MAX_TOKENS,
        )
    except LengthFinishReasonError:
        return TOO_LONG_RESPONSE
    except AuthenticationError:
        return ''

    response = completion.choices[0].message
    return response.content if not response.refusal else REFUSED_IMAGE