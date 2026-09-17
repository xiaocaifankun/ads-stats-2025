# LLM Wiki 模式说明

来源：Andrej Karpathy 于 2026-04-04 发布的 GitHub Gist [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

## 核心思想

传统 RAG 是 **JIT（即时编译）**：查询时才去向量库捞碎片，LLM 每次都从零"重新发现"知识，没有积累，没有复利。跨 5 篇论文综合一个答案？它每次都要重新拼一遍。

LLM Wiki 是 **AOT（提前编译）**：收录时就把素材编译成结构化 wiki 页面，查询时直接读已经凝练好的全局摘要与交叉链接。

> 关键区别：**wiki 是一个持久、可复利的产物。** 交叉引用已经建好，矛盾已经标记，综述已经反映了读过的一切。

## 三层解耦

1. **Raw Sources** — 不可变事实来源，LLM 只读不改（杜绝幻觉污染）。
2. **The Wiki** — LLM 完全拥有的 Markdown 目录，选 Markdown 是因为 LLM 擅长处理文本，且配合 Obsidian `[[双向链接]]` 天然形成知识图谱。
3. **The Schema** — 自然语言配置文件（`AGENTS.md`），相当于 agent 的"潜意识与操作手册"。人机共同迭代，防止知识库发散崩溃。

## 三个闭环

| 操作 | 类比 | 做什么 |
| --- | --- | --- |
| **Ingest** | 吸收 | 读素材 → 提炼 → 交叉引用 → 更新 10–15 个页面 → 记日志 → 标记矛盾 |
| **Query** | 查询 | 读 index 定位 → 综合带引用的答案 → **好答案回写进 wiki** |
| **Lint** | 自检 | 像跑测试一样扫死链、矛盾、孤儿页、过时信息、缺失引用 |

## 为什么有效

Karpathy 亲测：**在中等规模（约 100 个来源、数百页）下出人意料地有效**，并且避免了基于向量化的 RAG 基础设施需求。

社区实测：把 raw 编译成 wiki 后，同等查询的 token 消耗可大幅下降（有报告称 71.5×），因为不再需要每次塞入原始碎片。

## 开源实现参考

- [DavidPFussell/llm-wiki](https://github.com/DavidPFussell/llm-wiki) — 简洁的 starter repo，本库的 `AGENTS.md` 主要参照它
- [nvk/llm-wiki](https://github.com/nvk/llm-wiki) — 功能最全，多智能体研究编排、多种 ingest 适配器
- [jnystrom14/llm-wiki](https://github.com/jnystrom14/llm-wiki) — 带完整 Python 工具链（ingest/normalize/extract/integrate/query/lint）
