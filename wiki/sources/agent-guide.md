---
title: "Agent 智能体 · 溯源式概念学习手册"
type: source
tags: [agent, react, workflow, anthropic, aima]
sources: []
date: 2026-09-03
source_file: raw/sources/agent-guide.html
last_updated: 2026-09-17
---

# Agent 智能体 · 溯源式概念学习手册

## Summary

一份溯源式单概念手册，把「Agent」从 1993 年的学术定义一路追到 LLM 时代的工程形态。手册最有用的一刀是把 **Workflow 与 Agent 的分界线**切得极窄——不看是否调用 LLM、不看是否接工具，只看**下一步由代码写死还是由模型动态决定**。运行层面则落到 ReAct 的「思考 → 行动 → 观察」循环，每一步都必须从环境取回 ground truth。

## Key Claims

- **经典定义（AIMA）**：Agent 是任何能通过**传感器感知环境、通过执行器作用于环境**的实体。AI 被定义为「理性智能体的研究与设计」。按这个抽象，恒温器与人类同样符合定义——与技术形态无关。
- **四属性（Wooldridge & Jennings 1995）**：自主、社会、反应、主动——**不含学习**。手册明确点名「学习能力」是最常见的误记。
- **理性 ≠ 全知**：理性智能体最大化的是**期望表现**，不要求预知实际结果。结果差，不能反推行动不理性。
- **Workflow 与 Agent 的唯一天界线**：控制流归属。下一步由预定义代码路径编排 = Workflow；由模型动态决定 = Agent。两者都可用 LLM、都可用工具。
- **三层构件关系**：增强型 LLM（检索 · 工具 · 记忆）是**基本构件**；Workflow 是写死的编排；Agent 是模型自主的循环。上层都构建于增强型 LLM 之上。
- **ReAct 循环**：接收任务 → 思考 Thought（推理·拆解·计划）→ 行动 Action（调用工具改变环境）→ 观察 Observation（环境反馈 = ground truth）→ 未达标则继续。
- **最简方案优先**：Agent 用延迟与成本换任务表现；很多场景优化单次 LLM 调用就已足够，甚至根本不需要智能体系统。
- **错误会复利**：不每步获取 ground truth，错误随步数累积放大。

## Key Quotes

> 「**Agent 的本质是一个闭环：感知环境、自主决策、采取行动。**LLM 时代的 Agent，则是「增强型 LLM」在循环中使用工具的系统。」

> 「**判断一个系统是不是 Agent，只看一件事：下一步做什么，由代码写死，还是模型动态决定。**这是 Workflow 与 Agent 之间唯一的架构分界线。」

> 「**Agent 的一生就是「思考 → 行动 → 观察」的循环**，每一步都以环境反馈作为 ground truth，直到满足停止条件。」

> 「ReAct 范式：推理与行动交替进行，优于只推理（易幻觉）或只行动（易盲目）。」——手册图注

## 五条铁律

1. **谁掌握控制流，谁就是 Agent。**（Anthropic 2024）
2. **理性不等于全知。**最大化期望表现，不要求预知实际结果。（AIMA）
3. **先找最简方案，再谈 Agent。**很多场景优化单次调用就够。（Anthropic 2024）
4. **每一步都要拿到 ground truth。**否则错误随步数复利累积。（Anthropic 2024）
5. **推理与行动必须交替。**只想不做会幻觉，只做不想会盲目。（ReAct 2022）

## Connections

- [[Agent]] —— 本手册的**主概念页**。
- [[WorkflowVsAgent]] —— 控制流归属这条分界线，是本手册最锋利的判据。
- [[ReAct]] —— 运行全程的循环范式，含 ground truth 铁律。
- [[EnhancedLLM]] —— 增强型 LLM（检索 · 工具 · 记忆），Agent 与 Workflow 共同的地基。
- [[Anthropic]] —— 《Building Effective Agents》的作者方，本手册工程侧结论的主要出处。

## Contradictions

无直接冲突。但需注意一处**口径差异**：AIMA 的「智能体」是包罗万象的抽象（恒温器也算），而 Anthropic 的「Agent」特指模型自主控制流的循环系统。同一词在两个语境下外延不同，引用时应标明出处。

## 溯源（手册自带）

| # | 来源 | 贡献 |
|---|---|---|
| 01 | *Artificial Intelligence: A Modern Approach* · Russell & Norvig | 传感器/执行器定义、理性智能体、PEAS 框架 |
| 02 | *Agent-Oriented Programming* · Yoav Shoham（1993）· DOI 10.1016/0004-3702(93)90034-9 | Agent 状态由信念、能力、选择、承诺等心智成分构成 |
| 03 | *Intelligent Agents: Theory and Practice* · Wooldridge & Jennings（1995）· DOI 10.1017/S0269888900008122 | 四属性操作性定义 |
| 04 | *ReAct: Synergizing Reasoning and Acting in Language Models* · Yao et al. · arXiv:2210.03629 | 推理与行动交替；ALFWorld +34% / WebShop +10% 绝对优势 |
| 05 | *Building Effective Agents* · Anthropic（Erik Schluntz & Barry Zhang, 2024-12-19） | Workflow/Agent 架构区分；增强型 LLM；最简方案原则 |
