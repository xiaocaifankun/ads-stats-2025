---
title: "MemGPT"
type: concept
tags: [agent-memory, operating-systems, paging]
sources: [agent-memory-system-guide]
last_updated: 2026-09-17
---

# MemGPT

*MemGPT: Towards LLMs as Operating Systems* —— Packer et al., 2023, arXiv:2310.08560。

[[MemoryParadigms]] 中的第二种范式：**把 LLM 当操作系统来管理记忆**。核心类比是**虚拟内存**——内存不够，就在内存与磁盘之间倒腾。

## 分层结构

```text
主上下文（小而快 · 当前相关）
   ↕ 换入 / 换出
外部存储（大而慢 · 完整历史）
   ├─ 检索库（向量）
   └─ 归档库（原文）
```

| 层 | 特性 | 内容 |
|---|---|---|
| **主上下文** | 小而快 | 当前任务相关的部分 |
| **检索库** | 大而慢 | 向量化索引，供语义检索 |
| **归档库** | 大而慢 | **完整原文**（不是只存向量） |

## 关键点

- **管理方式的一般解**：不是「存不下就丢最旧的」，而是**在两层之间换页**——需要时换入，不需要时换出。丢弃是不可逆的，换页是可逆的。
- **归档库存原文**：常见误解是「外部存储只存向量」——MemGPT 的设计是向量库（检索用）与原文库（回取用）并存。
- 这条思路直接支撑 [[AgentMemory]] 的第二条铁律：**分层是唯一出路**。

## 与记忆流的分工

[[MemoryStream]] 解决「**该取哪条**」；MemGPT 解决「**装不下怎么办**」。两者正交，可叠加使用——这也是 [[MemoryParadigms]] 强调「三者不互斥」的原因。

## Connections

- [[MemoryParadigms]] —— 所属范式框架。
- [[AgentMemory]] —— 上行概念。
- [[MemoryStream]] —— 正交的另一范式。
- [[ContextEngineering]] —— 分页与压缩共同服务于「有限窗口」。

## 出处

[[agent-memory-system-guide]]（溯源第 02 条为原始论文）。
