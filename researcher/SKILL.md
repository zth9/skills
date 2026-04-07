---
name: researcher
description: 构建并维护持久化个人知识库，专为深度研究某一技术领域的架构、模型、原理、机制和落地实践而设计。内部使用 LLM Wiki 模式组织知识，支持持续学习和知识复合积累。触发场景：用户想要初始化研究仓库、摄入源文档/网址/代码库并组织知识、或从知识库中查询并输出专业文档。适用于：研究技术领域、分析代码库、快速探索陌生领域、沉淀日常技术灵感、演进 idea。
---

# Researcher

基于 LLM Wiki 模式的持久化知识库，专为技术领域深度研究设计。知识随每次摄入和查询持续复合积累。

## 使用方式

调用 `/researcher` 后，根据用户的意图自动判断执行以下哪个操作：

1. **初始化**：用户提到"初始化"、"创建仓库"、"setup" 等 → 执行初始化流程
2. **摄入源**：用户提供文件路径、网址、代码库 → 执行摄入流程
3. **查询知识**：用户提出问题或查询请求 → 执行查询流程

用户也可以明确指定操作，例如：
- `/researcher init` - 初始化研究仓库
- `/researcher research <source>` - 摄入源并组织知识
- `/researcher consult <query>` - 从知识库查询

## 仓库结构

```
<repo>/
├── AGENTS.md          # Wiki schema 和约定（由 init 生成，canonical）
├── CLAUDE.md          # -> AGENTS.md 软链接
├── GEMINI.md          # -> AGENTS.md 软链接
├── raw/               # 不可变源文档
│   └── assets/        # 图片和媒体文件
└── wiki/
    ├── index.md       # 内容目录（每次摄入后更新）
    ├── log.md         # 操作日志（追加写入）
    ├── source_*.md    # 源摘要页面
    ├── entity_*.md    # 实体页面（人物、组织、产品）
    ├── concept_*.md   # 概念页面
    └── analysis_*.md  # 分析页面（consult 结果自动保存）
```

---

## 操作流程判断

当用户调用 `/researcher` 时，根据以下规则判断执行哪个操作：

### 1. 初始化操作
**触发条件**：
- 用户明确说"init"、"初始化"、"创建仓库"、"setup"
- 或者当前目录下不存在研究仓库结构（无 wiki/ 目录）

**执行流程**：
1. 询问仓库路径（默认 `./research`）
2. 运行 `python scripts/init_repo.py <path>`
3. 确认结构并说明后续步骤

### 2. 摄入源操作
**触发条件**：
- 用户明确说"research"、"摄入"、"分析"、"添加"
- 或者用户提供了具体的源（文件路径、网址、代码库链接）

**执行流程**：见下方"阶段 2：摄入源"

### 3. 查询知识操作
**触发条件**：
- 用户明确说"consult"、"查询"、"问"
- 或者用户提出了一个问题/查询请求
- 或者用户想要总结/分析已有知识

**执行流程**：见下方"阶段 3：查询知识"

---

## 阶段 2：摄入源

**完全自动化，使用 Multi-Agent 并行分析。**

### 源类型处理

| 源类型 | 处理方式 |
|--------|----------|
| 文件（PDF/MD/TXT） | 直接读取 `raw/` 中的文件 |
| 网址/博客/公众号 | 使用 `/web-access` skill 抓取转换为 markdown，保存到 `raw/` |
| 图片 | 保存到 `raw/assets/`，用 LLM 解读图片内容 |
| 对话记录/ASR 字幕 | 直接读取文本内容 |
| 代码库 | clone 到仓库目录，读取代码文件进行分析 |

### Multi-Agent 工作流

派出 **3 个并行 subagent**，均以**第一性原理**为核心，实事求是，不夸大也不贬低：

**Agent 1 - 理论分析者**
- 提取核心概念、原理、模型、架构
- 从第一性原理推演知识体系
- 识别关键抽象和设计决策

**Agent 2 - 实践探索者**
- 关注落地措施、实现细节、代码示例
- 提取最佳实践和常见模式
- 分析性能指标和工程权衡

**Agent 3 - 批判性思考者**
- 识别问题、矛盾、局限性
- 标记未解决的挑战和开放问题
- 对比不同方案的优劣

### Main-Agent 综合流程

1. 收集三个 subagent 的分析结果
2. 创建/更新 wiki 页面：
   - `wiki/source_<title>.md` - 源摘要
   - `wiki/entity_<name>.md` - 实体页面
   - `wiki/concept_<name>.md` - 概念页面
3. 添加交叉引用 `[[page_name]]`
4. 更新 `wiki/index.md`
5. 追加到 `wiki/log.md`：`## [YYYY-MM-DD] ingest | <title>`
6. 输出摘要：创建/更新了哪些页面

### 代码库特殊处理

- 将代码库 clone/复制到仓库目录
- research 阶段：读取关键代码文件，理解整体架构和实现机制
- consult 阶段：可继续细致探索具体代码（consult 本身包含 research 能力）
- wiki 页面类型：模块页面、接口页面、设计模式页面、数据流页面

---

## 阶段 3：查询知识

### 流程

1. 读取 `wiki/index.md` 找到相关页面
2. 读取相关 wiki 页面（必要时用 grep 搜索）
3. 如需要，对代码库或源文档进行补充探索
4. 综合输出**完整专业文档**
5. **自动保存**为 `wiki/analysis_<topic>_<date>.md`
6. 追加到 `wiki/log.md`：`## [YYYY-MM-DD] consult | <query>`

### 输出文档规范

根据问题类型，输出完整的专业 markdown 文档，包含适用的内容：

- **代码示例和实现细节**（带语言标注的代码块）
- **架构图和流程图**（Mermaid 图表）
- **技术对比表格**
- **最佳实践和反模式**
- **性能指标和基准测试**
- **引用来源**：`[source_title](wiki/source_title.md)`

### 典型 Consult 问题模式

| 问题类型 | 输出重点 |
|----------|----------|
| "目前研究到什么程度了" | 知识覆盖地图、已摄入源列表、待探索方向 |
| "有哪些可以落地的措施" | 实践清单、实现步骤、代码示例 |
| "未妥善解决的问题" | 开放问题列表、已知局限、研究空白 |
| "总结心智模型和认知框架" | 概念层次图、核心抽象、思维框架 |
| "从第一性原理拆解" | 逐层推演、基本假设、推导链路 |

---

## Wiki 页面格式

### 源摘要 (`source_*.md`)
```markdown
---
source: raw/filename
date: YYYY-MM-DD
type: article|paper|code|video|conversation
---
# Source: 标题
## 关键要点
## 核心论点
## 相关
- [[concept_name]]
- [[entity_name]]
```

### 概念页面 (`concept_*.md`)
```markdown
---
type: concept
---
# Concept: 名称
## 定义（第一性原理）
## 实现机制
## 演化（跨源对比）
## 相关概念
- [[related_concept]]
```

### 分析页面 (`analysis_*.md`)
```markdown
---
type: analysis
query: 原始查询
date: YYYY-MM-DD
sources: [source1, source2]
---
# Analysis: 主题
[完整专业文档内容]
```

---

## 维护操作

**Lint Wiki**（定期执行）：
- 查找页面间矛盾
- 识别孤立页面（无入站链接）
- 标记过时信息
- 建议新的研究方向

---

## 注意事项

- 所有 consult 结果自动保存，形成可查阅的分析档案
- 代码库分析时，consult 阶段可直接读取代码进行细致探索
- 图片需先保存到 `raw/assets/`，再由 LLM 解读内容
- 网页抓取统一使用 `/web-access` skill
