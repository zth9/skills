中文 | [English](./README_EN.md)

# Skills

从日常学习、工作中沉淀出来的 skills，用于构建个人 AI Workflow。

## 什么是 Skills？

Skills 是可复用的工具和脚本，用于增强 AI 编程助手（如 Claude Code、Cursor 等）的专业能力。每个技能都是独立的，可以轻松集成到你的工作流程中。

## 可用技能

| 技能 | 描述 |
|------|------|
| [mermaid-to-img](./mermaid-to-img/) | 将 Mermaid 图表转换为高质量图片（PNG/JPG/SVG/PDF） |
| [mac-notifier](./mac-notifier/) | 当 Claude Code 完成任务或等待输入时发送 macOS 原生通知 |
| [text-to-audio](./text-to-audio/) | 使用 easyVoice 将文本转换为语音，支持多角色配音 |

## 安装

### 方式一：在 Claude Code 中直接安装

1. 添加插件市场：

```
/plugin marketplace add zth9/skills
```

2. 安装单个技能：

```
/plugin install mermaid-to-img@zth9/skills
```

### 方式二：使用 openskills 工具

```bash
openskills install zth9/skills --global
```

### 方式三：手动复制

将技能文件夹复制到 Claude Code 的 skills 目录：

```bash
git clone https://github.com/zth9/skills.git
cp -r skills/mermaid-to-img ~/.claude/skills/
```

### 其他 AI 助手

每个技能都包含一个 `SKILL.md` 文件，其中的指令可用于任何 AI 编程助手。

## 许可证

MIT 许可证 - 详见 [LICENSE](./LICENSE)。
