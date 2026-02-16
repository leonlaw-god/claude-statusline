#!/bin/bash
# Claude Statusline Installer for Linux/macOS
# Usage: curl -sL https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main/install.sh | bash

set -e

REPO_URL="https://raw.githubusercontent.com/leonlaw-god/claude-statusline/main"
CLAUDE_DIR="$HOME/.claude"
SCRIPT_NAME="statusline-enhanced.py"

echo "🔧 Installing Claude Statusline..."

# Create .claude directory if not exists
mkdir -p "$CLAUDE_DIR"

# Download the script
echo "📥 Downloading statusline script..."
curl -sL "$REPO_URL/$SCRIPT_NAME" -o "$CLAUDE_DIR/$SCRIPT_NAME"
chmod +x "$CLAUDE_DIR/$SCRIPT_NAME"

# Update settings.json
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
echo "📝 Updating settings.json..."

if [ -f "$SETTINGS_FILE" ]; then
    # Check if statusLine already exists
    if grep -q '"statusLine"' "$SETTINGS_FILE"; then
        # Update existing statusLine
        if command -v python3 &> /dev/null; then
            sed -i.bak 's|"command":.*|"command": "python3 '"$CLAUDE_DIR"'/'"$SCRIPT_NAME"'"|' "$SETTINGS_FILE"
        else
            sed -i.bak 's|"command":.*|"command": "python '"$CLAUDE_DIR"'/'"$SCRIPT_NAME"'"|' "$SETTINGS_FILE"
        fi
        echo "✅ Updated existing statusLine configuration"
    else
        # Add statusLine before the last }
        if command -v python3 &> /dev/null; then
            sed -i.bak 's|^}|  "statusLine": {\n    "type": "command",\n    "command": "python3 '"$CLAUDE_DIR"'/'"$SCRIPT_NAME"'\n  }\n}|' "$SETTINGS_FILE"
        else
            sed -i.bak 's|^}|  "statusLine": {\n    "type": "command",\n    "command": "python '"$CLAUDE_DIR"'/'"$SCRIPT_NAME"'\n  }\n}|' "$SETTINGS_FILE"
        fi
        echo "✅ Added statusLine configuration"
    fi
else
    # Create new settings.json
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
    cat > "$SETTINGS_FILE" << EOF
{
  "statusLine": {
    "type": "command",
    "command": "$PYTHON_CMD $CLAUDE_DIR/$SCRIPT_NAME"
  }
}
EOF
    echo "✅ Created new settings.json"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Restart Claude Code to see the new statusline."
echo ""
echo "Features:"
echo "  • Model name display"
echo "  • Token usage (Tok/Out)"
echo "  • Cost tracking (\$)"
echo "  • Context usage percentage (Ctx)"
echo "  • Git status (branch, changes, conflicts)"
echo "  • Full directory path"
