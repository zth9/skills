---
name: mac-notifier
description: Send native macOS notifications when Claude Code completes tasks or awaits user input. Use when user wants to set up desktop notifications, enable alerts for task completion, or configure Claude Code hooks for background monitoring.
version: 2.1.0
entry_point: scripts/notify.sh
dependencies: ["jq"]
---

# Mac Notifier for Claude Code

A lightweight utility that sends native macOS notifications when Claude Code events occur, such as task completion or waiting for user input.

## Features

- Native macOS notifications via AppleScript
- Customizable notification sounds
- Support for task completion, permission request, and MCP elicitation events
- **i18n support**: Auto-detect language from `$LANG` (zh/en)
- **Directory info**: Show project directory in notification subtitle
- Zero external dependencies (except `jq` for installation script)

## Installation

Use the installation script to configure hooks in your Claude Code settings:

```bash
# Install hooks to Claude Code
./scripts/install.sh install

# With custom sounds
./scripts/install.sh install --stop-sound Hero --permission-sound Pop

# With Chinese locale and directory info
./scripts/install.sh install --locale zh --directory-format short

# With English locale and full directory path
./scripts/install.sh install --locale en --directory-format full
```

This will automatically:
1. Backup your existing `~/.claude/settings.json`
2. Add notification hooks for task completion and user input prompts
3. Test the notification to verify it works

### Uninstall

```bash
./scripts/install.sh uninstall
```

### Check Status

```bash
./scripts/install.sh status
```

## Installation Script Options

```bash
./scripts/install.sh [COMMAND] [OPTIONS]

Commands:
  install     Install hooks to Claude Code settings (default)
  uninstall   Remove hooks from Claude Code settings
  status      Show current hooks configuration
  test        Test notification functionality
  help        Show help message

Options for install:
  --stop-sound SOUND        Sound for task completion (default: Glass)
  --permission-sound SOUND  Sound for permission prompt (default: Funk)
  --locale LOCALE           Language: zh|en (default: auto-detect from $LANG)
  --directory-format FMT    Directory format: short|full|none (default: none)
```

## Manual Configuration

If you prefer manual configuration, add the following to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/mac-notifier/scripts/notify.sh -k task_completed --locale zh --directory-format short"
          }
        ]
      }
    ],
    "PermissionRequest": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/mac-notifier/scripts/notify.sh -k permission_needed --locale zh --directory-format short -s Funk"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "elicitation_dialog",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/mac-notifier/scripts/notify.sh -k input_needed --locale zh --directory-format short -s Ping"
          }
        ]
      }
    ]
  }
}
```

## Notification Script Usage

```bash
# Basic notification
./scripts/notify.sh -m "Hello World"

# With custom title
./scripts/notify.sh -t "My App" -m "Process finished"

# With subtitle
./scripts/notify.sh -m "Build successful" --subtitle "Project: my-app"

# With custom sound
./scripts/notify.sh -m "Attention needed" -s Ping

# Silent notification (no sound)
./scripts/notify.sh -m "Silent update" --no-sound

# Using predefined message key with localization
./scripts/notify.sh -k task_completed --locale zh

# With directory info (project name)
./scripts/notify.sh -k task_completed --directory-format short

# With full directory path
./scripts/notify.sh -m "Build done" --directory-format full

# Show help
./scripts/notify.sh --help
```

## Parameters

| Parameter | Description |
|-----------|-------------|
| `-t, --title` | Notification title (default: `Claude Code`) |
| `-m, --message` | Notification message |
| `-k, --message-key` | Predefined message key: `task_completed`, `permission_needed`, `input_needed` |
| `-s, --sound` | Sound name (default: `Glass`) |
| `--subtitle` | Notification subtitle |
| `--locale` | Language: `zh` or `en` (default: auto-detect from `$LANG`) |
| `--directory-format` | Directory format: `short` (project name), `full` (absolute path), `none` |
| `--no-sound` | Disable notification sound |
| `-h, --help` | Show help message |

## Localization

The script supports Chinese (zh) and English (en) localization:

| Message Key | English | Chinese |
|-------------|---------|---------|
| `task_completed` | Task completed | 任务已完成 |
| `permission_needed` | Permission needed | 需要权限确认 |
| `input_needed` | Input needed for MCP tool | MCP 工具需要输入 |

Language is auto-detected from `$LANG` environment variable, or can be specified via `--locale` parameter.

## Directory Format

The `--directory-format` option controls how directory info is displayed in the notification subtitle:

| Format | Description | Example |
|--------|-------------|---------|
| `short` | Project name (basename) | `skills` |
| `full` | Full absolute path | `/Users/tian/osproject/zth9/skills` |
| `none` | No directory info (default) | - |

**Directory detection priority:**
1. `CLAUDE_PROJECT_DIR` environment variable (set by Claude Code)
2. Git repository root directory
3. Current working directory (`PWD`)

## Available Sounds

macOS provides the following built-in notification sounds:

| Sound | Description |
|-------|-------------|
| `Basso` | Low-pitched alert |
| `Blow` | Soft whoosh |
| `Bottle` | Cork pop |
| `Frog` | Frog croak |
| `Funk` | Funky tone |
| `Glass` | Glass tap (default) |
| `Hero` | Heroic fanfare |
| `Morse` | Morse code beep |
| `Ping` | Clear ping |
| `Pop` | Pop sound |
| `Purr` | Cat purr |
| `Sosumi` | Classic Mac alert |
| `Submarine` | Submarine sonar |
| `Tink` | Light tap |

## Hook Events

Claude Code supports several hook events that can trigger notifications:

| Event | Description |
|-------|-------------|
| `Stop` | Claude completes its response (immediate notification) |
| `PermissionRequest` | When permission dialog appears (immediate notification) |
| `Notification` with `elicitation_dialog` | When Claude Code needs input for MCP tool elicitation |
| `SubagentStop` | A sub-agent task completes |
| `PostToolUse` | After a tool executes successfully |

> **Note**: This skill uses `Stop`, `PermissionRequest`, and `Notification` (elicitation_dialog) hooks which trigger immediately when human intervention is needed. The `idle_prompt` is not used because it has a built-in 60-second delay.

## How It Works

The installation script modifies your `~/.claude/settings.json` to register hooks:

1. **Stop Hook**: Triggered immediately when Claude finishes responding to your request
2. **PermissionRequest Hook**: Triggered immediately when Claude needs permission to execute a command
3. **Notification Hook (elicitation_dialog)**: Triggered when Claude needs input for MCP tool

## Troubleshooting

### Notifications Not Appearing

1. Check System Settings → Notifications → Script Editor is enabled
2. Ensure Terminal/iTerm has notification permissions
3. Verify the script has execute permissions: `chmod +x notify.sh`

### No Sound Playing

1. Check system volume is not muted
2. Verify the sound name is spelled correctly (case-sensitive)
3. Try a different sound name

### Installation Issues

1. Ensure `jq` is installed: `brew install jq`
2. Check if `~/.claude/settings.json` is valid JSON
3. Run `./scripts/install.sh status` to see current configuration

## License

MIT
