---
title: "Agent 记忆系统 · 溯源式概念学习手册"
type: source
tags: [agent-memory, memory-taxonomy, context-engineering, workbuddy]
sources: []
date: 2026-09-03
source_file: raw/sources/agent-memory-guide.html
last_updated: 2026-09-17
---

# Agent 记忆系统 · 溯源式概念学习手册

## Summary

一份两段式手册：Part A 讲**通用记忆原理**（记忆分类学、读写回路、上下文工程），Part B 落到 **WorkBuddy 的三层记忆落地**。它走的是**分类学路线**——把认知科学的记忆分类直接当架构清单用：按「存哪里（上下文内 / 外部）」× 「存多久（短期 / 长期）」两条轴切分，判据是**这条信息要不要跨会话活**。

## Key Claims

- **「无状态」是问题，「记忆」是解**：记忆不在模型里，而在系统给它搭的「能存能取」的容器里。
- **记忆分类（工程清单）**：
  - **工作记忆** Working —— 上下文窗口内，实时；
  - **语义记忆** Semantic —— 事实、偏好、领域知识，**不含时间**，长期外部；
  - **情景记忆** Episodic —— 具体事件、会话记录、成败经历，**含时间**，长期外部；
  - **程序记忆** Procedural —— 怎么做、技能、工作流、行为规则，常以 skill / runbook 形式存在；
  - **检索记忆** Retrieval —— 窗口外的文档按需拉回（RAG），混合形态，向量库；
  - 另有两类常被提及：**参数记忆**（训练进权重的世界知识）与**前瞻记忆**（未执行的未来意图）。
  - 工程落地最常用前三类：**工作 + 语义 + 情景**。
- **判据**：这条信息「要不要跨会话活」→ 决定放上下文还是外部存储。
- **读写回路**：推理前 **Retrieve**（从长期记忆捞回注入上下文）→ 模型推理作答 → 推理后 **Record / Consolidate**（把短期对话提炼存入长期记忆）。写入常在会话结束或触发点批量执行。
- **上下文工程三策略（Anthropic）**：**压缩 Compaction**（满窗时摘要重启，保连续性但有损）、**笔记 Note-taking**（把进度写到窗口外文件如 NOTES.md，持久且人类可读）、**子代理 Sub-agent**（隔离重活，只回报浓缩摘要）。按任务类型选，而非全用。

## Key Quotes

> 「**「无状态」是问题，「记忆」是解：让信息能跨一次推理、跨一个会话、甚至跨多个会话存活。**记忆不在模型里，而在系统给它搭的「能存能取」的容器里。」

> 「**记忆按两条轴分类：存哪里（参数量/文本量）× 存多久（短期/长期）。**认知科学的分类法（工作、情景、语义、程序记忆）被工程界直接借用，作为架构清单。」

> 「**记忆系统靠一对读写回路运转：推理前 Retrieve，推理后 Record。**上下文窗口装不下时，还要靠上下文工程来压缩。」

> 「Compaction 把接近上限的对话压缩成高保真摘要（保留架构决策、未决问题）再续跑，是最直接的长期连贯手段。」——自测第 6 题解析

## 五条铁律

1. **先问「这条信息要不要跨会话活」，再决定放哪。**放错层是记忆设计最常见的失误。（记忆分类学）
2. **上下文窗口是稀缺资源，不是无限缓冲。**工作记忆里每个 token 都在挤占推理。（Anthropic）
3. **写入要提炼，读取要按相关性筛**——不要照搬原始记录。巩固太激进存噪音，太保守丢信息。（Mem0 类方案）
4. **长期记忆要分清读取范围，防止跨项目串味。**语义记忆按用户、项目、工具分域，检索时带 scope 约束。（Anthropic Managed Agents）
5. **持久记忆要防「陈腐」与「冲突」。**没有显式的刷新/冲突规则，旧的错记忆会挤掉新的对信息——即上下文污染。

## WorkBuddy 三层记忆（手册 Part B）

| 层级 | 写入方 | 读取时机 | 路径 |
|---|---|---|---|
| **L1 云端记忆** | 服务端自动（不可控） | 每次会话开场注入 | `~/.workbuddy/memory/…_memory.md` |
| **L2 用户级本地** | 主动请求「长期记住」 | 需要非项目规则时回查 | `~/.workbuddy/MEMORY.md` |
| **L3 项目级工作区** | 完成任务后追加（日志只增） | 同项目恢复上下文时回查 | `.workbuddy/memory/MEMORY.md` + `YYYY-MM-DD.md` |

作用域由外到内收窄、写入由系统自动到用户显式。L1 只读不可改写（服务端画像）。

## Connections

- [[AgentMemory]] —— 本手册的**主概念页**。
- [[MemoryTaxonomy]] —— 分类学主体：七类记忆与两条分类轴。
- [[ContextEngineering]] —— 三策略：压缩 / 笔记 / 子代理。
- [[WorkBuddyMemory]] —— Part B 的三层落地。
- [[RetrieveRecordLoop]] —— 读写回路（Retrieve / Record）。
- [[Anthropic]]、[[WorkBuddy]] —— 来源方与本机形态参照。

## Contradictions

- **与 [[WorkBuddyMemory]] / `agent-memory-system-guide` 的关系**：两份手册对 WorkBuddy 三层的**结构描述一致**（云端 / 用户级 / 工作空间），但**侧重不同**——本手册走分类学与读写回路，另一份走三大范式与四步循环。属互补，非冲突。
- **⚠️ 来源口径存疑（需标注）**：本手册 Part B 的 WorkBuddy 细节（三层结构、作用域、只读性）与本机 system prompt 对记忆的定义**吻合**，可视为本机形态的真实描述。但手册 Part A 引用的 Anthropic Managed Agents（2026-04）一篇引自 `usewire.io` 的**第三方报道**而非官方文档——按本项目既定来源纪律（禁二手聚合、优先官方文档），该条应视为**待核实**。使用这部分结论时，优先回查 Anthropic 官方文档。

## 溯源（手册自带）

| # | 来源 | 性质 |
|---|---|---|
| 01 | Effective Context Engineering for AI Agents · Anthropic | 官方 · 上下文是有限资源 + 三策略 |
| 02 | Building Effective Agents · Anthropic（2024-12-19） | 官方 · 增强型 LLM = 检索 + 工具 + 记忆 |
| 03 | Agent Memory: Types & Techniques · Mastra | 工程博客 · 记忆分类学映射 |
| 04 | Anthropic Memory for Managed Agents（2026-04） | ⚠️ 第三方报道（usewire.io）· 待核实 |
| 05 | 记忆读写回路模式 · Mem0 类长期记忆组件 | 工程方案 · Record / Retrieve 流程 |
| 06 | WorkBuddy 会话定义 + 本机记忆文件 | 一手 · 本机 `~/.workbuddy/` 实测 |
