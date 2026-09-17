---
title: "Agent"
type: concept
tags: [agent, aima, architecture]
sources: [agent-guide, agent-skills-guide, agent-memory-guide]
last_updated: 2026-09-17
---

# Agent

「Agent」在本 wiki 中有一个**双口径**问题，两个口径的外延不同：

| 口径 | 定义 | 出处 |
|---|---|---|
| **经典（AIMA）** | 任何能通过**传感器感知环境、通过执行器作用于环境**的实体 | Russell & Norvig |
| **现代（Anthropic）** | **动态决定自身流程与工具使用**的系统；通常只是「循环中使用工具的 LLM」 | 《Building Effective Agents》 |

按 AIMA 的抽象，**恒温器与人类同样是 Agent**——定义只看「感知 + 行动」闭环，与技术形态无关。按 Anthropic 的口径则窄得多，能自主控制流才算。引用时必须标明出处。

## 学术脉络

- **1993 · Shoham**：Agent-Oriented Programming 首次给 Agent 赋予**心智状态**——状态由信念、能力、选择、承诺等心智成分构成；AOP 可视为面向对象编程的特化。
- **1995 · Wooldridge & Jennings**：被引用最多的操作性定义——「弱概念」下智能体具备**自主、社会、反应、主动**四属性。**注意：不含学习能力**，这是最常见的误记。
- **AIMA**：理性智能体（rational agent）被定义为最大化**期望表现**者，**不等于全知**——结果差不能反推行动不理性。

## 组成（现代形态）

- **闭环**：感知环境 → 自主决策 → 采取行动。
- **构件关系**（自下而上）：[[EnhancedLLM]]（检索·工具·记忆）是基本构件 → Workflow 是写死的编排 → Agent 是模型自主的循环。判据见 [[WorkflowVsAgent]]。
- **运行循环**：[[ReAct]] 的「思考 → 行动 → 观察」，每步以环境反馈为 ground truth。
- **记忆**：Agent 的连续性来自 [[AgentMemory]]，而非模型本身。

## Connections

- [[WorkflowVsAgent]] —— Agent 与 Workflow 的分界线。
- [[ReAct]] —— Agent 的运行循环范式。
- [[EnhancedLLM]] —— Agent 的基本构件。
- [[AgentSkills]] —— 给 Agent 补充程序性知识的格式。
- [[AgentMemory]] —— 让无状态模型获得连续性的基础设施。

## 出处

[[agent-guide]]（含 AIMA / Shoham 1993 / Wooldridge & Jennings 1995 / ReAct / Anthropic 五条一手溯源）。
