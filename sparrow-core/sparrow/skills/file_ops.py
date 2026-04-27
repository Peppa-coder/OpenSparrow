"""File operations skill — browse, read, write, search files in workspace."""

from __future__ import annotations

from sparrow.skills.registry import SkillDef


async def list_files(path: str = ".", **kwargs) -> dict:
    """List files in a directory within the workspace."""
    # Delegates to local agent via WebSocket
    return {"action": "file.list", "path": path}


async def read_file(path: str, **kwargs) -> dict:
    """Read a file's content."""
    return {"action": "file.read", "path": path}


async def write_file(path: str, content: str, **kwargs) -> dict:
    """Write content to a file."""
    return {"action": "file.write", "path": path, "content": content}


async def search_files(query: str, path: str = ".", **kwargs) -> dict:
    """Search for files by name or content."""
    return {"action": "file.search", "query": query, "path": path}


FILE_SKILLS = [
    SkillDef(name="file.list", description="List files and directories", handler=list_files, risk_level="low"),
    SkillDef(name="file.read", description="Read file content", handler=read_file, risk_level="low"),
    SkillDef(name="file.write", description="Write content to a file", handler=write_file, risk_level="medium"),
    SkillDef(name="file.search", description="Search files by name or content", handler=search_files, risk_level="low"),
]
