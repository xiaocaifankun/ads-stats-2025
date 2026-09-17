# AGENTS.md

本文件定义 agent 如何维护这个知识库（LLM Wiki 模式，源自 Andrej Karpathy 的 llm-wiki 构想）。

## Mission（使命）

把这个仓库当作三层系统来对待：

- `raw/` — 不可变的原始素材与附件。agent 只读，永不修改。
- `wiki/` — 由 agent 编写和维护的 Markdown 知识库。
- `AGENTS.md` — 约束 agent 行为的 schema / 操作手册。

人类负责策展素材、判断什么重要、提出问题。Agent 负责所有让知识库长期保持连贯的维护工作：摘要、交叉引用、建索引、记录日志、发现矛盾。

核心区别：**wiki 是一个持续积累的产物**。交叉引用已经建好，矛盾已经被标记，综述已经反映了读过的一切。每加一份素材、每问一个问题，wiki 都更丰富一层。知识是"编译一次、持续保持最新"，而不是每次查询重新拼装。

## Startup Routine（每次会话开始）

1. 读本文件。
2. 读 `wiki/index.md`。
3. 读 `wiki/log.md` 的最新若干条。
4. 改动前先检查 `wiki/` 中相关区域。

## Non-Negotiable Rules（不可违背的规则）

- 绝不修改 `raw/` 下的文件。
- 优先更新已有的规范页面，而不是创建重复页面。
- 重要论断必须引用来源页面。
- 明确标注不确定性。
- 不要静默抹除矛盾——记录下来。
- 尽可能保持链接稳定。
- 新增页面或页面摘要实质性变化时，更新 `wiki/index.md`。
- ingest / query / lint / schema 维护动作都要追加到 `wiki/log.md`。

## Source Layout（原始素材布局）

- `raw/` 下的文件是不可变输入。
- 素材可直接放在 `raw/sources/` 下，也可放在稳定的主题子目录中（如 `raw/sources/ads-design/`）。
- 保留用户选择的素材组织方式，不要擅自摊平。
- wiki 页面引用原始文件时，使用真实的相对路径。
- 图片、附件统一放 `raw/assets/`。

## Wiki Page Types（页面类型）

- `wiki/sources/` — 单份原始素材的摘要页
- `wiki/entities/` — 实体页：人物、组织、工具、项目、地点等具名对象
- `wiki/concepts/` — 概念页：观点、方法、主题、模型、理论
- `wiki/outputs/` — 由查询产生的可复用产出（对比、综述、时间线、简报）
- `wiki/maintenance/` — lint 报告、一致性检查、清理建议
- `wiki/indexes/` — 根 `index.md` 之外的专用索引（可选）

## Naming Conventions（命名约定）

- 文件名统一 lowercase kebab-case。
- 优先短而稳定的名字。
- 素材摘要页用基于素材标题的描述性文件名。
- 产出页在有助于唯一性时加日期前缀（如 `2026-09-10-rag-vs-wiki.md`）。

## Frontmatter（元数据）

在有助于结构化时使用 YAML frontmatter，保持轻量。推荐字段：

```yaml
---
title:
type:          # source | entity | concept | output | maintenance
status:        # draft | active | stale | archived
created:
updated:
sources:       # 引用的素材或页面（wiki 链接）
tags:
aliases:
confidence:    # high | medium | low
---
```

不要让元数据维护喧宾夺主、压过内容本身。

## Linking Conventions（链接约定）

- 用 wiki 风格链接指向已有的规范页面：`[[concepts/llm-wiki]]`。
- 合适时添加 "Related" / "See also" 小节。
- 当一份素材更新了某个实体或概念时，两侧都要反映：
  - 在实体/概念页里加上这份素材
  - 在素材摘要页里加上对应实体/概念的链接

## Contradictions and Uncertainty（矛盾与不确定）

新证据与旧内容冲突时：

- 不要在不说明冲突的情况下覆盖旧论断。
- 更新综述以反映这一分歧。
- 引用涉及的页面或素材。
- 需要跟进时记入 maintenance 产出。

