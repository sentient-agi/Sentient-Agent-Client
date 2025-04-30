from src.sentient_agent_client.sentient_agent_client import SentientAgentClient
from src.sentient_agent_client.sentient_agent_client_cli import SentientAgentClientCLI
import asyncio
import argparse

def main():
    parser = argparse.ArgumentParser(description='Sentient Agent Client CLI')
    parser.add_argument('--url', type=str, default="http://0.0.0.0:8000/assist",
                      help='URL of the agent (default: http://0.0.0.0:8000/assist)')
    
    args = parser.parse_args()
    
    client = SentientAgentClient()
    cli = SentientAgentClientCLI(client, args.url)
    asyncio.run(cli.chat())

if __name__ == "__main__":
    main()