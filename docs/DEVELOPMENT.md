# OpenSparrow 详细开发文档

> **版本**: v0.1.0-draft | **最后更新**: 2026-04-28
>
> 本文档是 OpenSparrow 项目的完整开发指南。面向所有贡献者和希望深入理解系统设计的开发者。

---

## 目录

1. [项目愿景与定位](#1-项目愿景与定位)
2. [竞品分析与借鉴](#2-竞品分析与借鉴)
3. [核心架构设计](#3-核心架构设计)
4. [Agentic Loop（智能体循环）详解](#4-agentic-loop智能体循环详解)
5. [Tool System（工具系统）设计](#5-tool-system工具系统设计)
6. [Channel Gateway（渠道网关）设计](#6-channel-gateway渠道网关设计)
7. [安全模型详解](#7-安全模型详解)
8. [LLM 适配层设计](#8-llm-适配层设计)
9. [Web UI 设计](#9-web-ui-设计)
10. [数据库设计](#10-数据库设计)
11. [部署架构](#11-部署架构)
12. [API 设计规范](#12-api-设计规范)
13. [开发规范与流程](#13-开发规范与流程)
14. [分阶段实施计划](#14-分阶段实施计划)
15. [附录：关键数据结构](#15-附录关键数据结构)

---

## 1. 项目愿景与定位

### 1.1 一句话定义

**OpenSparrow 是一个自托管的轻量级 AI Agent，让小型团队通过 Web 界面或通讯软件（Telegram/Slack/飞书）远程控制工作机上的文件、命令行和自动化任务。**

### 1.2 设计哲学

| 原则 | 含义 |
|------|------|
| **麻雀虽小，五脏俱全** | 一个工具覆盖 80% 的使用场景，而非 5000 个插件覆盖 100% |
| **5 分钟原则** | 从 `git clone` 到可用，不超过 5 分钟 |
| **安全即默认** | 所有危险操作默认需要审批，而非默认允许 |
| **非技术用户友好** | Web 设置向导、引导式操作，不需要编辑 YAML |
| **自托管优先** | 数据永不离开你的机器，除非你主动调用云端 LLM |

### 1.3 目标用户画像

- 5-20 人的创业团队 / 实验室 / 工作室
- 团队中有 1-2 名技术人员负责部署，其余成员通过 Web/聊天使用
- 需要远程管理一台或几台开发/生产服务器
- 希望用自然语言代替 SSH 操作

### 1.4 非目标（Explicit Non-Goals）

- **不是** 通用 AI 平台（不做训练、微调、向量数据库）
- **不是** 企业级多租户 SaaS
- **不是** 全自主 Agent（不会在没有人类确认的情况下执行危险操作）
- **不是** IDE 或代码编辑器

---

## 2. 竞品分析与借鉴

### 2.1 Claude Code — Anthropic 的 Agent 架构

Claude Code 是 Anthropic 官方的编程 Agent，其核心架构思想对 OpenSparrow 有重要参考价值。

#### 2.1.1 核心模式：Agentic Tool-Use Loop

Claude Code 的核心是一个 **client-executed agentic loop**（客户端执行的智能体循环）：

```
用户消息 → LLM 推理 → 决定调用工具
    ↓
返回 tool_use（工具名 + 参数）
    ↓
客户端执行工具 → 返回 tool_result
    ↓
LLM 继续推理（可能再次调用工具）
    ↓
循环直到 stop_reason != "tool_use"
    ↓
返回最终文本响应给用户
```

这个循环的关键设计：
- **LLM 永远不直接执行任何操作** — 它只是输出结构化的 "请求"
- **客户端（你的代码）负责所有执行** — 安全边界在你手中
- **循环可能运行多次** — 一个任务可能需要多次工具调用
- **错误可恢复** — 工具返回 `is_error: true` 时 LLM 会尝试修正

#### 2.1.2 三类工具设计

| 类型 | 执行方 | 示例 | OpenSparrow 对应 |
|------|--------|------|-----------------|
| User-defined tools | 客户端 | 自定义 API 调用 | Skills 系统 |
| Anthropic-schema tools | 客户端 | `bash`, `text_editor` | Shell/File 技能 |
| Server-executed tools | Anthropic 服务器 | `web_search` | 暂不实现 |

#### 2.1.3 Channels 机制

Claude Code 支持通过 Telegram、Discord、iMessage、Webhook 等渠道推送事件到 Agent session。这与 OpenSparrow 的 Channel Gateway 设计高度一致。

**OpenSparrow 借鉴点：**
- ✅ Agentic Loop 模式（核心采纳）
- ✅ 工具定义与执行分离
- ✅ 多渠道统一接入
- ✅ 错误恢复机制
- ✅ 持久化指令文件（CLAUDE.md → SPARROW.md）
- ⚠️ 简化工具类型（只做 client-executed）
- ❌ 不做 server-executed tools（保持自托管）

---

### 2.2 OpenClaw — 开源 Agent 框架

OpenClaw（160K+ Stars）是目前最完整的开源 Agent 框架，采用 Brain/Muscle 分离架构。

#### 2.2.1 核心架构：Brain + Muscle

```
┌─────────────────────────────────────────┐
│              OpenClaw Gateway            │
│  WhatsApp │ Telegram │ Email │ Web      │
├─────────────────────────────────────────┤
│           Task Orchestrator (Brain)      │
│  意图理解 → 任务分解 → 子任务调度         │
├─────────────────────────────────────────┤
│              LLM Backend                 │
│  Claude │ GPT │ DeepSeek │ Ollama       │
├─────────────────────────────────────────┤
│           Executor / Sandbox (Muscle)    │
│  Docker 隔离容器内执行所有操作            │
│  File │ Shell │ Web │ Browser           │
└─────────────────────────────────────────┘
```

#### 2.2.2 关键设计决策

| 设计点 | OpenClaw 做法 | OpenSparrow 简化 |
|--------|--------------|-----------------|
| 沙盒 | Docker 容器隔离 | Workspace 路径沙盒 + 非 root 用户 |
| 插件 | 5700+ Marketplace | 20 个内建技能 |
| 内存 | 复杂持久化 + Dreaming | SQLite + 滑动窗口 |
| 渠道 | 20+ 平台 | 4 个核心渠道 |
| 配置 | YAML + 代码 | Web 向导 |
| 调度 | 分布式多机 | 单机 cron |
| LLM | 35+ 供应商 | 3 核心 + Ollama |

#### 2.2.3 OpenClaw 的 Dreaming Engine

OpenClaw 有一个独特的 "Dreaming" 机制：在空闲时重新处理过去的对话和文件，改善记忆关联。

**OpenSparrow 简化版：** V1 不实现。V3 可考虑轻量版——在后台汇总对话历史，生成每日摘要。

---

### 2.3 架构对比总表

| 维度 | Claude Code | OpenClaw | **OpenSparrow** |
|------|------------|----------|-----------------|
| 定位 | 编程助手 | 通用自主 Agent | 轻量远程控制 Agent |
| 执行模型 | Client agentic loop | Brain+Muscle sandbox | Dual-process agentic loop |
| 安全 | 用户审批 + 权限系统 | Docker sandbox | 审批引擎 + 路径沙盒 |
| 渠道 | Terminal + Channels | 20+ 平台 | Web + 3 通讯渠道 |
| LLM | Anthropic 专属 | 35+ 供应商 | 3 供应商 + Ollama |
| 部署 | npm install | docker-compose | docker-compose / pip |
| 开源 | 部分开源 | 完全开源 | 完全开源 |
| 复杂度 | 中 | 极高 | **低** |

---

## 3. 核心架构设计

### 3.1 双进程架构

OpenSparrow 的核心架构创新是 **Control Plane + Local Agent 双进程模型**：

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户触达层                                │
│                                                                 │
│   ┌─────────┐    ┌──────────────┐    ┌────────┐    ┌────────┐  │
│   │ Web UI  │    │ Telegram Bot │    │ Slack  │    │Webhook │  │
│   │ (Vue 3) │    │   Adapter    │    │Adapter │    │  API   │  │
│   └────┬────┘    └──────┬───────┘    └───┬────┘    └───┬────┘  │
│        └────────────────┴───────────────┴─────────────┘        │
│                         │                                       │
│              Unified Message Protocol                           │
│                         │                                       │
├─────────────────────────┼───────────────────────────────────────┤
│                                                                 │
│                 CONTROL PLANE (sparrow-core)                     │
│                 Python / FastAPI / SQLite                        │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │  ┌────────────┐  ┌────────────────┐  ┌──────────────┐   │  │
│   │  │  Auth &    │  │    Agent       │  │   LLM        │   │  │
│   │  │  RBAC      │  │  Orchestrator  │──│   Adapter    │   │  │
│   │  │            │  │  (Agentic Loop)│  │              │   │  │
│   │  └────────────┘  └───────┬────────┘  └──────────────┘   │  │
│   │                          │                               │  │
│   │  ┌────────────┐  ┌──────┴─────────┐  ┌──────────────┐   │  │
│   │  │  Approval  │  │    Skill       │  │   Audit      │   │  │
│   │  │  Engine    │──│   Registry     │  │   Logger     │   │  │
│   │  │            │  │                │  │              │   │  │
│   │  └────────────┘  └────────────────┘  └──────────────┘   │  │
│   │                                                          │  │
│   │  ┌────────────┐  ┌────────────────┐                      │  │
│   │  │ Scheduler  │  │   SQLite DB    │                      │  │
│   │  │ (APSchedule│  │   (aiosqlite)  │                      │  │
│   │  └────────────┘  └────────────────┘                      │  │
│   │                                                          │  │
│   └──────────────────────────────────────────────────────────┘  │
│                         │                                       │
│              WebSocket (Agent → Core, 出站连接)                  │
│                         │                                       │
├─────────────────────────┼───────────────────────────────────────┤
│                                                                 │
│                 LOCAL AGENT (sparrow-agent)                      │
│                 Python / 轻量进程                                │
│                                                                 │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │                                                          │  │
│   │  ┌────────────┐  ┌────────────────┐  ┌──────────────┐   │  │
│   │  │  Sandbox   │  │  File Manager  │  │   Shell      │   │  │
│   │  │  (路径校验  │  │  (浏览/读写/   │  │  Executor   │   │  │
│   │  │   + 安全)  │  │    搜索文件)   │  │  (命令执行)  │   │  │
│   │  └────────────┘  └────────────────┘  └──────────────┘   │  │
│   │                                                          │  │
│   │  ┌────────────┐  ┌────────────────┐                      │  │
│   │  │  System    │  │  WebSocket     │                      │  │
│   │  │  Monitor   │  │  Connector     │                      │  │
│   │  │(CPU/RAM/磁盘)│  │ (自动重连)     │                      │  │
│   │  └────────────┘  └────────────────┘                      │  │
│   │                                                          │  │
│   │      ↕  所有操作限定在 workspace_root 范围内               │  │
│   │         默认: ~/sparrow-workspace                         │  │
│   │                                                          │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 为什么是双进程而非单容器

| 方案 | 优点 | 致命缺陷 |
|------|------|---------|
| **单容器** | 部署简单 | 容器访问宿主文件需 bind mount 或 privileged mode，安全性极差 |
| **双进程** ✅ | 清晰安全边界 | 需要管理两个进程（Docker Compose 解决） |

Local Agent 以**出站 WebSocket** 连接 Control Plane，意味着：
- 工作机不暴露任何端口
- Control Plane 可以安全地放在容器或远程服务器
- 安全边界清晰：Web/Chat 层永远无法直接触及文件系统

### 3.3 进程间通信协议

Control Plane 和 Local Agent 之间通过 WebSocket 传输 JSON 消息：

```json
// Control Plane → Local Agent (请求)
{
  "request_id": "uuid-v4",
  "action": "file.list",
  "params": {
    "path": "src/"
  }
}

// Local Agent → Control Plane (响应)
{
  "type": "result",
  "request_id": "uuid-v4",
  "data": {
    "path": "src/",
    "entries": [
      {"name": "main.py", "is_dir": false, "size": 1234},
      {"name": "tests/", "is_dir": true, "size": 0}
    ]
  }
}

// Local Agent → Control Plane (错误)
{
  "type": "error",
  "request_id": "uuid-v4",
  "error": "SandboxViolation: Path outside workspace boundary"
}
```

---

## 4. Agentic Loop（智能体循环）详解

### 4.1 概述

Agentic Loop 是 OpenSparrow 的核心引擎，借鉴 Claude Code 的 tool-use loop 模式，但增加了**审批门**和**多渠道适配**。

### 4.2 完整流程图

```
                    ┌─────────────────┐
                    │  用户发送消息     │
                    │ (Web/TG/Slack)  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Channel Adapter │
                    │  → UnifiedMessage│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Message Router  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Agent          │
                    │  Orchestrator   │
                    └────────┬────────┘
                             │
                ┌────────────▼────────────┐
                │  构建 LLM Context        │
                │  [system_prompt]         │
                │  [conversation_history]  │
                │  [available_tools]       │
                └────────────┬────────────┘
                             │
              ┌──────────────▼──────────────┐
              │         LLM 推理             │
              │  "我应该调用什么工具？"         │
              └──────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │  stop_reason?   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼──────┐      │     ┌────────▼──────┐
     │ "tool_use"    │      │     │ "end_turn"    │
     │ 需要调用工具   │      │     │ 最终回复      │
     └────────┬──────┘      │     └────────┬──────┘
              │              │              │
     ┌────────▼──────┐      │     ┌────────▼──────┐
     │  Approval     │      │     │  返回给用户    │
     │  Engine       │      │     │  记录审计日志  │
     │  风险评估      │      │     └───────────────┘
     └────────┬──────┘      │
              │              │
    ┌─────────┼──────────┐  │
    │         │          │  │
┌───▼──┐ ┌───▼───┐ ┌────▼────┐
│ AUTO │ │CONFIRM│ │FORBIDDEN│
│自动执行│ │需审批  │ │ 直接拒绝 │
└───┬──┘ └───┬───┘ └────┬────┘
    │        │          │
    │   ┌────▼────┐     │
    │   │ 等待用户 │     │
    │   │ 审批/拒绝│     │
    │   └────┬────┘     │
    │        │          │
    ▼        ▼          ▼
┌───────────────┐  ┌─────────────┐
│ Execute Tool  │  │ Return Error│
│ via WebSocket │  │ to LLM      │
│ → Local Agent │  └─────────────┘
└───────┬───────┘
        │
┌───────▼───────┐
│  tool_result  │
│  返回给 LLM   │
└───────┬───────┘
        │
        └──→ 回到 "LLM 推理" (循环继续)
```

### 4.3 核心代码：Agentic Loop 伪代码

```python
class AgentOrchestrator:
    """核心编排器 — 驱动 Agentic Loop"""

    async def handle_message(self, message: UnifiedMessage) -> UnifiedResponse:
        # 1. 加入对话历史
        self.memory.add(message.user_id, "user", message.content)

        # 2. 构建 LLM 上下文
        context = self._build_context(message.user_id)

        # 3. Agentic Loop
        max_iterations = 10  # 防止无限循环
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # 4. 调用 LLM
            response = await self.llm.chat(
                messages=context,
                tools=self.skills.list_for_llm(),  # 传入可用工具定义
            )

            # 5. 检查停止原因
            if response.stop_reason == "end_turn":
                # LLM 给出了最终回复
                final_text = response.content
                self.memory.add(message.user_id, "assistant", final_text)
                await self.audit.log(message.user_id, "chat.response", final_text[:100])
                return UnifiedResponse(content=final_text)

            if response.stop_reason == "tool_use":
                # LLM 想调用工具
                for tool_call in response.tool_calls:
                    result = await self._execute_tool_call(
                        tool_call, message.user_id, message.channel
                    )
                    # 将结果追加到上下文
                    context.append({
                        "role": "tool_result",
                        "tool_use_id": tool_call.id,
                        "content": json.dumps(result),
                        "is_error": result.get("error") is not None,
                    })

                continue  # 继续循环，让 LLM 处理工具结果

        # 超过最大迭代次数
        return UnifiedResponse(content="⚠️ 任务过于复杂，请分步操作。")

    async def _execute_tool_call(self, tool_call, user_id, channel):
        """执行单个工具调用（带审批检查）"""

        skill = self.skills.get(tool_call.name)
        if not skill:
            return {"error": f"Unknown tool: {tool_call.name}"}

        # 审批检查
        risk = self.approval.needs_approval(tool_call.name, tool_call.params)

        if risk == RiskLevel.FORBIDDEN:
            await self.audit.log(user_id, tool_call.name, result="forbidden")
            return {"error": "This operation is forbidden for security reasons."}

        if risk == RiskLevel.AUTO:
            # 低风险，直接执行
            pass

        elif risk in (RiskLevel.CONFIRM, RiskLevel.ADMIN_ONLY):
            # 需要审批
            approval_request = self.approval.create_request(
                skill_name=tool_call.name,
                description=f"Execute: {tool_call.name}({tool_call.params})",
                parameters=tool_call.params,
                requested_by=user_id,
            )
            # 推送审批请求到所有渠道
            await self._push_approval_request(approval_request, channel)
            # 等待审批（带超时）
            approved = await self._wait_for_approval(approval_request.id, timeout=300)
            if not approved:
                return {"error": "Operation rejected or timed out."}

        # 执行工具
        try:
            result = await self._send_to_agent(tool_call.name, tool_call.params)
            await self.audit.log(user_id, tool_call.name, result="success", channel=channel)
            return result
        except Exception as e:
            await self.audit.log(user_id, tool_call.name, result="error", details=str(e))
            return {"error": str(e), "is_error": True}
```

### 4.4 与 Claude Code 的 Agentic Loop 对比

| 方面 | Claude Code | OpenSparrow |
|------|------------|-------------|
| 循环驱动 | while stop_reason == "tool_use" | 相同 |
| 工具执行 | 客户端执行 | 通过 WebSocket 委托给 Local Agent |
| 错误处理 | is_error: true → LLM 重试 | 相同 + 审计日志 |
| 并行工具 | 支持多个 tool_use 块 | 支持（串行执行，后续可并行） |
| **审批门** | 无（用户通过权限系统控制） | **有，风险分级审批** ← 核心差异 |
| 最大迭代 | 无限制（靠 token 限制自然停止） | 10 次（可配置） |

### 4.5 System Prompt 设计

System Prompt 是 Agent 行为的 "宪法"。参考 Claude Code 的 CLAUDE.md 机制：

```python
SYSTEM_PROMPT = """You are OpenSparrow 🐦, a helpful AI assistant for small teams.

## Your Identity
- You are running on the user's work machine
- You can manage files, execute commands, monitor systems, and schedule tasks
- You always explain what you're about to do before doing it
- For risky operations, you propose a plan and wait for approval

## Available Tools
{tools_json}

## Safety Rules
1. NEVER execute commands that could damage the system (rm -rf /, mkfs, etc.)
2. ALWAYS stay within the workspace boundary: {workspace_root}
3. For file writes, shell commands, and system changes: explain what will happen first
4. If unsure, ASK the user instead of guessing
5. Redact any secrets, tokens, or passwords in your responses

## Response Style
- Be concise and practical
- Use emoji sparingly for readability
- Format file contents and command outputs in code blocks
- When listing files, use a clean table format
- Always confirm the result of an action

## Context
- Workspace: {workspace_root}
- Platform: {platform}
- Current time: {current_time}
- User role: {user_role}
"""
```

**可扩展点：** 用户可在 workspace 根目录放置 `SPARROW.md` 文件，内容会被追加到 System Prompt（类似 Claude Code 的 `CLAUDE.md`）。

---

## 5. Tool System（工具系统）设计

### 5.1 设计理念

借鉴 Claude Code 和 OpenClaw 的工具系统，但做极致简化：

- **Claude Code**: 工具定义为 JSON Schema，LLM 通过 function calling 调用
- **OpenClaw**: 工具以 Plugin/Skill 形式存在，支持 Marketplace
- **OpenSparrow**: 内建 Skill，统一注册，LLM 通过 function calling 使用

### 5.2 Skill 定义规范

每个 Skill 遵循统一接口：

```python
@dataclass
class SkillDef:
    """工具/技能的完整定义"""
    name: str                    # 唯一标识 "file.read"
    description: str             # LLM 可读的描述
    handler: AsyncCallable       # 异步执行函数
    risk_level: RiskLevel        # AUTO / CONFIRM / ADMIN_ONLY / FORBIDDEN
    parameters: dict             # JSON Schema 格式的参数定义
    requires_agent: bool = True  # 是否需要 Local Agent 执行
    category: str = "general"    # 分类：file / shell / monitor / schedule / notify
```

### 5.3 参数传递给 LLM 的格式

将 Skill 列表转换为 Anthropic/OpenAI function calling 格式：

```json
{
  "tools": [
    {
      "name": "file.list",
      "description": "List files and directories in a path within the workspace",
      "input_schema": {
        "type": "object",
        "properties": {
          "path": {
            "type": "string",
            "description": "Relative path within workspace. Default: current directory",
            "default": "."
          }
        }
      }
    },
    {
      "name": "shell.execute",
      "description": "Execute a shell command on the work machine. REQUIRES APPROVAL for most commands.",
      "input_schema": {
        "type": "object",
        "properties": {
          "command": {
            "type": "string",
            "description": "The shell command to execute"
          },
          "timeout": {
            "type": "integer",
            "description": "Timeout in seconds (default: 30, max: 300)",
            "default": 30
          }
        },
        "required": ["command"]
      }
    }
  ]
}
```

### 5.4 V1 内建 Skill 清单

| 技能 | 名称 | 风险级别 | 说明 |
|------|------|---------|------|
| 📂 列出文件 | `file.list` | AUTO | 浏览目录结构 |
| 📄 读取文件 | `file.read` | AUTO | 读取文件内容（≤1MB） |
| ✏️ 写入文件 | `file.write` | CONFIRM | 创建或覆盖文件 |
| 🔍 搜索文件 | `file.search` | AUTO | 按名称模式搜索 |
| ⚡ 执行命令 | `shell.execute` | CONFIRM/ADMIN | 运行 shell 命令 |
| 📊 系统状态 | `monitor.status` | AUTO | CPU/内存/磁盘用量 |
| ⏰ 添加定时 | `scheduler.add` | CONFIRM | 添加 cron 任务 |
| 📋 查看定时 | `scheduler.list` | AUTO | 查看所有定时任务 |
| 🗑️ 删除定时 | `scheduler.remove` | CONFIRM | 删除定时任务 |
| 📢 广播通知 | `notify.broadcast` | AUTO | 向团队渠道发通知 |

### 5.5 工具执行的完整路径

```
LLM 输出 tool_use("file.read", {"path": "config.yml"})
    │
    ▼
Orchestrator 收到 tool_call
    │
    ▼
SkillRegistry.get("file.read") → SkillDef
    │
    ▼
ApprovalEngine.needs_approval("file.read", params) → RiskLevel.AUTO
    │
    ▼
skill.requires_agent == True → 通过 WebSocket 发送到 Local Agent
    │
    ▼
Agent Connector._handle_message({"action": "file.read", "params": {"path": "config.yml"}})
    │
    ▼
FileManager.read_file("config.yml")
    │
    ▼
Sandbox.validate_path("config.yml") → ~/sparrow-workspace/config.yml ✅
    │
    ▼
读取文件内容 → 返回 {"path": "config.yml", "content": "...", "size": 256}
    │
    ▼
WebSocket → Orchestrator → 追加到 LLM context 作为 tool_result
    │
    ▼
LLM 继续推理...
```

---

## 6. Channel Gateway（渠道网关）设计

### 6.1 设计原则

参考 Claude Code Channels 和 OpenClaw Gateway 的经验：

1. **不追求跨渠道一致性** — 每个渠道有自己的能力声明
2. **小核心 + 能力标记** — 统一消息只包含最小公共集
3. **适配器模式** — 每个渠道一个 Adapter，实现统一接口

### 6.2 统一消息协议（UMP）

```python
class UnifiedMessage(BaseModel):
    """跨渠道的统一消息表示"""
    id: str                           # UUID
    channel: ChannelType              # web / telegram / slack / webhook
    user_id: str                      # 渠道内的用户标识
    user_name: str                    # 显示名
    thread_id: str | None             # 线程/会话 ID（如支持）
    content: str                      # 纯文本内容
    attachments: list[Attachment]     # 附件
    actions: list[Action]             # 交互按钮（如支持）
    metadata: dict[str, Any]          # 渠道特有数据透传
    timestamp: datetime

class ChannelCapabilities(BaseModel):
    """渠道能力声明 — 不是所有渠道都一样"""
    supports_threads: bool        # 是否支持线程回复
    supports_buttons: bool        # 是否支持交互按钮
    supports_file_upload: bool    # 是否支持文件上传
    supports_edit: bool           # 是否支持编辑已发消息
    supports_markdown: bool       # 是否支持 Markdown 格式
    max_message_length: int       # 最大消息长度
```

### 6.3 Adapter 接口规范

```python
class BaseChannelAdapter(ABC):
    """所有渠道适配器的基类"""

    channel_type: ChannelType
    capabilities: ChannelCapabilities

    @abstractmethod
    async def start(self) -> None:
        """启动适配器（如开始 polling 或注册 webhook）"""

    @abstractmethod
    async def stop(self) -> None:
        """停止适配器"""

    @abstractmethod
    async def send_response(self, response: UnifiedResponse,
                            original: UnifiedMessage) -> None:
        """将 Agent 回复发送到该渠道"""

    @abstractmethod
    async def send_approval_request(self, request: ApprovalRequest,
                                     target_user: str) -> None:
        """推送审批请求（如有交互按钮能力，使用按钮）"""
```

### 6.4 渠道适配器实现规划

| 渠道 | 版本 | 接入方式 | 特殊能力 |
|------|------|---------|---------|
| **Web** | V1 | WebSocket | 全能力：文件上传、按钮、实时流 |
| **Telegram** | V1 | Bot API Long Polling | Inline Keyboard 审批按钮 |
| **Slack** | V2 | Bot + Events API | Slash commands、Block Kit |
| **飞书/钉钉** | V2 | 机器人 Webhook | 消息卡片 |
| **Webhook** | V1 | HTTP POST/GET | 基础文本，无交互 |

### 6.5 消息流转示例

```
Telegram 用户发送 "查看服务器状态"
    │
    ▼
TelegramAdapter 收到 Update
    │
    ▼
_to_unified(update) → UnifiedMessage(
    channel="telegram",
    user_id="12345",
    user_name="alice",
    content="查看服务器状态"
)
    │
    ▼
MessageRouter.route(message) → AgentOrchestrator.handle_message(message)
    │
    ▼
(Agentic Loop runs...)
    │
    ▼
UnifiedResponse(content="📊 系统状态:\n- CPU: 23%\n- 内存: 4.2/8.0 GB (52%)\n- 磁盘: 120/250 GB (48%)")
    │
    ▼
TelegramAdapter.send_response(response, original_message)
    │
    ▼
调用 Telegram Bot API: sendMessage(chat_id=12345, text="📊 系统状态:...")
```

---

## 7. 安全模型详解

### 7.1 威胁模型

OpenSparrow 本质是一个 **远程管理工具 + AI 接口**，必须严肃对待安全：

| 威胁 | 风险等级 | 攻击面 | 缓解措施 |
|------|---------|-------|---------|
| 未授权访问 | 🔴 高 | Web UI / Chat Bot | JWT + RBAC |
| 路径遍历 | 🔴 高 | 文件操作 | 路径沙盒 + resolve-and-check |
| 命令注入 | 🔴 高 | Shell 执行 | 审批门 + 命令黑名单 + 非 root |
| Prompt 注入 | 🟡 中 | LLM 交互 | System Prompt 加固 + 工具权限 |
| 密钥泄露 | 🟡 中 | 日志/输出 | 自动正则屏蔽 |
| 暴力破解 | 🟡 中 | 登录接口 | 速率限制 |
| 供应链攻击 | 🟢 低 | 依赖包 | 最小依赖 + 锁定版本 |

### 7.2 认证流程

```
首次启动:
    generate-secrets.sh → .env 文件写入:
        SPARROW_SECRET_KEY=<random-32-bytes>
        SPARROW_ADMIN_TOKEN=<random-24-bytes>
    │
    ▼
管理员用 ADMIN_TOKEN 通过 Web UI 首次登录
    │
    ▼
Setup Wizard → 创建管理员账户 (username + password)
    │
    ▼
后续登录: username + password → JWT Token (24h 有效)
    │
    ▼
所有 API 请求携带: Authorization: Bearer <jwt>
```

### 7.3 RBAC 权限矩阵

```python
PERMISSIONS = {
    Role.ADMIN: {
        # 文件
        "files.read", "files.write", "files.delete",
        # 命令
        "shell.execute", "shell.execute_dangerous",
        # 任务
        "tasks.create", "tasks.approve", "tasks.cancel",
        # 管理
        "admin.config", "admin.users", "admin.backup",
        # 监控 & 审计
        "monitor.read", "audit.read", "audit.export",
    },
    Role.MEMBER: {
        "files.read", "files.write",
        "shell.execute",
        "tasks.create",
        "monitor.read",
    },
    Role.VIEWER: {
        "files.read",
        "monitor.read",
        "audit.read",
    },
}
```

### 7.4 审批引擎详细设计

```
操作风险分级:

┌─────────────────────────────────────────────────────┐
│  FORBIDDEN (永远阻止)                                │
│  rm -rf /、mkfs、fork bomb、dd if=/dev/zero          │
├─────────────────────────────────────────────────────┤
│  ADMIN_ONLY (需管理员审批)                            │
│  rm -rf、git push --force、pip install、             │
│  apt install、curl|bash                              │
├─────────────────────────────────────────────────────┤
│  CONFIRM (需用户确认)                                 │
│  file.write、shell.execute (一般命令)、               │
│  scheduler.add、scheduler.remove                    │
├─────────────────────────────────────────────────────┤
│  AUTO (自动执行)                                     │
│  file.list、file.read、file.search、                │
│  monitor.status、scheduler.list、notify.broadcast   │
└─────────────────────────────────────────────────────┘
```

### 7.5 路径沙盒实现

```python
class Sandbox:
    def validate_path(self, path: str) -> Path:
        """防止路径遍历攻击"""
        # 1. 展开用户目录 (~)
        # 2. 解析为绝对路径 (.resolve())
        # 3. 检查是否在 workspace_root 内

        if os.path.isabs(path):
            resolved = Path(path).resolve()
        else:
            resolved = (self.workspace_root / path).resolve()

        # 关键检查：resolved 必须是 workspace_root 的子路径
        try:
            resolved.relative_to(self.workspace_root)
        except ValueError:
            raise SandboxViolation(
                f"Access denied: '{path}' is outside workspace"
            )

        return resolved
```

这能防御：
- `../../etc/passwd` → 解析后在 workspace 外 → 拒绝
- `/etc/shadow` → 绝对路径不在 workspace 内 → 拒绝
- `./safe/../../etc/passwd` → resolve 后出界 → 拒绝
- 符号链接指向外部 → resolve 跟踪链接后出界 → 拒绝

---

## 8. LLM 适配层设计

### 8.1 抽象接口

```python
class BaseLLM(ABC):
    """LLM 供应商抽象层 — 所有供应商实现此接口"""

    @abstractmethod
    async def chat(
        self,
        messages: list[LLMMessage],
        tools: list[dict] | None = None,   # function calling 定义
        **kwargs,
    ) -> LLMResponse:
        """发送聊天请求，可选 function calling"""

    @abstractmethod
    async def health_check(self) -> bool:
        """检查 LLM 供应商是否可达"""
```

### 8.2 响应标准化

不同 LLM 的 function calling 响应格式不同，适配层负责统一：

```python
@dataclass
class LLMResponse:
    content: str                           # 文本回复
    model: str                             # 使用的模型名
    stop_reason: str                       # "end_turn" | "tool_use"
    tool_calls: list[ToolCall] | None     # 工具调用请求
    usage: dict                            # token 用量

@dataclass
class ToolCall:
    id: str                                # 唯一 ID（用于匹配 tool_result）
    name: str                              # 工具名
    params: dict                           # 参数
```

### 8.3 各供应商 Function Calling 差异

| 供应商 | Function Calling 格式 | 响应字段 |
|--------|---------------------|---------|
| **OpenAI** | `tools` 参数 + `tool_choice` | `choices[0].message.tool_calls` |
| **Anthropic** | `tools` 参数 | `content` 中的 `tool_use` block |
| **Ollama** | OpenAI 兼容格式（部分模型） | 同 OpenAI |

适配层的职责就是抹平这些差异，让 Orchestrator 只看到统一的 `LLMResponse`。

### 8.4 供应商选择策略

```python
def create_llm(config: SparrowConfig) -> BaseLLM:
    """根据配置创建合适的 LLM 实例"""
    match config.llm_provider:
        case "openai":
            return OpenAIAdapter(
                api_key=config.llm_api_key,
                model=config.llm_model or "gpt-4o",
                base_url=config.llm_base_url or "https://api.openai.com/v1",
            )
        case "anthropic":
            return AnthropicAdapter(
                api_key=config.llm_api_key,
                model=config.llm_model or "claude-sonnet-4-20250514",
            )
        case "ollama":
            return OllamaAdapter(
                model=config.llm_model or "llama3",
                base_url=config.llm_base_url or "http://localhost:11434",
            )
        case _:
            raise ValueError(f"Unknown LLM provider: {config.llm_provider}")
```

---

## 9. Web UI 设计

### 9.1 技术栈

| 层 | 选择 | 理由 |
|---|------|------|
| 框架 | Vue 3 + Composition API | 轻量、学习曲线低 |
| 构建 | Vite | 极速 HMR |
| 路由 | Vue Router 4 | SPA 路由 |
| 状态 | Pinia | 官方推荐、简单 |
| 样式 | 纯 CSS（无 UI 库） | 零依赖、暗色主题 |
| 通信 | WebSocket + fetch | 实时 + REST |

### 9.2 页面结构

```
/setup           → SetupWizard.vue    # 首次运行向导
/                → Chat.vue           # 主聊天界面（默认页）
/files           → Files.vue          # 文件浏览器
/tasks           → Tasks.vue          # 审批队列 & 任务历史
/dashboard       → Dashboard.vue      # 系统状态仪表盘
/settings        → Settings.vue       # 配置管理
```

### 9.3 实时通信设计

```
Web UI ←── WebSocket ──→ FastAPI

消息类型:
├── chat.message        # 用户发送消息
├── chat.response       # Agent 回复
├── chat.thinking       # Agent 思考中状态
├── chat.tool_use       # Agent 正在调用工具
├── chat.tool_result    # 工具执行结果
├── approval.request    # 新的审批请求
├── approval.resolved   # 审批结果
├── system.status       # 系统状态更新
└── agent.status        # Agent 连接状态变更
```

### 9.4 响应式设计

```css
/* 断点策略 */
@media (max-width: 768px) {
    /* 移动端：侧边栏折叠为图标，全宽内容区 */
    .sidebar { width: 60px; }
    .logo-text, .nav-label { display: none; }
}

@media (min-width: 769px) and (max-width: 1200px) {
    /* 平板：正常侧边栏，适中内容区 */
}

@media (min-width: 1201px) {
    /* 桌面：完整布局 */
}
```

---

## 10. 数据库设计

### 10.1 ER 关系图

```
┌──────────────┐     ┌──────────────────┐
│    users     │     │   audit_log      │
├──────────────┤     ├──────────────────┤
│ id (PK)      │──┐  │ id (PK)          │
│ username     │  │  │ timestamp        │
│ password_hash│  ├──│ user_id (FK)     │
│ role         │  │  │ action           │
│ is_active    │  │  │ target           │
│ created_at   │  │  │ parameters       │
└──────────────┘  │  │ result           │
                  │  │ details          │
                  │  │ channel          │
                  │  └──────────────────┘
                  │
                  │  ┌──────────────────┐
                  │  │approval_requests │
                  │  ├──────────────────┤
                  ├──│ requested_by (FK)│
                  │  │ id (PK)          │
                  │  │ skill_name       │
                  │  │ description      │
                  │  │ parameters       │
                  │  │ risk_level       │
                  │  │ status           │
                  ├──│ reviewed_by (FK) │
                  │  │ created_at       │
                  │  │ reviewed_at      │
                  │  └──────────────────┘
                  │
                  │  ┌──────────────────┐
                  │  │ scheduled_tasks  │
                  │  ├──────────────────┤
                  ├──│ created_by (FK)  │
                  │  │ id (PK)          │
                  │  │ name             │
                  │  │ cron_expr        │
                  │  │ command          │
                  │  │ is_active        │
                  │  │ created_at       │
                  │  │ last_run         │
                  │  └──────────────────┘
                  │
                  │  ┌──────────────────┐
                  │  │ conversations    │
                  │  ├──────────────────┤
                  └──│ user_id (FK)     │
                     │ id (PK, auto)    │
                     │ role             │
                     │ content          │
                     │ channel          │
                     │ created_at       │
                     └──────────────────┘
```

### 10.2 Repository 模式

所有 DB 操作通过 Repository 抽象层，不直接写 SQL：

```python
class BaseRepository:
    """数据访问抽象 — 为未来迁移 Postgres 预留接口"""

    def __init__(self, conn, table):
        self.conn = conn
        self.table = table

    async def find_by_id(self, id: str) -> dict | None: ...
    async def find_all(self, limit, offset) -> list[dict]: ...
    async def insert(self, data: dict) -> str: ...
    async def update(self, id: str, data: dict) -> bool: ...
    async def delete(self, id: str) -> bool: ...
```

迁移到 Postgres 时，只需替换 Repository 的实现，业务代码零改动。

---

## 11. 部署架构

### 11.1 Docker Compose（推荐）

```yaml
services:
  core:       # Control Plane
    build: ./sparrow-core
    ports: ["8080:8080", "8081:8081"]
    volumes: [sparrow-data:/app/data]

  agent:      # Local Agent
    build: ./sparrow-agent
    volumes: [~/sparrow-workspace:/workspace]
    depends_on: [core]

  web:        # Vue SPA (Nginx)
    build: ./sparrow-web
    ports: ["3000:3000"]
    depends_on: [core]
```

### 11.2 裸机部署

```bash
# 终端 1: Control Plane
pip install -e ./sparrow-core
sparrow-core

# 终端 2: Local Agent
pip install -e ./sparrow-agent
sparrow-agent --core-url ws://localhost:8081/ws/agent

# 终端 3: Web UI (开发模式)
cd sparrow-web && npm install && npm run dev
```

### 11.3 网络拓扑

```
互联网/内网
    │
    ▼
[Nginx/反向代理] (可选)
    │
    ├── :3000 → sparrow-web (Vue SPA)
    ├── :8080 → sparrow-core (REST API + WebSocket /ws/chat)
    └── :8081 → sparrow-core (Agent WebSocket /ws/agent)
                     ▲
                     │ 出站 WebSocket
                     │
              [sparrow-agent] (宿主机进程)
                     │
                     ▼
              [~/sparrow-workspace] (文件系统)
```

---

## 12. API 设计规范

### 12.1 REST API 端点

```
GET    /api/health                   # 基础健康检查
GET    /api/health/detailed          # 详细健康检查（含子系统状态）

POST   /api/auth/login               # 登录 → JWT
POST   /api/auth/refresh             # 刷新 token
GET    /api/auth/me                  # 当前用户信息

GET    /api/files?path=.             # 列出文件
GET    /api/files/read?path=x        # 读取文件
POST   /api/files/write              # 写入文件
POST   /api/files/upload             # 上传文件
GET    /api/files/download?path=x    # 下载文件
POST   /api/files/search             # 搜索文件

GET    /api/tasks/pending            # 待审批列表
POST   /api/tasks/{id}/approve       # 审批通过
POST   /api/tasks/{id}/reject        # 审批拒绝
GET    /api/tasks/history            # 任务历史

GET    /api/admin/config             # 获取配置（脱敏）
POST   /api/admin/setup              # 初始配置向导
GET    /api/admin/audit              # 审计日志
POST   /api/admin/backup             # 创建备份
GET    /api/admin/users              # 用户列表
POST   /api/admin/users              # 创建用户

WS     /ws/chat                      # Web UI 聊天
WS     /ws/agent                     # Agent 连接
```

### 12.2 WebSocket 消息格式

```typescript
// 客户端 → 服务端
interface ClientMessage {
  type: "chat.message" | "approval.response"
  content?: string
  task_id?: string
  action?: "approve" | "reject"
}

// 服务端 → 客户端
interface ServerMessage {
  type: "chat.response" | "chat.thinking" | "chat.tool_use"
      | "chat.tool_result" | "approval.request" | "system.status"
  content?: string
  tool_name?: string
  tool_params?: Record<string, any>
  task?: ApprovalRequest
  status?: SystemHealth
}
```

---

## 13. 开发规范与流程

### 13.1 技术规范

| 项目 | 规范 |
|------|------|
| Python | 3.11+, type hints 必须, asyncio 优先 |
| 格式化 | Ruff (formatter + linter) |
| 测试 | pytest + pytest-asyncio |
| 前端 | TypeScript strict mode, Vue 3 Composition API |
| Git | Conventional Commits (`feat:`, `fix:`, `docs:`) |
| 分支 | `main` (stable), `dev` (开发), `feat/*` (功能) |

### 13.2 代码组织原则

```
每个模块遵循:
├── __init__.py     # 公开接口
├── models.py       # Pydantic 数据模型
├── service.py      # 业务逻辑（无 IO）
├── repository.py   # 数据访问（有 IO）
└── router.py       # API 路由（仅在 api/ 目录）
```

### 13.3 错误处理策略

```python
# 统一错误响应格式
{
    "error": {
        "code": "SANDBOX_VIOLATION",
        "message": "Access denied: path is outside workspace",
        "details": {"path": "../../etc/passwd", "workspace": "/home/user/sparrow-workspace"}
    }
}
```

### 13.4 日志规范

```python
import logging

logger = logging.getLogger("sparrow.module_name")

# 级别使用:
logger.debug("Internal state: %s", state)        # 调试细节
logger.info("User %s connected via %s", uid, ch)  # 正常操作
logger.warning("Rate limit exceeded for %s", uid)  # 需关注但不影响
logger.error("LLM request failed: %s", err)        # 错误但可恢复
logger.critical("Database corruption detected")     # 致命错误
```

---

## 14. 分阶段实施计划

### Phase 1: 项目骨架 ✅ (已完成)

- [x] Monorepo 目录结构
- [x] sparrow-core FastAPI 骨架
- [x] sparrow-agent 进程骨架
- [x] sparrow-web Vue 3 SPA 骨架
- [x] Docker Compose 编排
- [x] 文档框架

### Phase 2: 打通核心通路

**目标：** 一条消息从 Web UI 到 Agent 执行再返回的完整路径

```
Web UI → WebSocket → Orchestrator → LLM → tool_use
→ WebSocket → Agent → 执行 → result → LLM → 回复 → Web UI
```

**具体任务：**

- [ ] sparrow-core: 实现 Agent WebSocket 服务端 (`/ws/agent`)
- [ ] sparrow-agent: 实现 WebSocket 客户端的完整消息处理
- [ ] sparrow-core: 集成 Ollama/OpenAI 的 function calling
- [ ] sparrow-core: 实现 Orchestrator 的 agentic loop（带 tool calling）
- [ ] sparrow-core: 将 Chat WebSocket 对接到 Orchestrator
- [ ] sparrow-web: Chat 页面对接真实 WebSocket
- [ ] 端到端测试：发送 "list files" → 收到真实文件列表

### Phase 3: 安全基座

**目标：** 所有操作有认证、授权、审批、审计

- [ ] 实现 JWT 登录 + 自动密钥生成
- [ ] RBAC 中间件集成到所有 API
- [ ] 审批引擎持久化到 SQLite
- [ ] 审计日志持久化到 SQLite
- [ ] 命令风险分级在执行层生效
- [ ] Rate Limiting 中间件
- [ ] sparrow-web: 登录页面 + token 管理

### Phase 4: Web UI 完善

**目标：** 所有页面功能可用

- [ ] Chat: 流式响应、tool_use 可视化、Markdown 渲染
- [ ] Files: 对接真实 API、文件预览、上传/下载
- [ ] Tasks: 实时审批推送（WebSocket）、历史查询
- [ ] Dashboard: 系统指标实时更新、健康检查
- [ ] Settings: 保存配置到 DB、LLM 连接测试
- [ ] Setup Wizard: 对接 /api/admin/setup

### Phase 5: Telegram 渠道

**目标：** 通过 Telegram 完成完整的工作流

- [ ] 实现 TelegramAdapter (python-telegram-bot)
- [ ] Telegram → UnifiedMessage 转换
- [ ] UnifiedResponse → Telegram 消息
- [ ] 审批请求: Inline Keyboard 确认/拒绝
- [ ] 文件发送: 通过 Telegram Document
- [ ] Web UI 配置: 粘贴 Bot Token 即可启用

### Phase 6: 打磨发布 v0.1.0

**目标：** 生产可用的最小版本

- [ ] Docker Compose 生产配置优化
- [ ] GitHub Actions CI/CD (lint → test → build → push)
- [ ] PyPI 发包: `opensparrow-core`, `opensparrow-agent`
- [ ] Docker Hub 镜像发布
- [ ] 快速上手文档 + GIF 演示
- [ ] SPARROW.md 自定义指令支持
- [ ] 备份/恢复功能

---

## 15. 附录：关键数据结构

### A. 完整的 Agentic Loop 消息流

```json
// Turn 1: 用户消息
{"role": "user", "content": "帮我看看 src 目录下有什么文件"}

// Turn 2: LLM 回复 (tool_use)
{
  "role": "assistant",
  "content": null,
  "stop_reason": "tool_use",
  "tool_calls": [{
    "id": "call_001",
    "name": "file.list",
    "params": {"path": "src"}
  }]
}

// Turn 3: 工具结果
{
  "role": "tool_result",
  "tool_use_id": "call_001",
  "content": "{\"path\":\"src\",\"entries\":[{\"name\":\"main.py\",\"is_dir\":false,\"size\":2048},{\"name\":\"utils/\",\"is_dir\":true}]}"
}

// Turn 4: LLM 最终回复
{
  "role": "assistant",
  "content": "📂 `src/` 目录下有:\n\n| 名称 | 类型 | 大小 |\n|------|------|------|\n| main.py | 文件 | 2.0 KB |\n| utils/ | 目录 | — |\n\n需要我查看某个文件的内容吗？",
  "stop_reason": "end_turn"
}
```

### B. 审批请求数据结构

```json
{
  "id": "apr_7f3a8b",
  "skill_name": "shell.execute",
  "description": "Execute: git pull origin main",
  "parameters": {"command": "git pull origin main"},
  "risk_level": "confirm",
  "requested_by": "alice",
  "status": "pending",
  "created_at": "2026-04-28T10:30:00Z",
  "reviewed_by": null,
  "reviewed_at": null
}
```

### C. 审计日志条目

```json
{
  "id": "aud_9c2e4d",
  "timestamp": "2026-04-28T10:30:05Z",
  "user_id": "alice",
  "action": "shell.execute",
  "target": "git pull origin main",
  "parameters": {"command": "git pull origin main", "timeout": 30},
  "result": "success",
  "details": "return_code=0, stdout_lines=3",
  "channel": "telegram"
}
```

### D. Agent 注册消息

```json
{
  "type": "agent.register",
  "agent_version": "0.1.0",
  "workspace": "/home/user/sparrow-workspace",
  "hostname": "dev-server-01",
  "platform": "Linux 6.1.0",
  "capabilities": ["file_ops", "shell", "monitor"],
  "python_version": "3.11.9"
}
```

### E. 系统健康检查响应

```json
{
  "status": "ok",
  "version": "0.1.0",
  "subsystems": {
    "database": {"status": "ok", "type": "sqlite", "size_mb": 2.4},
    "llm": {"status": "ok", "provider": "ollama", "model": "llama3", "latency_ms": 230},
    "agent": {"status": "connected", "hostname": "dev-server-01", "uptime_hours": 48.5},
    "telegram": {"status": "ok", "bot_username": "myteam_sparrow_bot", "pending_updates": 0},
    "scheduler": {"status": "ok", "active_tasks": 3, "next_run": "2026-04-28T11:00:00Z"}
  }
}
```

---

## 版权与许可

OpenSparrow 采用 [MIT 许可证](../LICENSE)。

本文档中引用的 Claude Code、OpenClaw 等产品架构信息均来自公开文档和技术文章，仅用于技术分析和借鉴。
