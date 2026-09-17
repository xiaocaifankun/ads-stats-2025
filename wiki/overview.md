---
title: "Overview"
type: synthesis
tags: [overview, synthesis]
sources: [agent-skills-guide, agent-guide, agent-memory-guide, agent-memory-system-guide]
last_updated: 2026-09-17
---

# Overview

*This page is maintained by the LLM. It is updated on every ingest to reflect the current synthesis across all sources.*

## 当前收录

四份来源手册，来自同一批教学材料，构成一条**从「技能」到「智能体」到「记忆」**的递进线：

| 来源 | 主题 | 方法 |
|---|---|---|
| [[agent-skills-guide]] | Agent Skills | 渐进式披露 |
| [[agent-guide]] | Agent 智能体 | 架构判据 + 运行循环 |
| [[agent-memory-guide]] | Agent 记忆系统 | 分类学 |
| [[agent-memory-system-guide]] | Agent 记忆系统 | 范式论 |

## 跨越四份来源的一条主线

**上下文窗口是稀缺资源，四份手册都在回答同一个问题的不同切面：什么该进窗口，什么该留在外面。**

- **[[AgentSkills]]**：把指令与脚本留在窗口外，只在元数据层常驻 ~100 tokens → [[ProgressiveDisclosure]]
- **[[Agent]]**：把推理过程外化成可观察的循环步骤，每步只取回必要的 observation → [[ReAct]]
- **[[AgentMemory]]**：把跨会话的信息留在窗口外的存储里，按需注入 → [[RetrieveRecordLoop]]
- **[[MemoryParadigms]]**：给出三种窗口外存储的管理方式（打分检索 / 分层换页 / 文件直读）

把它们放在一起看，得到一条**统一的判据链**：

```text
这条信息要不要跨会话活？
  否 → 留在工作记忆（当前上下文）
  是 → 放进窗口外存储，并决定：
         · 存哪（工作 / 语义 / 情景 / 程序 …）      ← 分类学
         · 怎么取回（打分 / 换页 / 按需读）          ← 范式论
         · 作用域多大（用户级 / 项目级 / 全局）      ← 作用域
```

## 三个反复出现的核心判断

1. **分界线在控制流，不在技术栈。** [[WorkflowVsAgent]]：是否用 LLM、是否接工具都不构成区分；下一步由代码写死还是模型决定，才是唯一判据。
2. **记忆是检索问题，不是存储问题。** [[AgentMemory]]：存了取不回等于没存；打分机制（新近度·重要性·相关性）决定记忆质量。
3. **必须会遗忘。** 从 [[MemoryStream]] 的反思、到 [[ContextEngineering]] 的 compaction、到 [[WorkBuddyMemory]] 的蒸馏——**只追加不压缩的系统，噪声迟早淹没信号**。

## 基础构件

[[EnhancedLLM]]（检索 · 工具 · 记忆）是贯穿各层的共同地基：[[WorkflowVsAgent]] 的两层、[[Agent]] 的循环、[[AgentSkills]] 的分发，都构建于其上。

## 落地样本

[[WorkBuddyMemory]] 是当前 wiki 中唯一的完整产品落地案例：云端 / 用户级 / 项目级三层作用域，直接印证 [[AgentMemory]] 第一铁律「作用域决定归属」（放错层就会「换个项目就失忆」）。

## 待解的矛盾与缺口

- **⚠️ 来源归属存疑**：两份记忆手册都涉及 WorkBuddy 三层记忆的具体规则（结构、字符预算、蒸馏周期）。根据本项目的核查记录，这些细节**并非出自官方文档**，而是本机运行形态；来源手册把其中一份标注为「WorkBuddy 官方文档」、另一份引用了腾讯云社区的第三方文章。**结论：事实可用（与本机运行规则一致），但归属需改为「本机形态」**，详见 [[agent-memory-guide]] 与 [[agent-memory-system-guide]] 的矛盾小节。
- **Manifest 的第三方报道**：`agent-memory-guide` 引用的 Anthropic Managed Agents（2026-04）一篇出自 `usewire.io` 而非官方文档，按本项目来源纪律应视为**待核实**。
- **缺口**：四份手册均为**概念教学材料**，缺少可直接运行的代码示例，也没有失败案例。若后续要补齐，优先补「一次完整的记忆写入 → 检索 → 注入」的可运行样例，以及上下文污染的真实排查记录。
