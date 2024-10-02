import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def create_client():
    client = OpenAI(api_key=api_key)
    return client
