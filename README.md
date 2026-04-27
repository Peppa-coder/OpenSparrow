<div align="center">

# 🐦 OpenSparrow

**麻雀虽小，五脏俱全** — Small as a sparrow, yet complete with all organs.

*Lightweight, all-in-one AI agent for small teams.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D.svg)](https://vuejs.org)

[Quick Start](#-quick-start) · [Features](#-features) · [Architecture](#-architecture) · [Docs](docs/)

</div>

---

## What is OpenSparrow?

OpenSparrow is a **self-hosted AI agent** that lets your small team control a work machine through a **Web UI** or **chat apps** (Telegram, Slack, etc.) — with built-in security, approval workflows, and LLM-powered intelligence.

Think of it as your team's private JARVIS: manage files, run commands, monitor systems, and automate tasks — all from your browser or phone.

```
🧑 "Deploy the latest build"  →  🐦 Agent proposes plan  →  👍 You approve  →  ✅ Done
```

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **Chat Interface** | Talk to your agent via Web UI or Telegram |
| 📁 **File Manager** | Browse, read, write, search files in workspace |
| ⚡ **Shell Execution** | Run commands with approval gates & audit trail |
| 📊 **System Monitor** | Real-time CPU, memory, disk stats |
| 🤖 **LLM Powered** | OpenAI, Anthropic, or Ollama (local/free) |
| 🔐 **Secure by Default** | RBAC, approval workflow, path sandbox, audit log |
| ⏰ **Task Scheduler** | Cron-like recurring tasks |
| 📱 **Mobile Ready** | Responsive web UI works on any device |
| 🐳 **One-Click Deploy** | `docker compose up` and you're live |

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
git clone https://github.com/Peppa-coder/OpenSparrow.git
cd OpenSparrow
docker compose up -d
```

Open **http://localhost:3000** → follow the setup wizard 🎉

### Option 2: Bare Metal

```bash
# Install control plane
cd sparrow-core && pip install -e .

# Install local agent
cd ../sparrow-agent && pip install -e .

# Start (in separate terminals)
sparrow-core    # Control plane at :8080
sparrow-agent   # Local agent connects automatically
```

### Option 3: One-Line Install

```bash
curl -fsSL https://raw.githubusercontent.com/Peppa-coder/OpenSparrow/main/deploy/scripts/setup.sh | bash
```

## 🏗 Architecture

OpenSparrow uses a **dual-process architecture** for security:

```
┌─────────────────────────────────────┐
│          User Interface             │
│   Web UI  │  Telegram  │  Webhook   │
├─────────────────────────────────────┤
│        Control Plane (Core)         │
│  Auth │ LLM │ Skills │ Approval    │
│  Audit │ Scheduler │ Gateway       │
├──────────── WebSocket ──────────────┤
│         Local Agent                 │
│  File Manager │ Shell │ Monitor    │
│       (sandboxed workspace)         │
└─────────────────────────────────────┘
```

- **Control Plane** (`sparrow-core`): FastAPI backend handling auth, LLM, messaging, and orchestration
- **Local Agent** (`sparrow-agent`): Runs on the work machine, executes file/shell/monitor tasks in a sandbox
- **Web UI** (`sparrow-web`): Vue 3 SPA with chat, file browser, dashboard, and setup wizard

The agent connects **outbound** to the control plane via WebSocket — no ports exposed on the work machine.

## 🔐 Security Model

OpenSparrow treats security as a first-class citizen:

- **Approval Workflow**: Risky operations require human confirmation
- **Path Sandbox**: File access limited to `~/sparrow-workspace`
- **Command Safety**: Dangerous commands blocked or require admin approval
- **RBAC**: Three roles — Admin, Member, Viewer
- **Audit Trail**: Every operation is logged with secret redaction
- **Auto-generated Secrets**: Secure tokens created on first run

## 🤖 Supported LLM Providers

| Provider | Type | Setup |
|----------|------|-------|
| **Ollama** | Local, free | `ollama serve` → ready |
| **OpenAI** | Cloud | Paste API key |
| **Anthropic** | Cloud | Paste API key |

## 📁 Project Structure

```
OpenSparrow/
├── sparrow-core/       # Control Plane (Python/FastAPI)
├── sparrow-agent/      # Local Agent (Python)
├── sparrow-web/        # Web UI (Vue 3/Vite)
├── deploy/             # Docker & deployment configs
├── docs/               # Documentation
├── docker-compose.yml  # One-click launch
└── Makefile            # Dev shortcuts
```

## 🛠 Development

```bash
# Show all available commands
make help

# Run each component in dev mode
make dev-core    # FastAPI with hot-reload
make dev-agent   # Local agent
make dev-web     # Vite dev server

# Testing
make test        # Run all tests
make lint        # Run linters
```

## 📋 Roadmap

### V1 — MVP ✨
- [x] Project skeleton & architecture
- [ ] Auth & security subsystem
- [ ] Core skills (files, shell, monitor)
- [ ] LLM integration (OpenAI + Ollama)
- [ ] Agent orchestrator
- [ ] Web UI (chat, files, dashboard)
- [ ] Telegram bot adapter
- [ ] Docker deployment

### V2 — Extended
- [ ] Slack & DingTalk/Feishu adapters
- [ ] Git operations
- [ ] Lightweight RAG over local docs
- [ ] Command recipes / presets

### V3 — Advanced
- [ ] Plugin system
- [ ] Multi-machine management
- [ ] Web scraping & doc conversion
- [ ] PostgreSQL upgrade path

## 🤝 Contributing

Contributions welcome! Please read the [architecture docs](docs/architecture.md) first.

## 📄 License

[MIT](LICENSE) — use it however you like.

---

<div align="center">

**🐦 OpenSparrow** — *Your team's pocket-sized AI agent.*

*麻雀虽小，五脏俱全*

</div>
