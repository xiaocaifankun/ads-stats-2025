---
title: Overview
type: output
status: active
created: 2026-09-10
updated: 2026-09-10
tags:
  - meta
  - overview
---

# Overview

知识库整体图景。由 agent 在每次 ingest 后视需要更新。

## 这是什么

一个个人知识库，采用 **LLM Wiki** 模式（源自 Andrej Karpathy 2026 年 4 月提出的 llm-wiki 构想）：

- 不做查询时的向量检索（RAG），而是在**收录时**就把原始素材编译成结构化、互链的 Markdown 页面。
- wiki 由 LLM 编写和维护，人只负责策展素材和提问。
- 知识持续复利增长——每份新素材、每个好问题都让整个网络更丰富。

类比：**Obsidian 是 IDE，LLM 是程序员，wiki 是代码库。**

## 三层架构

| 层 | 位置 | 谁写 | 谁读 | 内容 |
| --- | --- | --- | --- | --- |
| 原始素材 | `raw/` | 人 | LLM | 文章、论文、笔记、PDF、图片 |
| 知识库 | `wiki/` | LLM | 人 | 摘要、实体、概念、分析、交叉引用 |
| 规范 | `AGENTS.md` | 共同演进 | LLM | schema、workflows、约定 |

## 三大操作

- **Ingest（收录）** — 丢一份素材进 `raw/`，agent 读全文、写摘要、更新相关实体/概念页、刷新索引、记日志。单次可能触及 10–15 个页面。
- **Query（查询）** — 基于已编译的 wiki 提问，答案带引用；有价值的答案回写进 `wiki/outputs/`，让探索也复利。
- **Lint（质检）** — 定期通读全文，找出矛盾、过时论断、孤儿页、缺失交叉引用，写报告到 `wiki/maintenance/`。

## 当前研究重心

_（待首次收录素材后填写）_

## 待探索

_（agent 会在 lint 时建议新问题与新素材方向）_
