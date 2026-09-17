---
title: "MemoryStream"
type: concept
tags: [agent-memory, generative-agents, retrieval]
sources: [agent-memory-system-guide]
last_updated: 2026-09-17
---

# MemoryStream

记忆流：[[MemoryParadigms]] 中的第一种范式，出自 **Generative Agents: Interactive Simulacra of Human Behavior**（Park et al., UIST 2023, arXiv:2304.03442）。

做法极简：**把所有经历以自然语言追加式地存成一条流**，检索时打分排序，只取回 top 项。

## 三因子检索打分

```text
score = 新近度 + 重要性 + 相关性
```

| 因子 | 计算方式 |
|---|---|
| **新近度** Recency | 指数衰减，越近越高 |
| **重要性** Importance | 由 LLM 打分 |
| **相关性** Relevance | 向量余弦相似度 |

三者归一化后求和，取最高分项注入上下文。

## 记忆条目类型

```text
观察 Observation   冰箱空了 / 去药房买药
反思 Reflection    「Klaus 热衷研究」← 由琐碎观察合成的高层洞见
```

**反思**是该范式的关键机制：不是所有记忆都等价——系统主动把低层观察**压缩合成为高层洞见**，减少后续检索的噪声。这就是 [[AgentMemory]] 第三铁律「必须会遗忘」的最早工程实现，也是 [[ContextEngineering]] 中 compaction 的思想源头。

## 特点

- **全部自然语言**：无结构、无 schema，人可读。
- **追加式 append-only**：写入简单，但必须有反思/蒸馏配套，否则无限膨胀。
- **检索驱动**：价值不在存储，在打分取回——印证「记忆是检索问题」。

## Connections

- [[MemoryParadigms]] —— 所属范式框架。
- [[AgentMemory]] —— 上行概念。
- [[MemGPT]] —— 另一范式的对照（分层换页）。
- [[ContextEngineering]] —— 反思/蒸馏与 compaction 同源。

## 出处

[[agent-memory-system-guide]]（溯源第 01 条为原始论文）。
