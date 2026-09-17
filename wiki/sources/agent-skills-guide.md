---
title: "Agent Skills · 学习手册"
type: source
tags: [agent-skills, progressive-disclosure, anthropic]
sources: []
date: 2026-09-03
source_file: raw/sources/agent-skills-guide.html
last_updated: 2026-09-17
---

# Agent Skills · 学习手册

## Summary

一份溯源式单概念手册，讲 Anthropic 于 2025-10-16 首发的 Agent Skills 机制：Skill 就是**一个目录 + 一份 `SKILL.md`**，靠 YAML 元数据声明「做什么 + 何时用」，靠渐进式披露把上下文占用压到最低。手册的落点是一个反直觉的结论——Skill 的威力不在于「装了多少指令」，而在于**绝大部分内容可以永远不进上下文**。2025-12-18 起该格式成为开放标准。

## Key Claims

- **最小结构极简**：Skill = 一个目录 + `SKILL.md`（YAML frontmatter + Markdown 正文），不需要服务器、不需要 API 密钥。
- **渐进式披露三层**，这是核心设计：
  - **L1 元数据**（`name` + `description`）约 100 tokens，**启动即写入系统提示、始终在场**；
  - **L2 正文**（`SKILL.md`）建议 **< 500 行**，任务匹配时才读；
  - **L3 资源**（`references/` `scripts/` `assets/`）按需读取，**用不到 = 0 token**。
- **脚本不占上下文**：Claude 在文件系统中直接执行脚本，源码从不进入上下文，只有**运行输出**被读回。这是「能用代码就交给脚本」的机制基础。
- **`description` 是唯一触发依据**：必须同时写清「做什么」和「何时用」。`Helps with documents` 是手册给出的反例。
- **引用只嵌套一层**：`SKILL.md` 直接链接到引用文件，不再层层转引。
- **安全面**：Skill 能指挥 agent 调用工具、执行代码，因此**恶意 Skill 可导致数据外泄**；只装可信来源，非装不可时逐文件审计。

## Key Quotes

> 「Skill 是**一个目录**，里面放着指令、脚本和资源——相当于**给新员工写的一份入职指南**。最小形态只需一个文件。」

> 「不是一次全读，而是**像翻书**：先看封面简介，再翻目录，最后才读需要的那一章。装几百个 Skill 也不撑爆上下文。」

> 「合格的 description 必须同时说明**做什么**和**何时触发**——它是 Agent 决定是否加载的唯一依据。」——自测第 4 题解析

> 「Skill 能指挥 agent 调用工具、执行代码。官方明确：只装可信来源；非装不可时，**逐文件审计**所有内容。」——自测第 6 题解析

## 五条铁律

1. `description` 写清「**做什么** + **何时用**」——它是唯一的触发依据。
2. 正文 **< 500 行**，细节拆到引用文件；引用只嵌套一层。
3. 只写模型**不知道**的上下文——通用知识无需复述。
4. 能用代码解决的，**交给脚本**——确定性操作比让模型逐字生成更可靠。
5. 只装**可信来源**的 Skill——装前审计全部文件。

## Connections

- [[AgentSkills]] —— 本手册的**主概念页**，Skill 的定义、结构与生命周期。
- [[ProgressiveDisclosure]] —— 渐进式披露三层机制，本手册的核心设计章节。
- [[Anthropic]] —— 概念首发方与开放标准推动者（2025-10-16 首发，2025-12-18 标准化）。
- [[Agent]] —— Skill 服务的对象；Skill 是给 Agent 补充「程序性知识」的载体。

## Contradictions

无。本手册是当前 wiki 中唯一涉及 Agent Skills 的来源，无可比对对象。

## 溯源（手册自带）

| # | 来源 | 性质 |
|---|---|---|
| 01 | Equipping agents for the real world with Agent Skills · Anthropic Engineering（2025-10-16） | 概念首发，手册主要依据 |
| 02 | Agent Skills 开放标准 · agentskills.io（2025-12-18） | 跨平台规范，GitHub Copilot / Cursor / Codex CLI 相继采纳 |
| 03 | Agent Skills Overview · platform.claude.com | 官方文档：结构、安全考量、各平台限制 |
| 04 | Skill 编写最佳实践 · docs.anthropic.com（中文版） | 「五条铁律」的出处 |
| 05 | anthropics/skills（GitHub） | 官方开源仓库，真实 SKILL.md 写法 |
