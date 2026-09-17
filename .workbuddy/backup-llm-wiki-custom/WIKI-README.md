# LLM Wiki — 个人知识库

基于 **LLM Wiki** 模式（源自 Andrej Karpathy 的 [llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构想）：不做查询时的向量检索，而是在**收录时**就让 LLM 把原始素材编译成结构化、互链的 Markdown 知识库。

**Obsidian 是 IDE，LLM 是程序员，wiki 是代码库。**

## 三层架构

| 层 | 位置 | 谁写 | 谁读 | 内容 |
| --- | --- | --- | --- | --- |
| 原始素材 | `raw/` | 你 | LLM | 文章、论文、笔记、PDF、图片 |
| 知识库 | `wiki/` | LLM | 你 | 摘要、实体、概念、分析、交叉引用 |
| 规范 | `AGENTS.md` | 共同演进 | LLM | schema、workflows、约定 |

## 目录结构

```
.
├── AGENTS.md              # 操作手册 / schema（核心配置）
├── raw/                   # 原始素材（不可变，LLM 只读）
│   ├── sources/           #   素材文件（可按主题分子目录）
│   └── assets/            #   图片与附件
├── wiki/                  # LLM 生成并维护的知识库
│   ├── index.md           #   内容索引（查询入口）
│   ├── log.md             #   操作日志（只追加）
│   ├── overview.md        #   总览
│   ├── conventions.md     #   使用约定与偏好
│   ├── sources/           #   素材摘要页
│   ├── entities/          #   实体页（人物/组织/工具/项目）
│   ├── concepts/          #   概念页（理论/方法/模式）
│   ├── outputs/           #   查询产出（对比/综述/简报）
│   ├── maintenance/       #   lint 报告
│   └── indexes/           #   专用索引（可选）
├── templates/             # 页面模板（source/entity/concept/output）
├── scripts/               # 本地工具（无需 LLM）
└── docs/                  # 模式说明
```

## 三大操作

| 你说 | 它做 |
| --- | --- |
| 「收录这份素材」（先把文件放进 `raw/sources/`） | 读全文 → 写摘要页 → 更新相关实体/概念页 → 刷新 index → 记 log |
| 「XX 是什么？」 | 读 index 定位页面 → 综合带引用的答案 → 有价值的答案回写 `wiki/outputs/` |
| 「检查下知识库」 | 体检：矛盾、过时论断、孤儿页、缺链 → 报告写入 `wiki/maintenance/` |

一次 ingest 通常触及 10–15 个页面。

## 本地工具

```bash
python scripts/llm-wiki.py lint    # 健康检查：死链 / 孤儿页 / 缺 frontmatter
python scripts/llm-wiki.py stats   # 页面统计
```

## Obsidian 使用

把本目录作为 vault 打开（`Open folder as vault`）。左边与 agent 对话，右边实时看 wiki 页面生成；用 graph view 检查链接密度与孤儿页。建议装 Dataview（元数据看板）与 Marp（导出幻灯片）。

## 工作流建议

- 素材**一份一份收录**，人在环中把关重点。
- 每 2–3 天或每约 10 次 ingest 跑一次 lint。
- 每步改动都在 git 里留痕，写错了可一键回滚。

## 致谢

- Andrej Karpathy — LLM Wiki 原始理念
- Vannevar Bush — 1945 年 Memex 构想，个人知识管理思想源头
