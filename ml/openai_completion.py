import os
from functools import lru_cache

from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError

load_dotenv()

OPENAI_API_TOKEN = os.getenv('OPENAI_TOKEN')
COMPLETION_MODEL = 'gpt-4o-mini'


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