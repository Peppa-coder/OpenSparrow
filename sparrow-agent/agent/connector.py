"""WebSocket connector — outbound connection to the control plane."""

from __future__ import annotations

import asyncio
import json

import websockets

from agent.executor import CommandExecutor
from agent.file_manager import FileManager
from agent.monitor import SystemMonitor
from agent.sandbox import Sandbox


class AgentConnector:
    """Maintains outbound WebSocket connection to the control plane."""

    def __init__(self, core_url: str, token: str, workspace: str):
        self.core_url = core_url
        self.token = token
        self.workspace = workspace
        self._running = False
        self._ws = None

        # Initialize subsystems
        self.sandbox = Sandbox(workspace_root=workspace)
        self.file_manager = FileManager(sandbox=self.sandbox)
        self.executor = CommandExecutor(sandbox=self.sandbox)
        self.monitor = SystemMonitor()

    async def start(self):
        """Start the agent and maintain connection with auto-reconnect."""
        self._running = True
        while self._running:
            try:
                await self._connect()
            except Exception as e:
                print(f"⚠️ Connection error: {e}")
                if self._running:
                    print("   Reconnecting in 5 seconds...")
                    await asyncio.sleep(5)

    async def stop(self):
        """Stop the agent."""
        self._running = False
        if self._ws:
            await self._ws.close()
        print("🐦 Agent stopped")

    async def _connect(self):
        """Establish WebSocket connection and process messages."""
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        async with websockets.connect(self.core_url, extra_headers=headers) as ws:
            self._ws = ws
            print("✅ Connected to control plane")

            # Send registration
            await ws.send(json.dumps({
                "type": "agent.register",
                "workspace": self.workspace,
                "capabilities": ["file_ops", "shell", "monitor"],
            }))

            async for raw in ws:
                try:
                    msg = json.loads(raw)
                    response = await self._handle_message(msg)
                    if response:
                        await ws.send(json.dumps(response))
                except json.JSONDecodeError:
                    print(f"⚠️ Invalid message received")
                except Exception as e:
                    await ws.send(json.dumps({
                        "type": "error",
                        "request_id": msg.get("request_id"),
                        "error": str(e),
                    }))

    async def _handle_message(self, msg: dict) -> dict | None:
        """Route incoming messages to the appropriate handler."""
        action = msg.get("action", "")
        request_id = msg.get("request_id", "")

        handlers = {
            "file.list": self.file_manager.list_files,
            "file.read": self.file_manager.read_file,
            "file.write": self.file_manager.write_file,
            "file.search": self.file_manager.search_files,
            "shell.execute": self.executor.execute,
            "monitor.status": self.monitor.get_status,
            "ping": self._handle_ping,
        }

        handler = handlers.get(action)
        if handler is None:
            return {"type": "error", "request_id": request_id, "error": f"Unknown action: {action}"}

        result = await handler(**msg.get("params", {}))
        return {"type": "result", "request_id": request_id, "data": result}

    async def _handle_ping(self, **kwargs) -> dict:
        return {"status": "pong"}
