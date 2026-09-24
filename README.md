# ads-stats-2025

2025 级广告学 2 班《统计与数据分析》课程演示仓库。

| 项 | 内容 |
| --- | --- |
| 课程 | 《统计与数据分析》 |
| 班级 | 2025 级广告学 2 班 |
| 上课时间 | 每周四下午 |
| 姊妹仓库 | [statistics-data-analysis](https://github.com/yangjh-xbmu/statistics-data-analysis) — 广告学 1 班（每周三晚上） |

> 班级与上课时段按课程安排核对。

## 用途

课堂投屏演示用。含两部分：

- `slides/` — 单文件 HTML 课件，浏览器直接打开，无需环境依赖
- `notebooks/` — Python 实操讲义（Jupyter Notebook），配合数据集现场跑

## 目录结构

```
ads-stats-2025/
├── slides/       # 单文件 HTML 课件（课堂投屏）
├── notebooks/    # Jupyter Notebook 实操讲义
├── datasets/     # 课程数据集（CSV）
├── exercises/    # 课堂练习与课后作业
└── notes/        # 讲义文字稿、补充材料
```

## 环境准备

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install pandas numpy matplotlib jupyter

jupyter notebook notebooks/
```

## 课程进度

| 讲次 | 主题 | 课件 | Notebook |
| --- | --- | --- | --- |
| 01 | 描述性统计：从广告数据说起 | [slides/01-descriptive-statistics.html](slides/01-descriptive-statistics.html) | [notebooks/01-descriptive-statistics.ipynb](notebooks/01-descriptive-statistics.ipynb) |
| 02 | 概率基础与广告投放决策 | 待补 | 待补 |
| 03 | 假设检验：A/B 测试怎么做 | 待补 | 待补 |
| 04 | 回归分析：广告效果归因 | 待补 | 待补 |
| 05 | 数据可视化：图表怎么说话 | 待补 | 待补 |

## 数据说明

`datasets/` 中的数据为教学模拟数据，用于演示分析方法，非真实商业数据。
