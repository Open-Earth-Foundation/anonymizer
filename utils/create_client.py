import os
from openai import OpenAI


api_key = os.getenv("OPENAI_API_KEY")


def create_client():
    client = OpenAI(api_key=api_key)
    return client
