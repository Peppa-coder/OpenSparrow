# Slack App Setup Guide

> ⚠️ Slack integration is planned for **V2**. This guide is a preview.

## Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From scratch**
3. Name it "OpenSparrow" and select your workspace
4. Under **OAuth & Permissions**, add scopes:
   - `chat:write`
   - `commands`
   - `files:read`
   - `files:write`
   - `im:history`
   - `im:read`
   - `im:write`
5. Install to workspace and copy the **Bot User OAuth Token**

## Step 2: Configure OpenSparrow

```bash
SPARROW_SLACK_BOT_TOKEN=xoxb-your-token
SPARROW_SLACK_SIGNING_SECRET=your-signing-secret
```

## Step 3: Set Up Event Subscriptions

1. In Slack App settings → **Event Subscriptions**
2. Request URL: `https://your-sparrow-server/api/gateway/slack/events`
3. Subscribe to:
   - `message.im`
   - `app_mention`

## Coming Soon

Full Slack integration with:
- Slash commands (`/sparrow status`)
- Interactive messages with approval buttons
- File upload/download
- Thread support
