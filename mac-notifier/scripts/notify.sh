#!/bin/bash
# Mac Notifier for Claude Code
# Sends native macOS notifications when Claude Code events occur
# Supports i18n (zh/en) and directory info display

# Get script directory for ClaudeNotifier.app path
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_NOTIFIER="${SCRIPT_DIR}/../ClaudeNotifier.app/Contents/MacOS/ClaudeNotifier"

# ============================================================
# i18n: Message translations (bash 3.x compatible)
# ============================================================

# Detect locale from $LANG or parameter
# Priority: parameter > $LANG > default (en)
detect_locale() {
    local locale="${1:-}"
    if [[ -n "$locale" ]]; then
        # Validate input
        if [[ "$locale" == "zh" || "$locale" == "en" ]]; then
            echo "$locale"
            return
        fi
    fi
    # Auto-detect from $LANG
    if [[ "${LANG:-}" =~ ^zh ]]; then
        echo "zh"
    else
        echo "en"
    fi
}

# Translate message key to localized string
translate_message() {
    local key="$1"
    local locale="$2"

    case "${key}:${locale}" in
        "task_completed:zh") echo "任务已完成" ;;
        "task_completed:en") echo "Task completed" ;;
        "permission_needed:zh") echo "需要权限确认" ;;
        "permission_needed:en") echo "Permission needed" ;;
        "input_needed:zh") echo "MCP 工具需要输入" ;;
        "input_needed:en") echo "Input needed for MCP tool" ;;
        *) echo "$key" ;;
    esac
}

# Get directory info based on format
# Only use explicitly provided directory (from stdin JSON, env var, or --project-dir)
# Does NOT fallback to Git root or PWD to avoid showing wrong directory
get_directory_info() {
    local format="${1:-none}"
    local dir_info=""

    case "$format" in
        short|full)
            # First try directory from stdin JSON (session_cwd) - set by Claude Code
            if [[ -n "${STDIN_PROJECT_DIR:-}" && "$STDIN_PROJECT_DIR" != "/" && "$STDIN_PROJECT_DIR" != "$HOME" ]]; then
                if [[ "$format" == "short" ]]; then
                    dir_info=$(basename "$STDIN_PROJECT_DIR")
                else
                    dir_info="$STDIN_PROJECT_DIR"
                fi
            # Then try CLAUDE_PROJECT_DIR env var - set by Claude Code
            elif [[ -n "${CLAUDE_PROJECT_DIR:-}" && "$CLAUDE_PROJECT_DIR" != "/" && "$CLAUDE_PROJECT_DIR" != "$HOME" ]]; then
                if [[ "$format" == "short" ]]; then
                    dir_info=$(basename "$CLAUDE_PROJECT_DIR")
                else
                    dir_info="$CLAUDE_PROJECT_DIR"
                fi
            fi
            # No fallback to Git root or PWD - would show wrong directory in hook context
            ;;
        none|"")
            dir_info=""
            ;;
    esac

    echo "$dir_info"
}

# ============================================================
# Default values
# ============================================================
TITLE="Claude Code"
MESSAGE=""
SOUND="Glass"
SUBTITLE=""
USE_OSASCRIPT=""
LOCALE=""
DIRECTORY_FORMAT="none"
MESSAGE_KEY=""
STDIN_PROJECT_DIR=""

# Check if ClaudeNotifier exists and is executable
if [[ ! -x "$CLAUDE_NOTIFIER" ]]; then
    USE_OSASCRIPT="1"
fi

# Try to read JSON from stdin first (non-blocking)
# Claude Code passes context data through stdin for hooks
# Read all available data from stdin (JSON may span multiple lines)
STDIN_DATA=""
if [[ ! -t 0 ]]; then
    # stdin is not a terminal, read all data
    STDIN_DATA=$(cat)
fi

