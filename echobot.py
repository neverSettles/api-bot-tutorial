"""

Sample bot that echoes back messages.

This is the simplest possible bot and a great place to start if you want to build your own bot.

"""
from __future__ import annotations
import requests

from typing import AsyncIterable

from fastapi_poe import PoeBot
from fastapi_poe.types import QueryRequest
from sse_starlette.sse import ServerSentEvent

# TOGETHER_API_KEY = "YOURAPIKEY"
class EchoBot(PoeBot):
    def call(self, prompt):
        endpoint = 'https://api.together.xyz/inference'
        res = requests.post(endpoint, json={
            "model": "ChristopherRSettles/ft-88a5f83a-af33-4972-8bba-3fabbfb68a25-2023-08-13-19-31-07",
            "max_tokens": 512,
            "prompt": prompt,
            "request_type": "language-model-inference",
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 2
        }, headers={
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
        })

        print(res.json())

        print(res.json()['output']['choices'][0]['text'])

        return res.json()['output']['choices'][0]['text']

    async def get_response(self, query: QueryRequest) -> AsyncIterable[ServerSentEvent]:
        last_message = query.query[-1].content
        model_resp = self.call(last_message)
        yield self.text_event(model_resp)
