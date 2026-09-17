# ads-stats-2025 — 项目长期笔记

## 这是什么

一个仓库两种用途并存，互不干扰：

- **LLM Wiki 个人知识库**（顶层：`AGENTS.md` / `wiki/` / `raw/` / `tools/` / `graph/` / `.claude/`）
- **广告学《统计与数据分析》课程材料**（`slides/` / `notebooks/` / `datasets/` / `exercises/` / `notes/` / `README.md`）

知识库来自 `SamurAIGPT/llm-wiki-agent`（MIT）的整体克隆，已断开其 `.git`。原始说明保留在 `LLM-WIKI-README.md`（因为 `README.md` 被课程文档占用）。上一轮自制版备份在 `.workbuddy/backup-llm-wiki-custom/`。

## 工作流权威

**`AGENTS.md` 是 schema 与工作流的唯一权威**（`CLAUDE.md` / `GEMINI.md` 是同源变体）。五个 trigger：`ingest <file>` / `query: <q>` / `health` / `lint` / `build graph`。

编辑 wiki 时严格遵守：

- 页面 frontmatter 必含 `title` / `type` / `tags` / `sources` / `last_updated`；`type ∈ {source, entity, concept, synthesis}`
- 命名硬规则：来源页 `kebab-case.md`，实体与概念页 `TitleCase.md`
- `wiki/index.md` 每次 ingest 必须同步；`wiki/log.md` 只追加
- 跑 `health`（零 LLM，免费）在前，`lint`（有 LLM，耗 token）每 10–15 次 ingest 一次

## 本机环境适配（重要）

官方工具链有两处在本机不可用，已确定的替代路径：

| 官方路径 | 本机问题 | 替代 |
|---|---|---|
| `tools/file_to_md.py`（markitdown 多格式转换） | `markitdown` 未安装；`pip install` 经代理与清华源两次尝试均 SIGTERM 失败 | **`tools/html_to_md.py`**（自建，纯 stdlib，HTML→MD） |
| `tools/build_graph.py`（默认会语义推断） | 会调 `call_llm` + `litellm`（未装），且产生意外 API 调用 | **加 `--no-infer`**，只做确定性 wikilink 解析 |

`tools/html_to_md.py` 的三个关键点（改它之前先看）：

1. 手册的列表是 `<div class="rule">` 不是 `<li>` → 用「当前行 + 已完成行」缓冲模型，不能每片段 flush
2. 图的价值全在 `<svg><text>` 里 → 按 `y` 分组（阈值 6px）、行内按 `x` 排序，还原成 ```text 围栏
3. 自测题字段名跨文件不同（`o`/`opts`、`a`/`ans`、`e`/`why`、`lt`/`lv`），且是 `const` 声明 → 正则需兼容 `var|const|let` × `QUIZ|QS|QUESTIONS`

## 来源纪律（用户明确确立，不得违反）

1. **禁止**采信 ima（`ima.qq.com`）、各类文库（百度文库/豆丁/道客巴巴）、各类百科（百度百科/维基/MBA智库）、内容农场与 CSDN 洗稿文。
2. **优先官方文档站**与一手来源（论文 arXiv、官方博客）；检索时叠加 `site:docs.xxx.com` 限定。
3. **必须先抓取再引用**，不得凭模型记忆写来源。
4. 涉及本机实物时**必须实测**，并**明确区分「官方口径」与「本机形态」**，不得混为一谈。
5. wiki 页面遇到矛盾必须显式记录（写在 Contradictions 小节），不得静默取舍。

## 已知的口径陷阱（写 wiki 时注意）

- **WorkBuddy 三层记忆**（云端 / 用户级 / 工作空间）的结构与规则为**本机形态**，与本机 system prompt 的定义一致；但**官方文档并无「三层 + 字符上限 + 30 天蒸馏」的表述**。引用时必须标注为本机形态，不得写成「官方文档规定」。
- 同理，`agent-memory-guide` 引用的 Anthropic Managed Agents（2026-04）出自 `usewire.io` 第三方报道，属待核实。

## 已完成的 ingest

- **2026-09-17**：4 份 Agent 主题手册（skills / agent / memory×2）→ 4 source + 2 entity + 14 concept = 20 页。图谱 21 节点 / 87 边。health 全绿，断链 0。
