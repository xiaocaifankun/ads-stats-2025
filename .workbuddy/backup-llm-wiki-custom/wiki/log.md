# Wiki Log

只追加、按时间顺序的操作日志。每条以固定前缀开头，便于解析：

```bash
grep "^## \[" wiki/log.md | tail -5
```

记录类型：`ingest` / `query` / `lint` / `maintenance`

---

## [2026-09-10] maintenance | 初始化知识库

- 按 LLM Wiki 模式（Karpathy llm-wiki）建立三层架构。
- 创建 `raw/`（sources + assets）、`wiki/`（sources/entities/concepts/outputs/maintenance/indexes）、`templates/`、`scripts/`、`docs/`。
- 写入 `AGENTS.md` schema、`wiki/index.md` 索引、`wiki/overview.md` 总览、`wiki/conventions.md` 约定。
- 无素材收录。等待首次 ingest。
