#!/bin/bash
# --- Dice Dungeon Launcher ---

# Get script directory
DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$DIR"

# Pick a terminal
if command -v kitty &>/dev/null; then
    TERM_CMD=(kitty python3 Main.py)
elif command -v konsole &>/dev/null; then
    TERM_CMD=(konsole -e python3 Main.py)
elif command -v gnome-terminal &>/dev/null; then
    TERM_CMD=(gnome-terminal -- bash -c "python3 '$DIR/Main.py'")
elif command -v xterm &>/dev/null; then
    TERM_CMD=(xterm -e python3 Main.py)
else
    echo "No supported terminal found. Running directly..."
    python3 Main.py
    exit 0
fi

# Check if we're already inside a terminal
if [ -t 1 ]; then
    python3 Main.py
else
    "${TERM_CMD[@]}"
fi
