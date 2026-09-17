# Agent智能体

> 转换自 `agent-guide.html`（`tools/html_to_md.py`）· 原 HTML 保留在同目录，作为不可变源。

溯源式概念学习手册
# Agent智能体

任何能通过传感器感知环境、并通过执行器作用于环境的实体——而 AI 的任务，就是设计这样的**理性智能体**；在 LLM 时代，它指**动态决定自身流程与工具使用**的系统。
1993 · AOP 论文为 Agent 赋予心智状态 AIMA：AI 即理性智能体的研究与设计 Anthropic：Agent 通常只是循环中使用工具的 LLM
01
## 它是什么

**Agent 的本质是一个闭环：感知环境、自主决策、采取行动。**LLM 时代的 Agent，则是「增强型 LLM」在循环中使用工具的系统。

<!-- 图 -->

```text
经典定义 · AIMA
环境 Environment
任务 · 世界 · 其他智能体
智能体 Agent
感知 → 决策 → 行动
传感器 · 感知   执行器 · 行动
恒温器与人类同样符合此定义
现代形态 · Anthropic
记忆
检索   工具
LLM
核心推理
在循环中运行 · 直至停止条件
```

> 左：AIMA 的经典抽象——感知与行动的闭环；右：现代最小组成——检索、工具、记忆构成「增强型 LLM」。
02
## 核心设计

**判断一个系统是不是 Agent，只看一件事：下一步做什么，由代码写死，还是模型动态决定。**这是 Workflow 与 Agent 之间唯一的架构分界线。

<!-- 图 -->

```text
自主性 · 复杂度 递增
Agent 智能体
控制流由模型动态决定 · 循环直至停止条件
分界线：下一步由代码还是模型决定
Workflow 工作流
控制流写死在代码路径：提示链 · 路由 · 并行 · 编排 · 评估
以上两层均构建于其上
增强型 LLM
检索 · 工具 · 记忆 —— 所有智能体系统的基本构件
```

> 自下而上：增强型 LLM 是构件，Workflow 是写死的编排，Agent 是模型自主的循环。虚线即 Workflow 与 Agent 的分界线。
03
## 运行全程

**Agent 的一生就是「思考 → 行动 → 观察」的循环**，每一步都以环境反馈作为 ground truth，直到满足停止条件。

<!-- 图 -->

```text
未达标 · 继续循环
01
接收任务
目标与约束进入
02
思考 Thought
推理 · 拆解 · 计划
03
行动 Action
调用工具改变环境
04
观察 Observation
环境反馈 · ground truth
满足停止条件 · 结束
```

> ReAct 范式：推理与行动交替进行，优于只推理（易幻觉）或只行动（易盲目）。
04
## 铁律

- **谁掌握控制流，谁就是 Agent。** 下一步由代码写死是 Workflow；由模型自己决定才是 Agent——这是唯一的分界线。_Anthropic 2024_
- **理性不等于全知。** 理性智能体最大化的是「期望表现」，不要求预知实际结果——结果差，不代表不理性。_AIMA_
- **先找最简方案，再谈 Agent。** Agent 用延迟与成本换任务表现；很多场景优化单次 LLM 调用就已足够，甚至根本不需要智能体系统。_Anthropic 2024_
- **每一步都要拿到 ground truth。** 执行中必须从环境获取观察来评估进展，否则错误会随步数复利累积。_Anthropic 2024_
- **推理与行动必须交替。** 只想不做会幻觉，只做不想会盲目；ReAct 用实验证明交替优于任一单独。_ReAct 2022_
05
## 溯源

**本手册每个事实都出自以下五个一手来源**，点击即可验证。
01
### Artificial Intelligence: A Modern Approach · Russell & Norvig

