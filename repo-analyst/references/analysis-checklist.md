# 分析检查清单

## 1. 项目概览（5W2H）

### What
- 项目名称和一句话描述
- 解决的核心问题
- 核心价值主张（vs 现有方案）

### Why
- 创建动机和背景
- 现有方案的痛点

### Who
- 维护者/组织
- 核心贡献者 TOP 5（`git shortlog -sn --no-merges | head -5`）
- 目标用户画像

### When
- 首次提交时间（`git log --reverse --format="%ai" | head -1`）
- 最近提交时间（`git log -1 --format="%ai"`）
- 发布节奏（tags 间隔）
- 重要里程碑（CHANGELOG / releases）

### Where
- 支持的平台/运行环境
- 集成的生态系统
- 分发渠道（npm/PyPI/crates.io/Docker Hub 等）

### How
- 安装命令
- 最小可运行示例
- 核心使用路径

### How Much
- 代码行数（`find src -name '*.ts' -o -name '*.py' | xargs wc -l` 或类似）
- 依赖数量（直接 + 开发）
- GitHub stars/forks/contributors
- Open issues / PRs 数量

## 2. 技术栈全景

检查以下文件确定技术栈：

| 语言/生态 | 配置文件 |
|-----------|----------|
| Node/TS | `package.json`, `tsconfig.json` |
| Rust | `Cargo.toml` |
| Go | `go.mod` |
| Python | `pyproject.toml`, `setup.py`, `requirements.txt` |
| Java | `pom.xml`, `build.gradle` |

关注点：
- 运行时版本要求（engines 字段、.node-version、.python-version 等）
- 构建工具（webpack/vite/tsup/esbuild/cargo/make 等）
- 测试框架（jest/vitest/pytest/cargo test 等）
- Lint/Format（eslint/oxlint/prettier/rustfmt/black 等）
- CI/CD（`.github/workflows/`、`.gitlab-ci.yml`）
- 容器化（`Dockerfile`、`docker-compose.yml`）

## 3. 架构与代码组织

- 顶层目录结构（`ls` 或 tree depth=2）
- 入口文件（`main` 字段、`bin` 字段、`src/main.rs`、`cmd/` 等）
- 模块划分原则（按功能/按层/按领域）
- 架构模式识别：
  - 插件化：检查 plugin/extension 目录
  - Monorepo：检查 `workspaces`、`packages/`、`apps/`
  - 微服务：检查 `services/`、docker-compose 多服务
  - MVC：检查 controllers/models/views 目录
- 关键抽象和接口（grep `interface`/`trait`/`abstract`/`protocol`）
- 绘制模块依赖 Mermaid 图

## 4. 核心能力与特性

- README 中列出的功能
- CLI 命令（检查 `bin`、`commands/` 目录）
- API 端点（检查 routes/controllers）
- 配置项（检查 config schema、env vars）
- 扩展机制：
  - 插件系统
  - Hooks/中间件
  - 事件系统
  - SDK/API

## 5. 代码质量与工程实践

- 测试：`*.test.*` / `*.spec.*` / `tests/` 文件数量和分布
- 覆盖率配置（vitest.config、jest.config、.coveragerc）
- 类型检查（tsconfig strict、mypy、clippy）
- 文档：README 完整性、API docs、CONTRIBUTING.md
- 版本策略：semver / calver / 自定义
- 安全：SECURITY.md、依赖审计配置、.env 是否在 .gitignore

## 6. 社区与生态

- LICENSE 类型
- CONTRIBUTING.md 内容
- Issue/PR 模板（`.github/ISSUE_TEMPLATE/`）
- 行为准则（CODE_OF_CONDUCT.md）
- 最近 30 天 issue/PR 活跃度
- 插件/扩展生态
- 路线图（ROADMAP.md 或 GitHub Projects）

## 7. 学习路径建议

基于以上分析，推荐：
- 入口文件 → 核心模块 → 辅助模块的阅读顺序
- 最值得研究的 3-5 个设计决策
- `good first issue` 标签的 issues
- 测试文件作为理解行为的辅助
