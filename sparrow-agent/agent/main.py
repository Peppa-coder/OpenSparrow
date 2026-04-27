"""Local Agent entry point."""

from __future__ import annotations

import argparse
import asyncio
import signal

from agent.connector import AgentConnector


async def run_agent(core_url: str, token: str, workspace: str):
    """Main agent loop."""
    connector = AgentConnector(core_url=core_url, token=token, workspace=workspace)

    # Graceful shutdown
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: asyncio.create_task(connector.stop()))

    print(f"🐦 OpenSparrow Agent starting")
    print(f"   Connecting to: {core_url}")
    print(f"   Workspace: {workspace}")

    await connector.start()


def cli_entry():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="OpenSparrow Local Agent")
    parser.add_argument("--core-url", default="ws://localhost:8081/ws/agent",
                        help="WebSocket URL of the control plane")
    parser.add_argument("--token", default="", help="Authentication token")
    parser.add_argument("--workspace", default="~/sparrow-workspace",
                        help="Workspace root directory")
    args = parser.parse_args()

    asyncio.run(run_agent(args.core_url, args.token, args.workspace))


if __name__ == "__main__":
    cli_entry()
