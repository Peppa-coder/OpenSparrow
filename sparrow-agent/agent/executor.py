"""Command executor — sandboxed shell command execution."""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

from agent.sandbox import Sandbox


@dataclass
class ExecutionResult:
    command: str
    return_code: int
    stdout: str
    stderr: str


class CommandExecutor:
    """Executes shell commands within sandbox constraints."""

    MAX_OUTPUT_SIZE = 65536  # 64KB max output
    DEFAULT_TIMEOUT = 30    # 30 seconds default timeout

    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    async def execute(self, command: str, timeout: int | None = None, **kwargs) -> dict:
        """Execute a shell command in the workspace directory."""
        # Safety check
        is_safe, reason = self.sandbox.is_safe_command(command)
        if not is_safe:
            return {"error": f"Command blocked: {reason}", "command": command}

        timeout = timeout or self.DEFAULT_TIMEOUT

        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(self.sandbox.workspace_root),
                env={**os.environ, "HOME": str(self.sandbox.workspace_root)},
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )

            stdout_str = stdout.decode("utf-8", errors="replace")[:self.MAX_OUTPUT_SIZE]
            stderr_str = stderr.decode("utf-8", errors="replace")[:self.MAX_OUTPUT_SIZE]

            return {
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout_str,
                "stderr": stderr_str,
            }

        except asyncio.TimeoutError:
            process.kill()
            return {
                "command": command,
                "error": f"Command timed out after {timeout}s",
                "return_code": -1,
            }
        except Exception as e:
            return {
                "command": command,
                "error": str(e),
                "return_code": -1,
            }
