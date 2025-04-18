import json
from src.sentient_agent_client.sentient_agent_client import SentientAgentClient
from sentient_agent_framework.interface.events import (
    DoneEvent,
    TextChunkEvent,
    DocumentEvent
)

class SentientAgentClientCLI:
    def __init__(
        self,
        client: SentientAgentClient
    ):
        self.client = client

    def print_title(
        self
    ):
        with open("title.txt", "r") as file:
            print(file.read())
        print()


    def print_horizontal_line(
        self
    ):
        print("-" * 100)
        print()


    async def chat(
        self
    ):
        # Print title from title.txt
        self.print_title()

        # Print horizontal line 
        self.print_horizontal_line()

        # Print instructions
        print("To exit just type 'exit' and press enter.")
        print()

        # Get agent URL
        url = input("Enter agent URL: ")
        if url == "exit":
            return
        print()

        # Print horizontal line
        self.print_horizontal_line()

        # Query agent
        while True:
            prompt = input("Enter your message: ")
            if prompt == "exit":
                break
            print()

            stream_id = None

            async for event in self.client.query_agent(prompt, url):
                # Handle done event
                if isinstance(event, DoneEvent):
                    print()
                    self.print_horizontal_line()
                    break

                # Handle stream events
                if isinstance(event, TextChunkEvent):
                    if stream_id != event.stream_id:
                        # Update stream id
                        stream_id = event.stream_id
                        # Print empty line
                        print()
                        # Print event name only once for each stream
                        print(event.event_name)
                    # Print stream
                    print(event.content, end="", flush=True)
                    if event.is_complete:
                        print()
                
                # Handle other events
                else:
                    # Print event type
                    print(event.event_name)
                    # Pretty print event data
                    if isinstance(event, DocumentEvent):
                        print(json.dumps(event.content, indent=4))
                    else:
                        print(event.content)
                    # Print empty line
                    print()