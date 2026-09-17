---
title: "ReAct"
type: concept
tags: [agent, reasoning, acting]
sources: [agent-guide]
last_updated: 2026-09-17
---

# ReAct

*Synergizing Reasoning and Acting in Language Models* —— Yao et al.，2022（ICLR 2023），arXiv:2210.03629。

让 LLM 以**交替**方式生成推理轨迹与行动：推理帮助追踪与修正计划，行动帮助从外部环境获取信息。核心主张：**推理与行动交替进行，优于只推理（易幻觉）或只行动（易盲目）。**

## 循环

```text
01 接收任务   目标与约束进入
02 思考 Thought   推理 · 拆解 · 计划
03 行动 Action    调用工具改变环境
04 观察 Observation   环境反馈 · ground truth
   ↳ 未达标 → 回到 02
   ↳ 满足停止条件 → 结束
```

## 关键收益

- **Ground truth 闭环**：每一步都从环境取回真实反馈，错误不会静默累积——这是「错误会复利」问题的解法。
- **可追踪**：推理轨迹让计划可被观察与修正，而非黑箱跳跃。
- **实验数据**：在 ALFWorld 上以 **34% 绝对优势**、WebShop 上以 **10% 绝对优势**超过已有基线。

## 与本 wiki 其他概念的关系

- 它是 [[Agent]] 的**运行全程**——「Agent 的一生就是思考 → 行动 → 观察的循环」。
- 它提供的 Observation 环节，正是 [[WorkflowVsAgent]] 中「每一步都要拿到 ground truth」这条原则的机制来源。
- 与 [[EnhancedLLM]] 配合：行动环节通常就是调用工具与检索。

## Connections

- [[Agent]] —— ReAct 是其运行范式。
- [[WorkflowVsAgent]] —— ground truth 原则的具体落点。
- [[EnhancedLLM]] —— 行动所依赖的构件。

## 出处

[[agent-guide]]（溯源第 04 条为原始论文）。
