---
title: "MemoryParadigms"
type: concept
tags: [agent-memory, generative-agents, memgpt, anthropic]
sources: [agent-memory-system-guide]
last_updated: 2026-09-17
---

# MemoryParadigms

业界针对「记忆」收敛出的**三种通用范式**。三者不互斥——现代产品通常混用：**文件做载体，打分做检索，分层做容量管理。**

| 范式 | 类比 | 代表 | 机制 |
|---|---|---|---|
| **记忆流** | 日记本 + 打分检索 | [[MemoryStream]] · Generative Agents（2023） | 全部自然语言、追加式存储，`score = 新近度 + 重要性 + 相关性`，取 top 项 |
| **分层换页** | 操作系统虚拟内存 | [[MemGPT]]（2023） | 主上下文（小而快）↔ 外部存储（大而慢）换入换出；外部含检索库（向量）+ 归档库（原文） |
| **文件即记忆** | 文件柜 | Anthropic Memory Tool（2025） | `/memories/` 目录、客户端托管，用时才读，读写都是文件操作 |

## 一脉相承的三条共性

```text
存储在外 → 检索在后 → 注入靠前
```

1. **存储在外**：都不把历史留在上下文窗口里。
2. **检索在后**：都需要一个「判断什么相关」的机制（打分 / 分页 / 按需读）。
3. **注入靠前**：都在推理**之前**把取回的内容放进 prompt。

## 各范式的独特贡献

- **记忆流**：给出可计算的相关性打分公式（三因子），把「取什么」变成可调参数。
- **分层换页**：给出**容量管理**的一般解——不是「存不下就丢」，而是「在两层之间换页」。
- **文件即记忆**：给出**可审计性**——人可以直接打开文件查看与编辑记忆，无需专门工具。

## Connections

- [[AgentMemory]] —— 上行概念。
- [[MemoryStream]] —— 范式一。
- [[MemGPT]] —— 范式二。
- [[WorkBuddyMemory]] —— 采用「文件即记忆」为主、打分检索为辅的混合形态。
- [[Anthropic]] —— 范式三的提出方。

## 出处

[[agent-memory-system-guide]]（核心设计章节与图 2）。
