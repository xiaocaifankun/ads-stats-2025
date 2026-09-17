---
title: "ContextEngineering"
type: concept
tags: [context-engineering, anthropic, agent-memory]
sources: [agent-memory-guide, agent-memory-system-guide]
last_updated: 2026-09-17
---

# ContextEngineering

上下文工程：把**上下文窗口当作稀缺资源**来经营，而不是当作无限缓冲。

> 工作记忆里每个 token 都是挤占推理的 token。

[[Anthropic]] 在《Effective Context Engineering for AI Agents》中给出三条**不写坏上下文**的路径，按任务类型选，而非全用。

## 三策略

| 策略 | 做法 | 特性 |
|---|---|---|
| **压缩 Compaction** | 满窗时对对话做摘要，**保留架构决策与未决问题**，用摘要重启新窗口 | 保连续性 · 但摘要取舍有损 |
| **笔记 Note-taking** | Agent 主动把进度与关键信息写到窗口外文件（如 `NOTES.md`），下次再读回 | 持久 · 开销低 · 人类可读 |
| **子代理 Sub-agent** | 复杂探索交给专用子代理，它在自己的干净窗口里深挖，**只把浓缩摘要回报主代理** | 隔离 · 主窗保持干净 |

## 为什么必须有

1. **窗口是有限资源**——不管理就会被历史淹没。
2. **上下文污染**：旧的错记忆会挤掉新的对信息；只追加不压缩，噪声迟早淹没信号（与 [[AgentMemory]] 第三铁律「必须会遗忘」同源）。
3. **成本**：常驻 token 直接计费并拖慢推理。

## 与记忆系统的分工

- **记忆系统**负责「长期存什么、怎么取回」（[[AgentMemory]]）。
- **上下文工程**负责「取回来的东西怎么塞进有限的窗口」（本页）。
- Compaction 与记忆蒸馏是同一原理的两种表现：Generative Agents 用反思、Anthropic 用 compaction、[[WorkBuddyMemory]] 用定期蒸馏——都是**聪明的遗忘**。

## Connections

- [[AgentMemory]] —— 上游的存储与检索。
- [[ProgressiveDisclosure]] —— 同属「把重内容挪出上下文」家族（[[AgentSkills]] 的实现手段）。
- [[Anthropic]] —— 三策略的提出方。
- [[WorkBuddyMemory]] —— 蒸馏机制的产品化表现。

## 出处

[[agent-memory-guide]]（运行全程章节）、[[agent-memory-system-guide]]（溯源第 04 条《Context Engineering Cookbook》）。
