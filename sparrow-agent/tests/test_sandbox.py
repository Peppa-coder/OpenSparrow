"""Test sandbox security."""

import pytest
import tempfile
from pathlib import Path

from agent.sandbox import Sandbox, SandboxViolation


@pytest.fixture
def sandbox(tmp_path):
    return Sandbox(str(tmp_path / "workspace"))


def test_workspace_created(sandbox):
    assert sandbox.workspace_root.exists()


def test_valid_path(sandbox):
    result = sandbox.validate_path("test.txt")
    assert str(result).startswith(str(sandbox.workspace_root))


def test_path_traversal_blocked(sandbox):
    with pytest.raises(SandboxViolation):
        sandbox.validate_path("../../etc/passwd")


def test_absolute_path_outside_blocked(sandbox):
    with pytest.raises(SandboxViolation):
        sandbox.validate_path("/etc/passwd")


def test_dangerous_command_blocked(sandbox):
    is_safe, reason = sandbox.is_safe_command("rm -rf /")
    assert not is_safe


def test_safe_command_allowed(sandbox):
    is_safe, reason = sandbox.is_safe_command("ls -la")
    assert is_safe
