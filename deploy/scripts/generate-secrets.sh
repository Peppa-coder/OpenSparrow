#!/usr/bin/env bash
# Generate secure tokens for OpenSparrow
# Creates .env file with random secrets if it doesn't exist

set -euo pipefail

ENV_FILE="${1:-.env}"

if [ -f "$ENV_FILE" ]; then
    echo "⚠️  $ENV_FILE already exists. Skipping secret generation."
    exit 0
fi

SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
ADMIN_TOKEN=$(python3 -c "import secrets; print(secrets.token_urlsafe(24))")

cat > "$ENV_FILE" <<EOF
# OpenSparrow — Auto-generated configuration
# Generated on: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

SPARROW_SECRET_KEY=${SECRET_KEY}
SPARROW_ADMIN_TOKEN=${ADMIN_TOKEN}
SPARROW_LLM_PROVIDER=ollama
SPARROW_LLM_MODEL=llama3
SPARROW_LLM_BASE_URL=http://localhost:11434
EOF

echo "✅ Generated $ENV_FILE with secure tokens"
echo "   Admin token: ${ADMIN_TOKEN:0:8}..."
