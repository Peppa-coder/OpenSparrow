# Telegram Bot Setup Guide

## Step 1: Create a Bot

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Choose a name (e.g., "My Team Sparrow")
4. Choose a username (e.g., `myteam_sparrow_bot`)
5. Copy the **bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## Step 2: Configure OpenSparrow

### Via Web UI
1. Go to **Settings** → **Telegram Bot**
2. Paste your bot token
3. Click **Save**

### Via Environment Variable
```bash
SPARROW_TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```

### Via .env File
Add to your `.env`:
```
SPARROW_TELEGRAM_BOT_TOKEN=your-token-here
SPARROW_TELEGRAM_ALLOWED_USERS=alice,bob
```

## Step 3: Restrict Access (Recommended)

Limit which Telegram users can interact with the bot:

```bash
SPARROW_TELEGRAM_ALLOWED_USERS=alice_username,bob_username
```

If empty, **all users** can interact with the bot — not recommended for production.

## Step 4: Test

1. Open your bot in Telegram
2. Send `/start`
3. Try: "Show system status"

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Initialize the bot |
| `/status` | System health check |
| `/files` | List workspace files |
| `/help` | Show available commands |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot doesn't respond | Check token and that sparrow-core is running |
| "Unauthorized" | Add your username to `SPARROW_TELEGRAM_ALLOWED_USERS` |
| Slow responses | Check LLM provider connectivity |