智能体的教科书定义（传感器 / 执行器）、理性智能体、PEAS 框架；AI 被定义为「理性智能体的研究与设计」。首版 1995 年，第四版 2020 年，全球 135+ 国家采用。
[aima.cs.berkeley.edu](http://aima.cs.berkeley.edu/)
02
### Agent-Oriented Programming · Yoav Shoham（1993）

首次提出 AOP：Agent 的状态由信念、能力、选择、承诺等「心智成分」构成；AOP 可视为面向对象编程的特化。发表于 Artificial Intelligence 60(1): 51–92。
[doi.org/10.1016/0004-3702(93)90034-9](https://doi.org/10.1016/0004-3702(93)90034-9)
03
### Intelligent Agents: Theory and Practice · Wooldridge & Jennings（1995）

被引用最多的智能体操作性定义：「弱概念」下，智能体具备自主、社会、反应、主动四属性。发表于 The Knowledge Engineering Review 10(2)。
[doi.org/10.1017/S0269888900008122](https://doi.org/10.1017/S0269888900008122)
04
### ReAct: Synergizing Reasoning and Acting in Language Models · Yao et al.（2022, ICLR 2023）

让 LLM 以交替方式生成推理轨迹与行动：推理帮助追踪与修正计划，行动帮助从外部环境获取信息。在 ALFWorld / WebShop 上分别以 34% / 10% 的绝对优势超过已有基线。
[arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
05
### Building Effective Agents · Anthropic（Erik Schluntz & Barry Zhang, 2024-12-19）

Workflow 与 Agent 的架构区分（控制流归属）；增强型 LLM（检索 / 工具 / 记忆）；「找到可行的最简方案、只在必要时增加复杂度」原则。基于与数十个行业团队的合作实践。
[anthropic.com/engineering/building-effective-agents](https://www.anthropic.com/engineering/building-effective-agents)
06
## 自测

6 题 · 基础 / 进阶 / 挑战 三级递进 · 全部出自本手册内容
_/ 6_
重新自测
所有事实均可在 05 溯源中点击验证 · 溯源式概念学习手册

## 自测题

> 提取自页面交互脚本，共 6 题。

### 第 1 题（基础 · 识别）

「Agent」在 AIMA 教材中的定义核心是？
- A. 一个能调用外部工具的大语言模型
- B. 任何能通过传感器感知环境、并通过执行器作用于环境的实体 ✅
- C. 具有自我意识、可自主进化的程序
- D. 任何部署在聊天界面里的 AI 助手

**解析**：AIMA 第 2 章开篇即此定义。按这个抽象，恒温器与人类同样是 Agent——定义只看「感知 + 行动」闭环，与技术形态无关。

*对应章节：`sec-01`*

### 第 2 题（基础 · 识别）

Wooldridge &amp; Jennings（1995）的「智能体四属性」不包含以下哪一项？
- A. 自主性 Autonomy
- B. 反应性 Reactivity
- C. 学习能力 Learning ✅
- D. 社会能力 Social ability

**解析**：四属性为：自主、社会、反应、主动（pro-activeness）。学习不在其中——这是最常见的误记。

*对应章节：`sec-01`*

### 第 3 题（进阶 · 理解）

按 Anthropic 的架构区分，Workflow 与 Agent 的分界线是？
- A. 是否调用了大语言模型
- B. 是否接入了工具与检索能力
- C. 下一步做什么由预定义代码路径决定，还是由模型动态决定 ✅
- D. 是否运行在沙箱环境中

**解析**：两者都属于智能体系统、都可用工具、都可调用 LLM；唯一区别是控制流的归属——代码写死为 Workflow，模型自主为 Agent。

*对应章节：`sec-02`*

### 第 4 题（进阶 · 理解）

关于「理性智能体（rational agent）」，下列说法正确的是？
- A. 理性智能体总能取得最好的实际结果
- B. 理性指在已有感知与知识下最大化期望表现，不要求预知实际结果 ✅
- C. 理性与全知（omniscience）是同一概念
- D. 一个行动是否理性，取决于它事后带来的结果

**解析**：AIMA 明确区分：理性最大化「期望表现」，全知与完美最大化「实际表现」；全知在现实中不可能。事后结果差，不能反推行动不理性。

*对应章节：`sec-04`*

### 第 5 题（挑战 · 应用）

一个客服系统：先把工单分类（退款类走流程 A、咨询类走流程 B），每条流程的步骤完全写死在代码里。按 Anthropic 的分类，它是？
- A. Agent，因为它调用 LLM 完成了分类
- B. Workflow，因为控制流由预定义代码路径编排 ✅
- C. 增强型 LLM 本身，因为它没有任何工具
- D. 多智能体系统，因为分类与处理是两个模块

**解析**：LLM 参与不等于 Agent。下一步由谁决定才是判据：这里路径全部写死，LLM 只在节点上干活——这正是 Anthropic 五种工作流中的「路由」模式。

*对应章节：`sec-02`*

### 第 6 题（挑战 · 应用）

你的 LLM Agent 在多步任务中错误越滚越大。按照本手册的铁律，最应优先补上的是？
- A. 换用参数量更大的模型
- B. 让每一步从环境获取观察（ground truth）来评估进展 ✅
- C. 把系统提示写得更长更详细
- D. 增加并行调用的数量

**解析**：铁律四：执行中每一步都必须从环境拿到 ground truth（工具结果、代码执行、测试反馈），否则错误会随步数复利累积——这正是 ReAct 中 Observation 环节存在的意义。

*对应章节：`sec-03`*
