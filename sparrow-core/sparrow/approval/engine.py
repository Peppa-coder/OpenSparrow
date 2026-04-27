"""Approval engine — manages approval workflow."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sparrow.approval.models import ApprovalRequest, ApprovalStatus
from sparrow.approval.policies import DEFAULT_POLICIES, RiskLevel, classify_command
from sparrow.auth.models import Role


class ApprovalEngine:
    """Manages the approval workflow for risky operations."""

    def __init__(self):
        self._pending: dict[str, ApprovalRequest] = {}
        self._history: list[ApprovalRequest] = []

    def needs_approval(self, skill_name: str, parameters: dict | None = None) -> RiskLevel:
        """Determine if an action needs approval."""
        # Special handling for shell commands
        if skill_name == "shell.execute" and parameters:
            command = parameters.get("command", "")
            return classify_command(command)

        return DEFAULT_POLICIES.get(skill_name, RiskLevel.CONFIRM)

    def create_request(self, skill_name: str, description: str,
                       parameters: dict, requested_by: str) -> ApprovalRequest:
        """Create a new approval request."""
        risk = self.needs_approval(skill_name, parameters)
        request = ApprovalRequest(
            skill_name=skill_name,
            description=description,
            parameters=parameters,
            risk_level=risk.value,
            requested_by=requested_by,
        )
        self._pending[request.id] = request
        return request

    def approve(self, request_id: str, reviewer: str, role: Role) -> ApprovalRequest:
        """Approve a pending request."""
        request = self._pending.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")

        if request.risk_level == RiskLevel.ADMIN_ONLY and role != Role.ADMIN:
            raise PermissionError("Only admins can approve this action")

        request.status = ApprovalStatus.APPROVED
        request.reviewed_by = reviewer
        request.reviewed_at = datetime.utcnow()

        self._history.append(self._pending.pop(request_id))
        return request

    def reject(self, request_id: str, reviewer: str) -> ApprovalRequest:
        """Reject a pending request."""
        request = self._pending.get(request_id)
        if not request:
            raise ValueError(f"Request {request_id} not found")

        request.status = ApprovalStatus.REJECTED
        request.reviewed_by = reviewer
        request.reviewed_at = datetime.utcnow()

        self._history.append(self._pending.pop(request_id))
        return request

    def list_pending(self) -> list[ApprovalRequest]:
        """List all pending approval requests."""
        return list(self._pending.values())

    def get_history(self, limit: int = 50) -> list[ApprovalRequest]:
        """Get approval history."""
        return self._history[-limit:]
