from sentient_agent_framework.interface.events import (
    ResponseEvent,
    ResponseEventAdapter
)
from simple_sse_client import (
    async_stream,
    ServerSentEvent
)
from typing import AsyncIterator
from ulid import ULID


class SentientAgentClient:
    def __init__(
        self,
        session: dict = None
    ):
        if session is None:
            self.processor_id = "sentient-chat-client"
            self.activity_id = str(ULID())
            self.request_id = str(ULID())
            self.interactions = []
        else:
            self.processor_id = session["processor_id"]
            self.activity_id = session["activity_id"]
            self.request_id = session["request_id"]
            self.interactions = session["interactions"]


    async def process_event(
        self,
        event: ServerSentEvent
    ) -> ResponseEvent:
        return ResponseEventAdapter.validate_python(event.json())


    async def query_agent(
        self,
        prompt: str,
        url: str = "http://0.0.0.0:8000/assist"
    ) -> AsyncIterator[ResponseEvent]:
        query_id = str(ULID())
        json={
            "query": {
                "id": query_id,
                "prompt": prompt
            },
            "session": {
                "processor_id": self.processor_id,
                "activity_id": self.activity_id,
                "request_id": self.request_id,
                "interactions": self.interactions
            }
        }
        headers = {
            "Content-Type": "application/json"
        }

        async for event in async_stream(
            url=url,
            method="POST",
            headers=headers,
            json=json,
            timeout=60.0
        ):
            yield await self.process_event(event)