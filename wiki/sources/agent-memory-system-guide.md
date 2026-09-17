---
title: "Agent 记忆系统 · 溯源学习手册（单概念单页）"
type: source
tags: [agent-memory, generative-agents, memgpt, memory-tool, workbuddy]
sources: []
date: 2026-09-09
source_file: raw/sources/agent-memory-system-guide.html
last_updated: 2026-09-17
---

# Agent 记忆系统 · 溯源学习手册（单概念单页）

## Summary

一份单概念单页手册，与 `agent-memory-guide` 同题异构：它不走分类学，而走**范式路线**——把业界收敛出的三种记忆范式摆在一起对照（记忆流 / 分层换页 / 文件即记忆），再统一到**四步循环**（写入 → 蒸馏 → 检索 → 注入），最后落到 WorkBuddy 的三层作用域。核心命题一句话：**记忆本质上是检索问题，不是存储问题**。

## Key Claims

- **核心命题**：**存了取不回，等于没存。**记忆 = 外部存储 + 取回机制；LLM 每次调用都无状态，所谓「记住」全靠系统在 prompt 里重新喂入。
- **三大通用范式**：
  - **记忆流（Generative Agents, 2023）** —— 全部自然语言、追加式存储，检索打分 `score = 新近度 + 重要性 + 相关性`，只取回 top 项。新近度用指数衰减，重要性由 LLM 打分，相关性用向量余弦相似，归一化后求和。
  - **分层换页（MemGPT, 2023）** —— OS 虚拟内存思想：主上下文（小而快、当前相关）↔ 外部存储（大而慢、完整历史）在两者间换入换出。外部含**检索库（向量）+ 归档库（原文）**。
  - **文件即记忆（Anthropic Memory Tool, 2025)** —— `/memories/` 目录、客户端托管，`user_profile.md` / `project_notes.md` 等普通文件，**用时才读**；读写都是文件操作，**人可直接审计**。
  - 三者**不互斥**：现代产品通常混用——文件做载体，打分做检索，分层做容量管理。
- **四步循环**：① 写入（追加原始记录，append-only）→ ② 蒸馏（压缩提炼要点：反思 / 摘要 / 归档）→ ③ 检索（按打分取 top 项）→ ④ 注入（放进当前 prompt）。
- **蒸馏是「聪明的遗忘」**：Generative Agents 用反思把琐碎观察合成高层洞见，Anthropic 用 compaction 把长对话压成摘要——只存不用，迟早淹没在噪声里。
- **WorkBuddy 三层作用域**：① 云端记忆（服务端维护、AI 只读、跨设备；含 `<memory>` 画像注入 + `conversation_search` 历史检索）；② 用户级本地 `~/.workbuddy/`（跨项目是、跨设备否；`MEMORY.md` + `SOUL/IDENTITY/USER.md` 身份文件）；③ 工作空间 `项目/.workbuddy/memory/`（仅本项目、跨设备否；`YYYY-MM-DD.md` 日志只追加 + `MEMORY.md` 策展笔记 + 30 天蒸馏）。
- **检索策略按层分化**：云端靠服务端排序，本地靠「会话启动注入 + 按需读文件」。**写入则克制**——明确要求「记住」才落盘。

## Key Quotes

> 「**把经验存到上下文窗口之外，并在需要时精准取回的机制。**一句话：记忆本质上是**检索问题**，不是存储问题——存了取不回，等于没存。」

> 「**LLM 天生失忆：参数里没有你的对话，上下文窗口装不下你的历史。**记忆系统的使命，就是让每次会话结束时经验不蒸发，下一次按需取回。」

> 「三者不互斥：现代产品通常混用——文件做载体，打分做检索，分层做容量管理。」

> 「**蒸馏是「聪明的遗忘」**……只存不用，迟早淹没在噪声里。」

## 五条铁律

1. **记忆是检索问题，不是存储问题**——检索打分（新近度·重要性·相关性）决定记忆质量。
2. **分层是唯一出路**——小而快的上下文 + 大而慢的外部存储，在两者之间换入换出。
3. **必须会遗忘**——追加式日志必须配蒸馏/压缩，否则旧记忆的噪声淹没新任务的信号。
4. **作用域决定归属**——用户偏好放用户级，项目约定放工作空间级，长期画像归服务端；放错层就会「换个项目就失忆」。
5. **显式记忆优于静默记忆**——明确说「记住」才写入：可控、可审计、可清理；静默自学习容易记住错的且删不掉。

## Connections

- [[AgentMemory]] —— 本手册的**主概念页**（与 `agent-memory-guide` 共用）。
- [[MemoryParadigms]] —— 三大范式对照（记忆流 / 分层换页 / 文件即记忆）。
- [[MemoryStream]] —— Generative Agents 的记忆流与三因子打分。
- [[MemGPT]] —— OS 式分层换页。
- [[WorkBuddyMemory]] —— 三层作用域落地。
- [[WorkBuddy]] —— 本机形态参照物。

## Contradictions

- **与 [[AgentMemory]] / `agent-memory-guide` 互补而非冲突**：两份手册对 WorkBuddy 三层的**结构描述一致**（云端 / 用户级 / 工作空间，跨设备属性相同）。差异在方法：本手册用范式与循环，另一份用分类学与读写回路。
- **⚠️ 溯源标注与实际口径不符（重要）**：本手册把 WorkBuddy 三层记忆、**30 天蒸馏**、字符上限等细节标注为出自「WorkBuddy 官方文档（Quickstart）」。据本项目 2026-09-10 的核查记录，**官方文档并无「三层记忆 + 字符上限 + 30 天蒸馏」的表述**，该说法最初来自二手聚合页；但同时，这些规则**与本机 system prompt 对记忆的实际定义一致**，属真实运行的本机形态。结论：**事实可用，归属应改为「本机形态」，不宜标为「官方文档」**。
- **第三方来源**：溯源第 6 条引用 `cloud.tencent.com/developer/article/2671974`（第三方交叉验证）。按本项目来源纪律（禁二手聚合、优先官方文档），此条**仅作旁证**，不作为独立依据。

## 溯源（手册自带）

| # | 来源 | 性质 |
|---|---|---|
| 01 | Generative Agents: Interactive Simulacra of Human Behavior · Park et al., UIST 2023 · arXiv:2304.03442 | 一手论文 · 记忆流 + 三因子打分 + 反思 |
| 02 | MemGPT: Towards LLMs as Operating Systems · Packer et al., 2023 · arXiv:2310.08560 | 一手论文 · OS 式分层与虚拟上下文管理 |
| 03 | Anthropic · Memory Tool 官方文档 | 官方 · `/memories` 与 just-in-time 读取 |
| 04 | Anthropic · Context Engineering Cookbook | 官方 · compaction / tool clearing / memory 三策略 |
| 05 | WorkBuddy 官方文档（Quickstart） | ⚠️ 归属存疑，实际内容更接近本机形态 |
| 06 | WorkBuddy 记忆架构深读 · 腾讯云开发者社区 | ⚠️ 第三方旁证，仅作交叉验证 |
