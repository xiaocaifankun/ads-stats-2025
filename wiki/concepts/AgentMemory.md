---
title: "AgentMemory"
type: concept
tags: [agent-memory, core]
sources: [agent-memory-guide, agent-memory-system-guide, agent-guide]
last_updated: 2026-09-17
---

# AgentMemory

把经验存到上下文窗口之外、并在需要时精准取回的机制。**核心命题：记忆本质上是检索问题，不是存储问题——存了取不回，等于没存。**

大语言模型**天生无状态**：每次调用都从零开始，参数里没有你的对话，上下文窗口装不下你的历史。所谓「记住」，全靠系统在 prompt 里重新喂入内容。记忆系统 = **外部存储 + 取回机制**。

## 两条切入路径（本 wiki 有两份互补来源）

| 路径 | 组织方式 | 来源页 |
|---|---|---|
| **分类学** | 按「存哪里 × 存多久」切成工作 / 语义 / 情景 / 程序 / 检索 / 参数 / 前瞻记忆 | [[MemoryTaxonomy]] ← [[agent-memory-guide]] |
| **范式论** | 按业界收敛的三种实现范式对照：记忆流 / 分层换页 / 文件即记忆 | [[MemoryParadigms]] ← [[agent-memory-system-guide]] |

两条路径描述同一件事，可交叉印证。

## 运行回路

- **四步循环**：写入（append-only）→ 蒸馏（反思 / 摘要 / 归档）→ 检索（按打分取 top 项）→ 注入（放进当前 prompt）。
- **读写回路**：推理前 **Retrieve** 注入 → 推理作答 → 推理后 **Record** 提炼写回。详见 [[RetrieveRecordLoop]]。

## 五条铁律

1. **记忆是检索问题，不是存储问题。**
2. **分层是唯一出路**——小而快的上下文 + 大而慢的外部存储，在两者间换入换出。
3. **必须会遗忘**——追加式存储必须配蒸馏/压缩，否则旧记忆的噪声淹没新任务的信号。
4. **作用域决定归属**——放错层就会「换个项目就失忆」。
5. **显式记忆优于静默记忆**——可控、可审计、可清理。

## 落地样本

[[WorkBuddyMemory]]（三层作用域）是当前 wiki 中唯一的完整产品落地案例。

## Connections

- [[MemoryTaxonomy]] —— 分类学切入。
- [[MemoryParadigms]] —— 范式论切入。
- [[RetrieveRecordLoop]] —— 读写回路。
- [[ContextEngineering]] —— 窗口装不下时的压缩手段。
- [[WorkBuddyMemory]] —— 产品落地。
- [[EnhancedLLM]] —— 记忆是增强型 LLM 的三构件之一。

## 出处

[[agent-memory-guide]]、[[agent-memory-system-guide]]、[[agent-guide]]。
