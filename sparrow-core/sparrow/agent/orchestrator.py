"""Agent orchestrator — the brain that connects intent, skills, and execution."""

from __future__ import annotations

from sparrow.agent.memory import ConversationMemory
from sparrow.approval.engine import ApprovalEngine
from sparrow.approval.policies import RiskLevel
from sparrow.audit.logger import audit_logger
from sparrow.gateway.protocol import UnifiedMessage, UnifiedResponse
from sparrow.llm.base import BaseLLM, LLMMessage
from sparrow.skills.registry import SkillRegistry

SYSTEM_PROMPT = """You are OpenSparrow 🐦, a helpful AI assistant for small teams.
You can manage files, execute commands, monitor systems, and schedule tasks on the work machine.

Available skills:
{skills}

When the user asks you to do something, respond with a clear plan of what you'll do.
For risky operations, explain what will happen and wait for approval.
Always be concise and helpful."""


class AgentOrchestrator:
    """Orchestrates the flow: intent → plan → approval → execution → response."""

    def __init__(self, llm: BaseLLM, skills: SkillRegistry, approval: ApprovalEngine):
        self.llm = llm
        self.skills = skills
        self.approval = approval
        self.memory = ConversationMemory()

    async def handle_message(self, message: UnifiedMessage) -> UnifiedResponse:
        """Process an incoming message and return a response."""
        user_id = message.user_id

        # Add user message to memory
        self.memory.add(user_id, "user", message.content)

        # Build LLM context
        skills_desc = "\n".join(
            f"- {s.name}: {s.description} (risk: {s.risk_level})"
            for s in self.skills.list_skills()
        )
        system = SYSTEM_PROMPT.format(skills=skills_desc)

        messages = [LLMMessage(role="system", content=system)]
        for entry in self.memory.get_history(user_id):
            messages.append(LLMMessage(role=entry["role"], content=entry["content"]))

        # Get LLM response
        try:
            response = await self.llm.chat(messages)
            reply = response.content
        except Exception as e:
            reply = f"⚠️ LLM error: {str(e)}"

        # Add assistant response to memory
        self.memory.add(user_id, "assistant", reply)

        # Log the interaction
        await audit_logger.log(
            user_id=user_id,
            action="chat.message",
            target=message.content[:100],
            result="success",
            channel=message.channel.value,
        )

        return UnifiedResponse(content=reply)
