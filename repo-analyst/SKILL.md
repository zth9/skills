---
name: repo-analyst
description: |
  深度分析 GitHub 开源仓库的全方位 skill。对任意开源项目进行系统性拆解，输出结构化研究报告。
  触发场景：
  - 用户提供 GitHub 仓库 URL 或本地仓库路径，想要了解该项目
  - "帮我分析这个仓库"、"学习这个开源项目"、"这个项目用了什么技术栈"
  - "分析一下这个项目的架构"、"这个仓库怎么入手学习"
  - 用户想了解项目的 5W2H、技术栈、架构、特性、工程实践、社区生态
  - 用户想获得一个开源项目的源码阅读路径建议
---

# 开源仓库深度分析

对指定开源仓库进行全方位分析，输出结构化研究报告，帮助开发者快速建立对项目的完整认知。

## 分析流程

按以下 3 个阶段执行，每步基于仓库实际内容（代码、文档、commit 历史、issues）。无法获取的信息标注"未找到相关信息"，不编造。

### 阶段一：信息采集

根据仓库来源采集基础数据：

**本地仓库：**
- 读取项目配置文件（`package.json` / `Cargo.toml` / `go.mod` / `pom.xml` / `pyproject.toml` 等）
- `git log --oneline -20` 查看近期提交
- `git shortlog -sn --no-merges | head -10` 查看核心贡献者
- `git tag --sort=-creatordate | head -10` 查看版本标签
- 列出顶层目录结构
- 检查 CI 配置（`.github/workflows/`、`.gitlab-ci.yml` 等）
- 检查 linter/formatter/test 配置

**远程仓库（GitHub URL）：**
- 使用 GitHub MCP 工具获取仓库信息、文件内容、commits、releases、issues
- 获取 README、配置文件、目录结构

### 阶段二：七维分析

采集完成后，按以下维度逐步分析。每个维度的详细检查清单见 [references/analysis-checklist.md](references/analysis-checklist.md)。

| 步骤 | 维度 | 核心问题 |
|------|------|----------|
| 1 | 项目概览（5W2H） | What/Why/Who/When/Where/How/How much |
| 2 | 技术栈全景 | 语言、框架、工具链、基础设施、依赖图谱 |
| 3 | 架构与代码组织 | 目录结构、架构模式、数据流、模块依赖 |
| 4 | 核心能力与特性 | 功能列表、API入口、差异化特性、扩展机制 |
| 5 | 代码质量与工程实践 | 测试、规范、文档、版本管理、安全 |
| 6 | 社区与生态 | 治理、贡献流程、生态系统、路线图 |
| 7 | 学习路径建议 | 源码阅读顺序、入口点、设计决策、首次贡献 |

### 阶段三：报告生成

按 [references/report-template.md](references/report-template.md) 的模板格式输出报告。

报告要求：
- Markdown 格式，保存到 `~/tmp/repo-analyst-{repo-name}-{date}.md`
- 开头 3-5 句执行摘要，末尾一句话总结
- 关键信息用表格呈现
- 架构关系用 Mermaid 图表可视化
- 代码路径用 `code` 格式标注
- 报告语言跟随用户（默认中文）

## 约束

- 只读分析，不修改仓库任何文件
- 基于实际数据，不猜测不编造
- 大型仓库（>10000 文件）适当简化，聚焦核心模块
- monorepo 需识别并概述各子项目
