# 🚀 Quick Start — 5 Minutes to Running

## Option 1: Docker Compose (Easiest)

**Prerequisites**: Docker & Docker Compose installed.

```bash
# 1. Clone the repo
git clone https://github.com/Peppa-coder/OpenSparrow.git
cd OpenSparrow

# 2. Launch everything
docker compose up -d

# 3. Open in browser
open http://localhost:3000
```

That's it! The setup wizard will guide you through configuration.

## Option 2: Bare Metal

**Prerequisites**: Python 3.11+, Node.js 20+ (for frontend)

```bash
# 1. Clone
git clone https://github.com/Peppa-coder/OpenSparrow.git
cd OpenSparrow

# 2. Install control plane
cd sparrow-core
pip install -e ".[dev]"
cd ..

# 3. Install local agent
cd sparrow-agent
pip install -e ".[dev]"
cd ..

# 4. Generate secrets
bash deploy/scripts/generate-secrets.sh

# 5. Start control plane (Terminal 1)
sparrow-core

# 6. Start local agent (Terminal 2)
sparrow-agent

# 7. Start web UI in dev mode (Terminal 3)
cd sparrow-web && npm install && npm run dev
```

Open **http://localhost:3000** and follow the setup wizard.

## First-Time Setup

1. **Choose LLM Provider** — Ollama (local/free) or OpenAI/Anthropic (cloud)
2. **Set Workspace** — Default: `~/sparrow-workspace`
3. **Configure Channels** — Optional: add Telegram bot token
4. **Done!** — Start chatting with your agent

## Verifying Installation

```bash
# Check control plane health
curl http://localhost:8080/api/health

# Expected response:
# {"status":"ok","version":"0.1.0","service":"opensparrow-core"}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Port 8080 in use | Set `SPARROW_PORT=9090` in `.env` |
| Ollama not found | Install: `curl -fsSL https://ollama.ai/install.sh \| sh` |
| Permission denied | Ensure workspace dir is writable |

## Next Steps

- Read the [Architecture Guide](architecture.md)
- Configure [Telegram Bot](channel-setup/telegram.md)
- Review [Security Model](security.md)
