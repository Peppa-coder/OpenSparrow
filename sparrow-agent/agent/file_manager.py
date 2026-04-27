"""File manager — sandboxed file operations."""

from __future__ import annotations

import os
from pathlib import Path

from agent.sandbox import Sandbox


class FileManager:
    """Handles file operations within the sandboxed workspace."""

    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    async def list_files(self, path: str = ".", **kwargs) -> dict:
        """List files in a directory."""
        target = self.sandbox.validate_path(path)

        if not target.exists():
            return {"error": f"Path not found: {path}"}

        if not target.is_dir():
            return {"error": f"Not a directory: {path}"}

        entries = []
        for item in sorted(target.iterdir()):
            try:
                stat = item.stat()
                entries.append({
                    "name": item.name,
                    "path": str(item.relative_to(self.sandbox.workspace_root)),
                    "is_dir": item.is_dir(),
                    "size": stat.st_size if item.is_file() else 0,
                    "modified": stat.st_mtime,
                })
            except PermissionError:
                continue

        return {"path": path, "entries": entries}

    async def read_file(self, path: str, **kwargs) -> dict:
        """Read a file's content."""
        target = self.sandbox.validate_path(path)

        if not target.exists():
            return {"error": f"File not found: {path}"}

        if not target.is_file():
            return {"error": f"Not a file: {path}"}

        # Size limit: 1MB
        if target.stat().st_size > 1_048_576:
            return {"error": "File too large (>1MB). Use download instead."}

        try:
            content = target.read_text(encoding="utf-8")
            return {"path": path, "content": content, "size": len(content)}
        except UnicodeDecodeError:
            return {"error": "Binary file — cannot display as text"}

    async def write_file(self, path: str, content: str, **kwargs) -> dict:
        """Write content to a file."""
        target = self.sandbox.validate_path(path)

        # Create parent directories
        target.parent.mkdir(parents=True, exist_ok=True)

        target.write_text(content, encoding="utf-8")
        return {"path": path, "size": len(content), "status": "written"}

    async def search_files(self, query: str, path: str = ".", **kwargs) -> dict:
        """Search for files by name pattern."""
        target = self.sandbox.validate_path(path)

        if not target.is_dir():
            return {"error": f"Not a directory: {path}"}

        matches = []
        for item in target.rglob(f"*{query}*"):
            try:
                matches.append({
                    "name": item.name,
                    "path": str(item.relative_to(self.sandbox.workspace_root)),
                    "is_dir": item.is_dir(),
                })
            except (PermissionError, ValueError):
                continue

            if len(matches) >= 100:  # Limit results
                break

        return {"query": query, "matches": matches}
