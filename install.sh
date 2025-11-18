#!/usr/bin/env bash

set -e

echo "=== Software Testing Agent Installer ==="

# --- Clone Repository ---
echo "[1/6] Cloning repository..."
if ! command -v git >/dev/null 2>&1; then
    echo "Git not found. Please install Git first."
    exit 1
fi

git clone https://github.com/cazaresb/Software_Testing_Agent
cd Software_Testing_Agent

# --- Ensure VSCode Installed (Required for MCP Integration) ---
echo "[2/6] Checking for VSCode..."
if ! command -v code >/dev/null 2>&1; then
    echo "VSCode is required for the agent's CoPilot integration."
    echo "Please install VSCode and rerun this script."
    exit 1
fi

# --- Verify Python ---
echo "[3/6] Checking Python..."
if ! command -v python >/dev/null 2>&1; then
    echo "Python is not installed. Please install Python 3.8+."
    exit 1
fi

# --- Install Python Dependencies ---
echo "[4/6] Installing Python packages..."
python -m pip install --upgrade pip
python -m pip install fastmcp langchain javalang

# --- Provide Maven / Java Requirements Notice ---
echo "[5/6] Ensuring Java/Maven environment..."
if ! command -v mvn >/dev/null 2>&1; then
    echo "Maven not found. Please install Apache Maven for full functionality."
else
    echo "Maven detected."
fi

if ! command -v java >/dev/null 2>&1; then
    echo "Java not found. Please install JDK 17+."
else
    echo "Java detected."
fi

# --- Completion Notice ---
echo "[6/6] Installation complete!"
echo
echo "Next steps:"
echo "1. Open VSCode inside this directory:"
echo "      code ."
echo "2. Copy the MCP prompt from:"
echo "      .github/prompts/tester.prompt.md"
echo "   into your CoPilot Chat memory."
echo "3. (Recommended) Insert your Java codebase into:"
echo "      Software_Testing_Agent/codebase/"
echo "4. Run the agent server:"
echo "      python server.py"
echo
echo "You are now ready to use the Software Testing Agent!"