使用明确措辞：`Open question`、`Conflicting evidence`、`Low confidence`。

## index.md Rules（索引规则）

`index.md` 是面向内容的目录。更新规则：

- 按类别分组
- 每个页面附一行摘要
- 措辞简洁、可扫读
- 新页面及时加入
- 页面实质变化时刷新摘要

查询流程中先读 `index.md` 定位相关页面，再深入正文。

## log.md Rules（日志规则）

`log.md` 只追加、按时间顺序。每条记录以固定前缀开头：

- `## [YYYY-MM-DD] ingest | 标题`
- `## [YYYY-MM-DD] query | 问题`
- `## [YYYY-MM-DD] lint | 范围`
- `## [YYYY-MM-DD] maintenance | 说明`

每条包含：发生了什么、动了哪些文件、值得注意的发现或未决问题。

固定前缀便于用 unix 工具解析：`grep "^## \[" wiki/log.md | tail -5`。

## Ingest Workflow（收录流程）

被要求收录素材时：

1. 在 `raw/sources/`（含嵌套子目录）中定位新文件，以及 `raw/assets/` 中的相关附件。
2. 读素材全文。
3. 在 `wiki/sources/` 创建或更新摘要页。
4. 更新受影响的 `wiki/entities/` 实体页。
5. 更新受影响的 `wiki/concepts/` 概念页。
6. 若新素材改变了已有产出/综述页，一并更新。
7. 更新 `wiki/index.md`。
8. 追加一条 ingest 记录到 `wiki/log.md`。

若素材关联很弱或高度冗余，在摘要页里说明，而不是硬造新页面。一次收录可能触及 10–15 个页面。

## Query Workflow（查询流程）

被提问时：

1. 读 `index.md`。
2. 定位可能相关的页面。
3. 只深入读取必要的最小页面集合。
4. 综合作答，引用所用到的 wiki 页面或素材摘要。
5. 若答案有长期价值，写入 `wiki/outputs/`。
6. 合适时把产出链接回相关素材、实体、概念页。
7. 若创建了持久页面，更新 `index.md`。
8. 若归档了页面或做了实质性分析，追加 query 记录到 `log.md`。

**关键**：好答案要回写进 wiki。一次对比、一份分析、一个新洞见，都应沉淀为新页面，而不是消失在对话记录里。

## Lint Workflow（质检流程）

被要求 lint 时：

1. 检查 `index.md`、`log.md` 近期条目和相关 wiki 区域。
2. 查找：
   - 页面间矛盾
   - 被更新素材取代的过时论断
   - 无入链的孤儿页
   - 缺失的交叉引用
   - 被提及但缺少独立页面的重要概念 / 实体
   - 缺失引用
   - 因近期 ingest 产生的失效假设
3. 把发现写入 `wiki/maintenance/`。
4. 合适时建议下一步该问的问题或该补的素材。
5. 追加 lint 记录到 `log.md`。

建议每 2–3 天或每约 10 次 ingest 跑一次 lint。

## Filing Policy（归档策略）

好的产出应当积累。若查询产生了可复用的东西——对比、综述、时间线、简报、大纲——优先归档到 `wiki/outputs/`，而不是留在对话里。

## Human-Agent Division of Labor（人机分工）

人类应当：选择素材、判断什么值得关注、引导重点、检查重要产出。

Agent 应当：摘要、交叉引用、更新相关页面、维护索引、记录日志、建议有价值的后续工作。

## Model Guidance（模型说明）

本仓库不设定 agent 使用的模型——模型选择在外部工具/运行时里（如 Claude Code、Codex、OpenCode 或其他 agent 环境）。

尽可能选择：强长上下文阅读与综合能力、可靠的 Markdown 编辑、跨多文件良好的指令遵循、素材含图时支持多模态。

使用较弱模型时：缩小任务粒度、减小 ingest 批次、增加人工复核。
