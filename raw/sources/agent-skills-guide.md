# Agent Skills

> 转换自 `agent-skills-guide.html`（`tools/html_to_md.py`）· 原 HTML 保留在同目录，作为不可变源。

学 习 手 册 · 溯 源 版
# Agent Skills

一个文件夹，把通用智能体变成专家。
Anthropic · 2025-10-16 首发 2025-12-18 成为开放标准 核心：SKILL.md + 渐进式披露
01
## 它是什么

Skill 是**一个目录**，里面放着指令、脚本和资源——相当于**给新员工写的一份入职指南**。最小形态只需一个文件。
pdf-skill/ ├─ SKILL.md必需 · 元数据 + 指令 ├─ forms.md可选 · 深度参考 ├─ scripts/可选 · 确定性代码 └─ assets/可选 · 模板资源
# SKILL.md 的开头必须是 YAML 元数据 --- name: pdf-processing description: 填写 PDF 表单… 当用户提到 PDF 或表单时使用 --- # 以下是 Markdown 指令正文 # Quick start … # 表单细则见 forms.md

▲ 一个真实形态的 Skill（Anthropic 官方 PDF 示例的简化）
02
## 渐进式披露 —— 核心设计

不是一次全读，而是**像翻书**：先看封面简介，再翻目录，最后才读需要的那一章。装几百个 Skill 也不撑爆上下文。

<!-- 图 -->

```text
L1   元数据 · name + description
~100 tokens   启动即加载 · 写入系统提示
L2   指令 · SKILL.md 正文
建议 < 500 行   任务匹配时才读取
L3   资源 · references / scripts / assets
按需读取 · 用不到 = 0 token
书的隐喻：封面简介 → 目录 → 指定章节
```

03
## 一次任务的全程

用户说「帮我填这份 PDF 表单」，上下文窗口这样变化：

<!-- 图 -->

```text
① 启动 只有元数据在场
系统提示   Skill 元数据   用户：「帮我填 PDF 表单」
② 触发 匹配成功，读入 SKILL.md 正文
+ SKILL.md
③ 深入 正文指向 forms.md，按需再读
正文   + forms
④ 执行 脚本在磁盘上运行，只有输出进入上下文
fill_form.py（磁盘）
执行
仅输出进入上下文：3 个字段
```

▲ 源自 Anthropic 工程博客的时序演示（简化重绘）
04
## 五条铁律

1
description 要写清「**做什么** + **何时用**」
它是唯一的触发依据。`Helps with documents` 是反例。
2
正文 **< 500 行**，细节拆到引用文件
引用只嵌套一层，直接由 SKILL.md 链接。
3
只写模型**不知道**的上下文
简洁是关键——通用知识无需复述。
4
能用代码解决的，**交给脚本**
确定性操作用代码，比让模型逐字生成更可靠。
5
只装**可信来源**的 Skill
Skill 能指挥 agent 调用工具——恶意 Skill 可导致数据外泄。装前审计全部文件。
05
## 原始出处 · 点击验证

[Equipping agents for the real world with Agent Skills 概念首发 · Anthropic Engineering · 2025-10-16（本手册的主要依据） anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
[Agent Skills 开放标准 跨平台规范 · 2025-12-18 发布，GitHub Copilot / Cursor / Codex CLI 等相继采纳 agentskills.io](https://agentskills.io)
[Agent Skills Overview 官方文档 · Skill 结构、安全考量与各平台限制 platform.claude.com/docs/en/agents-and-tools/agent-skills/overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
[Skill 编写最佳实践 官方文档 · 「五条铁律」的出处（中文版可直接读） docs.anthropic.com/zh-CN/docs/agents-and-tools/agent-skills/best-practices](https://docs.anthropic.com/zh-CN/docs/agents-and-tools/agent-skills/best-practices)
[anthropics/skills 官方开源仓库 · 可直接阅读真实的 SKILL.md 写法 github.com/anthropics/skills](https://github.com/anthropics/skills)
06
## 自测 · 难度递进

三级递进：基础（识别）→ 进阶（理解）→ 挑战（应用）。
本手册依据上述原始出处整理，生成于 2026-09-03。概念归属 [Anthropic](https://www.anthropic.com)。

## 自测题

> 提取自页面交互脚本，共 6 题。

### 第 1 题（基础 · 识别）

一个 Agent Skill 的最小组成是什么？
- A. 一个 API 密钥
- B. 一个包含 SKILL.md 的目录 ✅
- C. 一段系统提示词
- D. 一个 MCP 服务器

**解析**：Skill 的最小形态就是一个目录 + 一份 SKILL.md（开头为 YAML 元数据）。不需要服务器，也不需要密钥。

### 第 2 题（基础 · 识别）

渐进式披露的三层中，哪一层「始终」占据上下文？
- A. SKILL.md 正文
- B. 所有引用文件
- C. name + description 元数据 ✅
- D. scripts/ 里的脚本

**解析**：启动时只把每个 Skill 的元数据（约 100 tokens）写入系统提示；正文和资源都按需加载。

### 第 3 题（进阶 · 理解）

为什么 scripts/ 里的脚本不占用上下文窗口？
- A. 脚本会被自动压缩
- B. Claude 直接执行脚本，只有输出结果进入上下文 ✅
- C. 脚本在别的模型上运行
- D. 脚本不产生任何输出

**解析**：Claude 在文件系统中直接执行脚本，源代码从不进入上下文，只有运行输出被读回。

### 第 4 题（进阶 · 理解）

下面哪个 description 写得最合格？
- A. Helps with documents
- B. 处理文件的东西
- C. Extract text and tables from PDFs… 当用户提到 PDF 或表单时使用 ✅
- D. 一个强大的人工智能技能

**解析**：合格的 description 必须同时说明做什么和何时触发——它是 Agent 决定是否加载的唯一依据。

### 第 5 题（挑战 · 应用）

你的 SKILL.md 已 480 行，还要加入 300 行「表单填写细则」。最佳做法是？
- A. 直接追加，凑到 780 行
- B. 删掉旧内容腾出空间
- C. 把细则拆到单独文件（如 forms.md），在正文中按需引用 ✅
- D. 拆成两个互相独立的 Skill

**解析**：官方建议正文 &lt; 500 行。拆出的文件在用到时才被读取，不占常驻上下文——这正是渐进式披露的用法。

### 第 6 题（挑战 · 应用）

从网上下载一个陌生 Skill 并安装，最大的风险是？
- A. 占用磁盘空间
- B. 加载速度变慢
- C. 恶意指令诱导 agent 执行与声明用途不符的操作（如数据外泄） ✅
- D. 与其他 Skill 的 name 冲突

**解析**：Skill 能指挥 agent 调用工具、执行代码。官方明确：只装可信来源；非装不可时，逐文件审计所有内容。
