# Wiki Log

Append-only chronological record of all operations.

Format: `## [YYYY-MM-DD] <operation> | <title>`

Parse recent entries: `grep "^## \[" wiki/log.md | tail -10`

---

## [2026-09-10] setup | 落地 SamurAIGPT/llm-wiki-agent

- 克隆 https://github.com/SamurAIGPT/llm-wiki-agent （MIT，3484 stars）并整体落到仓库根目录。
- 断开其自带 `.git`，作为普通文件并入 ads-stats-2025 仓库管理。
- 已就位：`CLAUDE.md`（Claude Code schema）、`AGENTS.md`（Codex/OpenCode）、`GEMINI.md`、`.claude/commands/`（4 个斜杠命令）、`tools/`（11 个 Python 脚本）、`wiki/`、`raw/`、`graph/`。
- 课程原 `README.md` 已从 git 恢复；仓库说明改名保留为 `LLM-WIKI-README.md`。
- 上一轮自建的自制知识库已备份至 `.workbuddy/backup-llm-wiki-custom/`。
- 验证：`tools/health.py` 全绿（0 空页 / 0 索引不同步 / 0 日志缺失）。
- 待装可选依赖：`networkx`（社群检测）、`litellm`（语义边推断）—— 均仅影响知识图谱增强，不影响 ingest/query/lint 主流程。

## [2026-09-10] graph | Knowledge graph rebuilt

1 nodes, 0 edges (0 extracted, 0 inferred).

## [2026-09-17] ingest | Agent Skills · 学习手册

- 源：`raw/sources/agent-skills-guide.html`（+ 自动转换的 `.md`）
- 产出页：`wiki/sources/agent-skills-guide.md`
- 涉及实体：[[Anthropic]]
- 涉及概念：[[AgentSkills]]、[[ProgressiveDisclosure]]、[[Agent]]
- 备注：首次 ingest，同时建立 `wiki/{sources,entities,concepts,syntheses}/` 四个子目录。

## [2026-09-17] ingest | Agent 智能体 · 溯源式概念学习手册

- 源：`raw/sources/agent-guide.html`（+ 自动转换的 `.md`）
- 产出页：`wiki/sources/agent-guide.md`
- 涉及实体：[[Anthropic]]
- 涉及概念：[[Agent]]、[[WorkflowVsAgent]]、[[ReAct]]、[[EnhancedLLM]]

## [2026-09-17] ingest | Agent 记忆系统 · 溯源式概念学习手册

- 源：`raw/sources/agent-memory-guide.html`（+ 自动转换的 `.md`）
- 产出页：`wiki/sources/agent-memory-guide.md`
- 涉及实体：[[Anthropic]]、[[WorkBuddy]]
- 涉及概念：[[AgentMemory]]、[[MemoryTaxonomy]]、[[ContextEngineering]]、[[RetrieveRecordLoop]]、[[WorkBuddyMemory]]
- ⚠️ 矛盾标注：该来源引用的 Anthropic Managed Agents（2026-04）一篇为第三方报道，已标记待核实。

## [2026-09-17] ingest | Agent 记忆系统 · 溯源学习手册（单概念单页）

- 源：`raw/sources/agent-memory-system-guide.html`（+ 自动转换的 `.md`）
- 产出页：`wiki/sources/agent-memory-system-guide.md`
- 涉及实体：[[WorkBuddy]]
- 涉及概念：[[AgentMemory]]、[[MemoryParadigms]]、[[MemoryStream]]、[[MemGPT]]、[[WorkBuddyMemory]]
- ⚠️ 矛盾标注：该来源把 WorkBuddy 三层记忆细节归为「官方文档」，据本项目核查归属存疑，已改为「本机形态」。

## [2026-09-17] report | 首次 ingest 批次小结

- 新增页面：4 个 source + 2 个 entity + 14 个 concept = 20 页。
- 新增工具：`tools/html_to_md.py`（stdlib HTML→Markdown 转换器，替代在本机不可用的 markitdown 路径）。
- `wiki/index.md`、`wiki/overview.md` 已按 4 份来源重写。

## [2026-09-17] graph | Knowledge graph rebuilt

21 nodes, 87 edges (87 extracted, 0 inferred). `--no-infer` 跳过语义推断，避免意外 LLM 调用。


## [2026-09-17] graph | Knowledge graph rebuilt

21 nodes, 87 edges (87 extracted, 0 inferred).
