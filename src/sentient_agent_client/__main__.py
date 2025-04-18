from src.sentient_agent_client.sentient_agent_client import SentientAgentClient
from src.sentient_agent_client.sentient_agent_client_cli import SentientAgentClientCLI
import asyncio

def main():
    client = SentientAgentClient()
    cli = SentientAgentClientCLI(client)
    asyncio.run(cli.chat())

if __name__ == "__main__":
    main()