if [[ -n "$STDIN_DATA" ]]; then
    # Try to extract cwd from JSON using grep/sed (more reliable than bash regex)
    # First try session_cwd, then fall back to cwd
    STDIN_PROJECT_DIR=$(echo "$STDIN_DATA" | grep -o '"session_cwd":"[^"]*"' | sed 's/"session_cwd":"//;s/"$//' 2>/dev/null)
    if [[ -z "$STDIN_PROJECT_DIR" ]]; then
        STDIN_PROJECT_DIR=$(echo "$STDIN_DATA" | grep -o '"cwd":"[^"]*"' | sed 's/"cwd":"//;s/"$//' 2>/dev/null)
    fi
fi

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
        -k|--message-key)
            MESSAGE_KEY="$2"
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
        --locale)
            LOCALE="$2"
            shift 2
            ;;
        --directory-format)
            DIRECTORY_FORMAT="$2"
            shift 2
            ;;
        --project-dir)
            STDIN_PROJECT_DIR="$2"
            shift 2
            ;;
        --no-sound)
            SOUND=""
            shift
            ;;
        --use-osascript)
            USE_OSASCRIPT="1"
            shift
            ;;
        -h|--help)
            echo "Usage: notify.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -t, --title              Notification title (default: 'Claude Code')"
            echo "  -m, --message            Notification message"
            echo "  -k, --message-key        Predefined message key (task_completed|permission_needed|input_needed)"
            echo "  -s, --sound              Sound name (default: 'Glass')"
            echo "  --subtitle               Notification subtitle"
            echo "  --locale LOCALE          Language: zh|en (default: auto-detect from \$LANG)"
            echo "  --directory-format FMT   Directory format: short|full|none (default: none)"
            echo "  --project-dir DIR        Project directory to display (overrides auto-detection)"
            echo "  --no-sound               Disable sound"
            echo "  --use-osascript          Force using osascript instead of ClaudeNotifier"
            echo "  -h, --help               Show this help message"
            echo ""
            echo "Available sounds: Basso, Blow, Bottle, Frog, Funk, Glass, Hero,"
            echo "                  Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink"
            echo ""
            echo "Examples:"
            echo "  notify.sh -m 'Build complete'"
            echo "  notify.sh -k task_completed --locale zh --directory-format short"
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

# If message is empty and no key provided, use default
if [[ -z "$MESSAGE" && -z "$MESSAGE_KEY" ]]; then
    # If we got stdin data, use default message key
    if [[ -n "$STDIN_DATA" ]]; then
        MESSAGE_KEY="task_completed"
    fi
fi

# Detect locale
LOCALE=$(detect_locale "$LOCALE")

# Translate message if message key is provided
if [[ -n "$MESSAGE_KEY" ]]; then
    MESSAGE=$(translate_message "$MESSAGE_KEY" "$LOCALE")
fi

# Validate message
if [[ -z "$MESSAGE" ]]; then
    MESSAGE="Notification"
fi

# Add directory info to message prefix if requested (ClaudeNotifier doesn't support subtitle)
if [[ "$DIRECTORY_FORMAT" != "none" ]]; then
    DIR_INFO=$(get_directory_info "$DIRECTORY_FORMAT")
    if [[ -n "$DIR_INFO" ]]; then
        MESSAGE="[$DIR_INFO] $MESSAGE"
    fi
fi

# Use ClaudeNotifier.app for native notifications with Claude icon
if [[ -z "$USE_OSASCRIPT" ]]; then
    # Build command array to avoid eval injection risks
    CMD=("$CLAUDE_NOTIFIER" -title "$TITLE" -message "$MESSAGE")

    if [[ -n "$SOUND" ]]; then
        CMD+=(-sound "$SOUND")
    fi

    "${CMD[@]}" &
else
    # Fallback to AppleScript
    SCRIPT="display notification \"$MESSAGE\" with title \"$TITLE\""

    if [[ -n "$SUBTITLE" ]]; then
        SCRIPT="$SCRIPT subtitle \"$SUBTITLE\""
    fi

    if [[ -n "$SOUND" ]]; then
        SCRIPT="$SCRIPT sound name \"$SOUND\""
    fi

    osascript -e "$SCRIPT"
fi
