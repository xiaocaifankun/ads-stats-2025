---
title: "Anthropic"
type: entity
tags: [company, llm, agent]
sources: [agent-skills-guide, agent-guide, agent-memory-guide, agent-memory-system-guide]
last_updated: 2026-09-17
---

# Anthropic

AI 公司，Claude 系列模型的开发方。在当前 wiki 的四份来源手册中，它是**唯一贯穿全部四份**的实体——Agent Skills、Agent 架构、记忆系统三条线的一手或主要出处都指向它。

## 在本 wiki 中的角色

| 线 | Anthropic 的产出 | 出处来源页 |
|---|---|---|
| Agent Skills | **Agent Skills 格式**（2025-10-16 首发；2025-12-18 成为开放标准 agentskills.io） | [[agent-skills-guide]] |
| Agent 架构 | 《**Building Effective Agents**》（Erik Schluntz & Barry Zhang, 2024-12-19）：Workflow / Agent 架构区分、增强型 LLM、「最简方案优先」原则 | [[agent-guide]] |
| 上下文工程 | 《**Effective Context Engineering for AI Agents**》：上下文是有限资源 + 压缩 / 笔记 / 子代理三策略 | [[agent-memory-guide]] |
| 记忆 | **Memory Tool**（`/memories/` 目录、文件即记忆、just-in-time 读取）、《Context Engineering Cookbook》、Managed Agents 记忆（2026-04） | [[agent-memory-system-guide]] |

## 关键贡献（本 wiki 范围内的提炼）

- **把「上下文」显式定义为稀缺资源**，并给出三条不写坏上下文的工程手段 → [[ContextEngineering]]
- **给 Agent 与 Workflow 划出唯一分界线**：控制流的归属 → [[WorkflowVsAgent]]
- **提出「增强型 LLM」= 检索 + 工具 + 记忆**，作为所有智能体系统的基本构件 → [[EnhancedLLM]]
- **开源 Agent Skills 格式**，把「程序性知识」做成可分发、可按需加载的目录 → [[AgentSkills]]

## Connections

- [[AgentSkills]] —— Anthropic 首发并推动标准化的技能格式。
- [[Agent]] —— 《Building Effective Agents》定义了 LLM 时代的 Agent 架构判据。
- [[AgentMemory]] —— Memory Tool 与 Context Engineering 的主要来源方。
- [[ProgressiveDisclosure]] —— Agent Skills 的核心加载机制。

## 备注

- 本 wiki 中 Anthropic 的结论**均可回溯到官方工程博客或官方文档**；唯 `agent-memory-guide` 引用的 Managed Agents（2026-04）一篇为**第三方报道**（usewire.io），已在来源页标注为待核实。
