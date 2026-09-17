---
title: "AgentSkills"
type: concept
tags: [agent-skills, tooling, anthropic]
sources: [agent-skills-guide]
last_updated: 2026-09-17
---

# AgentSkills

给 Agent 补充**程序性知识**的封装格式：**一个目录 + 一份 `SKILL.md`**。最小形态只需一个文件，不需要服务器、不需要 API 密钥。由 [[Anthropic]] 于 2025-10-16 首发，2025-12-18 起成为开放标准（agentskills.io），GitHub Copilot / Cursor / Codex CLI 等相继采纳。

## 结构

```
skill-name/
├─ SKILL.md     必需 · YAML 元数据 + Markdown 指令
├─ forms.md     可选 · 深度参考
├─ scripts/     可选 · 确定性代码
└─ assets/      可选 · 模板资源
```

`SKILL.md` 开头必须是 YAML frontmatter，至少含 `name` 与 `description`：

```yaml
---
name: pdf-processing
description: 填写 PDF 表单…当用户提到 PDF 或表单时使用
---
```

## 设计要点

- **`description` 是唯一触发依据**：必须同时写清「做什么」+「何时用」。反例：`Helps with documents`。
- **正文建议 < 500 行**，细节拆到引用文件；**引用只嵌套一层**，直接由 `SKILL.md` 链接。
- **只写模型不知道的上下文**——通用知识无需复述。
- **能用代码就交给脚本**：脚本在文件系统中直接执行，源码不进上下文，只有运行输出被读回。
- **安全面**：Skill 能指挥 agent 调用工具、执行代码，**恶意 Skill 可导致数据外泄**；只装可信来源，非装不可时逐文件审计。

## 为什么这样设计

全部服务于一个目标：**让绝大部分内容可以永远不进上下文**。装几百个 Skill 也不撑爆窗口——这就是 [[ProgressiveDisclosure]] 的工程价值。

## Connections

- [[ProgressiveDisclosure]] —— 支撑 Skill 可扩展性的核心加载机制。
- [[Agent]] —— Skill 服务的对象；Skill 是 Agent 的程序性知识载体。
- [[Anthropic]] —— 格式的首发方与标准推动者。
- [[ContextEngineering]] —— 与「笔记 / 脚本外置」同属「把重内容挪出上下文」的思路。

## 出处

[[agent-skills-guide]]（含五条铁律与 5 条官方溯源链接）。
