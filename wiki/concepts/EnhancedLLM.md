---
title: "EnhancedLLM"
type: concept
tags: [agent, architecture, llm]
sources: [agent-guide, agent-memory-guide]
last_updated: 2026-09-17
---

# EnhancedLLM

增强型 LLM：在裸语言模型之外补上三样东西——**检索 · 工具 · 记忆**。

```text
记忆
检索   工具
   LLM（核心推理）
在循环中运行 · 直至停止条件
```

[[Anthropic]] 在《Building Effective Agents》(2024-12-19) 中把它定位为**所有智能体系统的基本构件**——无论是 [[WorkflowVsAgent]] 分界线下方的 Workflow，还是上方的 [[Agent]]，都构建于其上。

## 三个组件的分工

| 组件 | 解决的问题 | 对应概念 |
|---|---|---|
| **检索** | 参数里没有的知识，按需取回 | [[AgentMemory]] 的 Retrieve 环节 |
| **工具** | 模型无法直接作用于环境 | [[ReAct]] 的 Action 环节 |
| **记忆** | 无状态、跨会话失忆 | [[AgentMemory]] |

## 为什么这个定位重要

- 它把「记忆」从可选增强项提升为**基本构件**——与检索、工具同级，而非事后补丁。这也是为什么记忆系统值得单独成一门学问（见 [[AgentMemory]]）。
- 它划清了层次：模型本身只负责**核心推理**，其余能力外挂、可替换、可演进。

## Connections

- [[Agent]] —— 构件之上的自主循环层。
- [[WorkflowVsAgent]] —— 构件之上的写死编排层。
- [[AgentMemory]] —— 三组件中「记忆」的展开。
- [[ReAct]] —— 「在循环中运行」的具体形态。
- [[Anthropic]] —— 提出方。

## 出处

[[agent-guide]]（核心设计三层图的底层）、[[agent-memory-guide]]（溯源第 02 条）。
