---
title: "ProgressiveDisclosure"
type: concept
tags: [context-engineering, agent-skills]
sources: [agent-skills-guide]
last_updated: 2026-09-17
---

# ProgressiveDisclosure

渐进式披露：**不是一次全读，而是像翻书**——先看封面简介，再翻目录，最后才读需要的那一章。[[AgentSkills]] 的核心加载机制，也是「装几百个 Skill 也不撑爆上下文」的原因。

## 三层加载

| 层 | 内容 | 体量 | 加载时机 |
|---|---|---|---|
| **L1 元数据** | `name` + `description` | ~100 tokens | **启动即加载，始终在场**（写入系统提示） |
| **L2 正文** | `SKILL.md` | 建议 < 500 行 | 任务匹配时才读取 |
| **L3 资源** | `references/` `scripts/` `assets/` | 不限 | 按需读取，**用不到 = 0 token** |

关键在最下层：**脚本在磁盘上执行，源码从不进入上下文**，只有运行输出被读回。

## 一次任务的全程（以「帮我填这份 PDF 表单」为例）

```text
① 启动   只有元数据在场
② 触发   匹配成功，读入 SKILL.md 正文
③ 深入   正文指向 forms.md，按需再读
④ 执行   脚本在磁盘运行，仅输出进入上下文
```

## 设计含义

- **成本与规模解耦**：Skill 库可以无限增长，常驻成本只随「数量 × 100 tokens」线性上升，不随内容体量上升。
- **元数据即接口**：`description` 的质量直接决定触发准确率——这是 [[AgentSkills]] 把「写清做什么 + 何时用」列为第一铁律的原因。
- 同属「把重内容挪出上下文」家族，与 [[ContextEngineering]] 的子代理隔离思路相通。

## Connections

- [[AgentSkills]] —— 承载该机制的格式。
- [[ContextEngineering]] —— 更广义的上下文资源管理策略。
- [[Anthropic]] —— 提出方。

## 出处

[[agent-skills-guide]]。
