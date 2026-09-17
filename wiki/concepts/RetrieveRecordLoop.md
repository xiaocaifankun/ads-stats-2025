---
title: "RetrieveRecordLoop"
type: concept
tags: [agent-memory, architecture]
sources: [agent-memory-guide]
last_updated: 2026-09-17
---

# RetrieveRecordLoop

记忆读写回路：记忆系统靠一对**方向相反**的操作运转——推理前把长期记忆捞回注入上下文（Retrieve），推理后把短期对话提炼存入长期记忆（Record / Consolidate）。

```text
提问 → 当前上下文（会话历史 · 系统提示）
  ① 检索 Retrieve · 拉回相关记忆  ──→  长期记忆（用户画像 · 经验 · 事件）
  ② 注入 ③ 推理作答  ←──
  得到回答
  ④ 巩固 Consolidate · 提炼并写入  ──→  长期记忆
```

## 四个环节

| 环节 | 时机 | 作用 |
|---|---|---|
| **① Retrieve** | 推理**前** | 从长期记忆里按 query 检索 top-k 相关条目 |
| **② 注入** | 推理前 | 把检索结果放进当前 prompt，成为上下文 |
| **③ 推理作答** | — | 模型结合注入的记忆生成回复 |
| **④ Record / Consolidate** | 推理**后** | LLM 抽取「事实 / 偏好 / 经验」并写入长期存储 |

写入常在**会话结束或触发点批量执行**，而非逐句落盘。

## 设计要点

- **写入要提炼，读取要按相关性筛**——不要照搬原始记录。
  - Record 不是存原始对话，而是 LLM 抽取事实与偏好；
  - Retrieve 不是全量回放，而是按 query 检索 top-k。
- **巩固太激进存噪音，太保守丢信息**——这是记忆质量的主要调节旋钮。
- 与四步循环（写入 → 蒸馏 → 检索 → 注入）的关系：**四步循环是稳态视角，读写回路是单次交互视角**，描述同一系统的两个切面。

## Connections

- [[AgentMemory]] —— 上行概念。
- [[MemoryTaxonomy]] —— 巩固即「工作 → 长期」的层间桥。
- [[WorkBuddyMemory]] —— 产品中的检索与写入策略按层分化（云端靠服务端排序，本地靠启动注入 + 按需读文件）。
- [[ContextEngineering]] —— 注入前的容量管理。

## 出处

[[agent-memory-guide]]（运行全程章节；工程出处为 Mem0 类长期记忆组件）。
