# 🏗 Architecture Guide

## Overview

OpenSparrow uses a **dual-process architecture** that separates the control plane from the execution environment for security and flexibility.

```
┌─────────────────────────────────────────────────────┐
│                   User Interface                     │
│  ┌──────┐  ┌──────────┐  ┌───────┐  ┌───────────┐  │
│  │Web UI│  │Telegram   │  │Slack  │  │Webhook API│  │
│  │(Vue3)│  │Bot Adapter│  │Adapter│  │(Generic)  │  │
│  └──┬───┘  └─────┬─────┘  └──┬────┘  └─────┬─────┘  │
│     └────────────┴───────────┴──────────────┘        │
│                      │                               │
│         Unified Message Protocol (UMP)               │
│                      │                               │
├──────────────────────┼───────────────────────────────┤
│              Control Plane                           │
│  ┌─────────────────────────────────────────┐        │
│  │  Auth/RBAC  │  Task Router  │  LLM      │        │
│  │  Approval   │  Skills       │  Audit    │        │
│  │  Scheduler  │  Memory       │  SQLite   │        │
│  └─────────────────────────────────────────┘        │
│                      │                               │
│            WebSocket (outbound from agent)            │
│                      │                               │
├──────────────────────┼───────────────────────────────┤
│              Local Agent                             │
│  ┌─────────────────────────────────────────┐        │
│  │  File Manager  │  Shell Executor  │ Monitor │    │
│  │        (all sandboxed to workspace_root)    │    │
│  └─────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
```

## Components

### Control Plane (`sparrow-core`)

The brain of the system. Runs as a FastAPI application.

| Module | Purpose |
|--------|---------|
| `auth/` | JWT tokens, RBAC (admin/member/viewer) |
| `llm/` | Model-agnostic LLM interface (OpenAI, Anthropic, Ollama) |
| `gateway/` | Unified message protocol, channel adapters |
| `skills/` | Skill registry and built-in skills |
| `approval/` | Approval workflow engine, risk classification |
| `audit/` | Audit logging with secret redaction |
| `agent/` | Orchestrator (intent → plan → execute), conversation memory |
| `db/` | SQLite with repository pattern (Postgres-ready) |
| `api/` | REST + WebSocket endpoints |

### Local Agent (`sparrow-agent`)

The hands of the system. Runs on the work machine.

| Module | Purpose |
|--------|---------|
| `connector.py` | Outbound WebSocket to control plane, auto-reconnect |
| `sandbox.py` | Path validation, command safety checks |
| `file_manager.py` | Browse, read, write, search files |
| `executor.py` | Shell command execution with timeout |
| `monitor.py` | CPU, memory, disk metrics via psutil |

### Web UI (`sparrow-web`)

Vue 3 SPA with dark theme.

| View | Purpose |
|------|---------|
| `SetupWizard` | First-run configuration |
| `Chat` | Real-time chat with the agent |
| `Files` | Visual file browser |
| `Tasks` | Approval queue and task history |
| `Dashboard` | System health and stats |
| `Settings` | Configuration management |

## Key Design Decisions

### 1. Dual Process (not single container)

The agent connects **outbound** to the control plane. This means:
- No ports exposed on the work machine
- Control plane can run in a container safely
- Agent has direct access to the host filesystem (sandboxed)
- Clear security boundary between web-facing and execution layers

### 2. Approval-First Interaction

Unlike fully autonomous agents, OpenSparrow defaults to a **propose → approve → execute** flow:
- Low-risk operations (file read, status check) execute automatically
- Medium-risk operations require user confirmation
- High-risk operations require admin approval
- Some operations are forbidden entirely

### 3. Unified Message Protocol

All channels (Web, Telegram, Slack, Webhook) translate to a common `UnifiedMessage` format. Each adapter declares its capabilities — we don't pretend all channels are equal.

### 4. SQLite with Repository Pattern

SQLite is zero-config and perfect for small teams. But all DB access goes through a `BaseRepository` abstraction, making a future Postgres migration straightforward.

## Data Flow

```
User sends "list files in /docs"
    ↓
Channel Adapter → UnifiedMessage
    ↓
Message Router → Agent Orchestrator
    ↓
Orchestrator → LLM (intent: file.list, path: /docs)
    ↓
Approval Engine → Risk: AUTO (no approval needed)
    ↓
Skill Handler → WebSocket → Local Agent
    ↓
File Manager → sandbox.validate_path("/docs") → list directory
    ↓
Result → WebSocket → Orchestrator → Channel Adapter → User
    ↓
Audit Logger records the operation
```
