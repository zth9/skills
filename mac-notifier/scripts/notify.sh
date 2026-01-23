#!/bin/bash
# Mac Notifier for Claude Code
# Sends native macOS notifications when Claude Code events occur

# Default values
TITLE="Claude Code"
MESSAGE=""
SOUND="Glass"
SUBTITLE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--title)
            TITLE="$2"
            shift 2
            ;;
        -m|--message)
            MESSAGE="$2"
            shift 2
            ;;
        -s|--sound)
            SOUND="$2"
            shift 2
            ;;
        --subtitle)
            SUBTITLE="$2"
            shift 2
            ;;
        --no-sound)
            SOUND=""
            shift
            ;;
        -h|--help)
            echo "Usage: notify.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -t, --title     Notification title (default: 'Claude Code')"
            echo "  -m, --message   Notification message (required)"
            echo "  -s, --sound     Sound name (default: 'Glass')"
            echo "  --subtitle      Notification subtitle"
            echo "  --no-sound      Disable sound"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Available sounds: Basso, Blow, Bottle, Frog, Funk, Glass, Hero,"
            echo "                  Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink"
            exit 0
            ;;
        *)
            # If no flag, treat as message
            if [[ -z "$MESSAGE" ]]; then
                MESSAGE="$1"
            fi
            shift
            ;;
    esac
done

# Read from stdin if message is empty (for hook integration)
if [[ -z "$MESSAGE" ]]; then
    # Try to read JSON from stdin and extract useful info
    if read -t 0.1 stdin_data; then
        # Just use a default message since we got hook data
        MESSAGE="Task completed"
    fi
fi

# Validate message
if [[ -z "$MESSAGE" ]]; then
    MESSAGE="Notification"
fi

# Build AppleScript command
SCRIPT="display notification \"$MESSAGE\" with title \"$TITLE\""

if [[ -n "$SUBTITLE" ]]; then
    SCRIPT="$SCRIPT subtitle \"$SUBTITLE\""
fi

if [[ -n "$SOUND" ]]; then
    SCRIPT="$SCRIPT sound name \"$SOUND\""
fi

# Execute notification
osascript -e "$SCRIPT"
