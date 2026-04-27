#!/usr/bin/env bash
# OpenSparrow — Bare-metal setup script
# Usage: curl -fsSL https://raw.githubusercontent.com/Peppa-coder/OpenSparrow/main/deploy/scripts/setup.sh | bash

set -euo pipefail

BOLD='\033[1m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BOLD}🐦 OpenSparrow Setup${NC}"
echo "================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3.11+ is required. Please install it first."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo -e "✅ Python ${PYTHON_VERSION} detected"

# Check pip
if ! command -v pip3 &>/dev/null; then
    echo "❌ pip3 is required. Please install it first."
    exit 1
fi

# Create workspace
WORKSPACE="${SPARROW_WORKSPACE:-$HOME/sparrow-workspace}"
mkdir -p "$WORKSPACE"
echo -e "✅ Workspace: ${BLUE}${WORKSPACE}${NC}"

# Install packages
echo ""
echo "📦 Installing OpenSparrow..."
pip3 install opensparrow-core opensparrow-agent 2>/dev/null || {
    echo "⚠️  PyPI packages not published yet. Installing from source..."
    if [ -d "sparrow-core" ]; then
        pip3 install -e ./sparrow-core
        pip3 install -e ./sparrow-agent
    else
        echo "❌ Please run this script from the OpenSparrow repository root."
        exit 1
    fi
}

# Generate secrets
echo ""
echo "🔐 Generating security tokens..."
bash "$(dirname "$0")/generate-secrets.sh"

echo ""
echo -e "${GREEN}${BOLD}🎉 OpenSparrow is installed!${NC}"
echo ""
echo "Start the control plane:"
echo "  sparrow-core"
echo ""
echo "Start the local agent (in another terminal):"
echo "  sparrow-agent"
echo ""
echo "Then open http://localhost:8080 in your browser."
