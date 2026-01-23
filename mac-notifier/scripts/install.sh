#!/bin/bash
# Mac Notifier Installation Script for Claude Code Hooks
# Automatically configures hooks in Claude Code settings

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NOTIFY_SCRIPT="$SCRIPT_DIR/notify.sh"
CLAUDE_SETTINGS_DIR="$HOME/.claude"
CLAUDE_SETTINGS_FILE="$CLAUDE_SETTINGS_DIR/settings.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if jq is installed
check_jq() {
    if ! command -v jq &> /dev/null; then
        print_error "jq is required but not installed."
        echo "Please install jq first:"
        echo "  brew install jq"
        exit 1
    fi
}

# Create settings directory if it doesn't exist
ensure_settings_dir() {
    if [[ ! -d "$CLAUDE_SETTINGS_DIR" ]]; then
        print_info "Creating Claude settings directory..."
        mkdir -p "$CLAUDE_SETTINGS_DIR"
    fi
}

# Create default settings file if it doesn't exist
ensure_settings_file() {
    if [[ ! -f "$CLAUDE_SETTINGS_FILE" ]]; then
        print_info "Creating new settings file..."
        echo '{}' > "$CLAUDE_SETTINGS_FILE"
    fi
}

# Backup existing settings
backup_settings() {
    if [[ -f "$CLAUDE_SETTINGS_FILE" ]]; then
        local backup_file="$CLAUDE_SETTINGS_FILE.backup.$(date +%Y%m%d_%H%M%S)"
        cp "$CLAUDE_SETTINGS_FILE" "$backup_file"
        print_info "Backed up existing settings to: $backup_file"
    fi
}

# Generate hooks configuration
generate_hooks_config() {
    local stop_sound="${1:-Glass}"
    local permission_sound="${2:-Funk}"

    cat << EOF
{
  "Stop": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "$NOTIFY_SCRIPT -m 'Task completed' -s $stop_sound"
        }
      ]
    }
  ],
  "PermissionRequest": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "$NOTIFY_SCRIPT -m 'Permission needed' -s $permission_sound"
        }
      ]
    }
  ]
}
EOF
}

# Install hooks to settings
install_hooks() {
    local stop_sound="${1:-Glass}"
    local permission_sound="${2:-Funk}"

    print_info "Installing Mac Notifier hooks..."

    # Read current settings
    local current_settings
    current_settings=$(cat "$CLAUDE_SETTINGS_FILE")

    # Generate new hooks config
    local hooks_config
    hooks_config=$(generate_hooks_config "$stop_sound" "$permission_sound")

    # Check if hooks already exist
    if echo "$current_settings" | jq -e '.hooks' > /dev/null 2>&1; then
        # Merge with existing hooks
        print_info "Merging with existing hooks configuration..."

        local new_settings
        new_settings=$(echo "$current_settings" | jq --argjson newhooks "$hooks_config" '
            .hooks = (.hooks // {}) * $newhooks
        ')

        echo "$new_settings" | jq '.' > "$CLAUDE_SETTINGS_FILE"
    else
        # Add new hooks section
        local new_settings
        new_settings=$(echo "$current_settings" | jq --argjson newhooks "$hooks_config" '
            .hooks = $newhooks
        ')

        echo "$new_settings" | jq '.' > "$CLAUDE_SETTINGS_FILE"
    fi

    print_success "Hooks installed successfully!"
}

# Uninstall hooks from settings
uninstall_hooks() {
    print_info "Uninstalling Mac Notifier hooks..."

    if [[ ! -f "$CLAUDE_SETTINGS_FILE" ]]; then
        print_warning "Settings file not found. Nothing to uninstall."
        return
    fi

    local current_settings
    current_settings=$(cat "$CLAUDE_SETTINGS_FILE")

    # Remove our hooks (ones that contain notify.sh)
    local new_settings
    new_settings=$(echo "$current_settings" | jq '
        if .hooks then
            .hooks |= with_entries(
                .value |= map(
                    select(.hooks | all(.command | contains("notify.sh") | not))
                ) | select(length > 0)
            ) | if .hooks == {} then del(.hooks) else . end
        else
            .
        end
    ')

    echo "$new_settings" | jq '.' > "$CLAUDE_SETTINGS_FILE"

    print_success "Hooks uninstalled successfully!"
}

# Show current hooks status
show_status() {
    print_info "Current hooks status:"
    echo ""

    if [[ ! -f "$CLAUDE_SETTINGS_FILE" ]]; then
        print_warning "Settings file not found: $CLAUDE_SETTINGS_FILE"
        return
    fi

    local hooks
    hooks=$(jq '.hooks // {}' "$CLAUDE_SETTINGS_FILE")

    if [[ "$hooks" == "{}" ]]; then
        echo "No hooks configured."
    else
        echo "$hooks" | jq '.'
    fi
}

# Test notification
test_notification() {
    print_info "Testing notification..."
    "$NOTIFY_SCRIPT" -m "Mac Notifier installed successfully!" -s Glass
    print_success "If you saw a notification, the installation is working!"
}

# Show help
show_help() {
    echo "Mac Notifier Installation Script for Claude Code"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  install     Install hooks to Claude Code settings (default)"
    echo "  uninstall   Remove hooks from Claude Code settings"
    echo "  status      Show current hooks configuration"
    echo "  test        Test notification functionality"
    echo "  help        Show this help message"
    echo ""
    echo "Options for install:"
    echo "  --stop-sound SOUND       Sound for task completion (default: Glass)"
    echo "  --permission-sound SOUND Sound for permission prompt (default: Funk)"
    echo ""
    echo "Available sounds: Basso, Blow, Bottle, Frog, Funk, Glass, Hero,"
    echo "                  Morse, Ping, Pop, Purr, Sosumi, Submarine, Tink"
    echo ""
    echo "Examples:"
    echo "  $0 install"
    echo "  $0 install --stop-sound Hero --permission-sound Pop"
    echo "  $0 uninstall"
    echo "  $0 status"
}

# Main
main() {
    local command="${1:-install}"
    shift || true

    local stop_sound="Glass"
    local permission_sound="Funk"

    # Parse options
    while [[ $# -gt 0 ]]; do
        case $1 in
            --stop-sound)
                stop_sound="$2"
                shift 2
                ;;
            --permission-sound)
                permission_sound="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    case $command in
        install)
            check_jq
            ensure_settings_dir
            ensure_settings_file
            backup_settings
            install_hooks "$stop_sound" "$permission_sound"
            test_notification
            echo ""
            print_info "Restart Claude Code for changes to take effect."
            ;;
        uninstall)
            check_jq
            backup_settings
            uninstall_hooks
            ;;
        status)
            show_status
            ;;
        test)
            test_notification
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
