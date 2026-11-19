# -*- coding: utf-8 -*-
"""
03 父母职业相关性分析（类别变量练习）
=====================================
任务：对"类别变量练习数据.csv"进行数据清理与转化，
用卡方独立性检验分析父亲职业与母亲职业之间是否存在相关性，
并计算效应量（Cramér's V）与补充性 Fisher 精确检验。

数据说明：
- 原始数据是"父母工作单位名称"（非标准类别），需先清理、再转化为职业类别。
- 文件编码为 GBK/GB18030（Excel 导出常见），不是 UTF-8。

分类方案（转化规则）：
  1. 党政机关        —— 各级党政机构、街道社区、政法系统等公共管理部门
  2. 事业单位        —— 学校、医院、保健站、公共服务中心等公共服务机构
  3. 企业            —— 各类公司、集团、工程局、银行等企业单位
  4. 个体经营/私营商业 —— 店铺、餐馆、个体户等自营商业
  5. 家务劳动/无业    —— 家庭主妇、无工作
  6. 无效/缺失        —— "家庭父母""家庭父亲"等无法判断的填答，剔除

统计方法：
  - 5x5 列联表卡方独立性检验（小样本，期望频数不足，结果作参考并说明局限）
  - 压缩为 2x2（体制内=党政机关+事业单位 vs 体制外=企业+个体）后做 Fisher 精确检验
  - 效应量：Cramér's V 与 2x2 情形下的 φ 系数
  - 脚本在无 scipy 的环境下使用纯 Python 实现卡方分布上侧概率
    （正则化不完全 Gamma 函数）与 Fisher 精确检验，保证可复现。

用法：python 03_父母职业相关性分析.py [csv路径]
      不传参数时在脚本所在目录找"类别变量练习数据.csv"。
"""

import csv
import math
import os
import sys
from collections import Counter, OrderedDict

# ----------------------------------------------------------------------
# 一、文件路径
# ----------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.join(SCRIPT_DIR, "类别变量练习数据.csv")
DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_CSV
OUT_CLEAN = os.path.join(SCRIPT_DIR, "03_清理后数据.csv")
OUT_TABLE = os.path.join(SCRIPT_DIR, "03_列联表.csv")

# ----------------------------------------------------------------------
# 二、统计函数（无 scipy 时使用；有 scipy 时结果一致，可直接验证）
# ----------------------------------------------------------------------
def _contfract(a, x, itmax=300, eps=3e-9):
    """正则化上不完全 Gamma 函数 Q(a,x) 的连分式（Numerical Recipes）。"""
    b, c, d = x + 1.0 - a, 1.0 / (x + 1.0 - a), 1.0 / (x + 1.0 - a)
    for i in range(1, itmax + 1):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < 1e-300:
            d = 1e-300
        c = b + an / c
        if abs(c) < 1e-300:
            c = 1e-300
        d = 1.0 / d
        delta = d * c
        d *= delta
        if abs(delta - 1.0) < eps:
            break
    return math.exp(-x + a * math.log(x) - math.lgamma(a)) * d


def chi2_sf(x, df):
    """卡方分布上侧概率 P(X >= x)。"""
    if x <= 0:
        return 1.0
    a, xx = df / 2.0, x / 2.0
    if xx < a + 1.0:  # 级数法求下不完全 Gamma，再取补
        s, term = 1.0 / a, 1.0 / a
        for n in range(1, 500):
            term *= xx / (a + n)
            s += term
            if abs(term) < abs(s) * 1e-12:
                break
        p_lower = s * math.exp(-xx + a * math.log(xx) - math.lgamma(a))
        return max(0.0, 1.0 - p_lower)
    return _contfract(a, xx)


def fisher_exact_2x2(a, b, c, d):
    """Fisher 精确检验（双侧）。a b c d 按行排列。"""
    n = a + b + c + d
    r1, c1 = a + b, a + c
    p_obs = math.comb(r1, a) * math.comb(n - r1, c1 - a) / math.comb(n, c1)
    total = 0.0
    lo, hi = max(0, r1 + c1 - n), min(r1, c1)
    for k in range(lo, hi + 1):
        p_k = math.comb(r1, k) * math.comb(n - r1, c1 - k) / math.comb(n, c1)
        if p_k <= p_obs * (1 + 1e-9):
            total += p_k
    return min(1.0, total)

try:
    from scipy import stats as _stats
    HAVE_SCIPY = True
except ImportError:
    HAVE_SCIPY = False

# ----------------------------------------------------------------------
# 三、读取原始数据（自动尝试多种编码）
# ----------------------------------------------------------------------
def read_raw(path):
    for enc in ("utf-8-sig", "gb18030", "utf-8"):
        try:
            with open(path, encoding=enc, newline="") as f:
                rows = list(csv.reader(f))
            print(f"[读取] {path}（编码 {enc}），共 {len(rows) - 1} 行数据")
            return rows[0], rows[1:]
        except UnicodeDecodeError:
            continue
    raise RuntimeError("无法识别文件编码")

# ----------------------------------------------------------------------
# 四、清理与转化：单位名称 -> 职业类别
# ----------------------------------------------------------------------
INVALID_TOKENS = {"家庭父亲", "家庭父母", "家庭母亲", "未知", "不清楚"}
HOME_TOKENS = {"家庭主妇", "无", "无业", "家务", "待业"}

# 关键词按优先级依次匹配：先个体商业，再企业，再党政，最后事业单位。
# （"公司""工程局"必须先于"局"判断，避免"中铁六局太原铁路建设公司"误入党政）
KW_SELF = ["个体", "店", "饺子馆", "食府", "烟酒", "便利店", "菜市场",
           "农资", "电动工具", "汽修", "浴足", "杂粮", "书店", "蛋糕", "浴"]
KW_QIYE = ["公司", "集团", "工程局", "银行", "农行", "支行", "信用社",
           "厂", "中海油"]
KW_GOV = ["局", "委员会", "管委会", "党委", "纪委", "政府", "街道", "社区",
          "法院", "公安", "监狱", "执法队", "团委", "编办", "市委办",
          "统战部", "市政管理"]
KW_SHIYE = ["学校", "中学", "小学", "大学", "学院", "医院", "保健站",
            "疾控", "中心", "研究所", "卫生院", "教职工", "融媒体"]

# 个别名称无法用关键词覆盖，人工指定（领域判断）
OVERRIDES = {"大自然旅行社": "个体经营/私营商业",
             "二十一冶": "企业"}  # 甘肃二十一冶建设集团（国企）


def classify(raw):
    """把一个工作单位名称转化为职业类别；无法判断返回 None。"""
    s = str(raw).replace("\n", "").replace("\r", "").strip()
    if s == "":
        return None
    if s in INVALID_TOKENS:
        return None
    if s in HOME_TOKENS:
        return "家务劳动/无业"
    if s in OVERRIDES:
        return OVERRIDES[s]
    for kw in KW_SELF:
        if kw in s:
            return "个体经营/私营商业"
    for kw in KW_QIYE:
        if kw in s:
            return "企业"
    for kw in KW_GOV:
        if kw in s:
            return "党政机关"
    for kw in KW_SHIYE:
        if kw in s:
            return "事业单位"
    return None  # 兜底：无法归类


def load_and_transform(path):
    header, rows = read_raw(path)
    records = []
    for i, row in enumerate(rows, 1):
        if len(row) < 2:
            row = (row + ["", ""])[:2]
        f_raw, m_raw = row[0], row[1]
        f_cat, m_cat = classify(f_raw), classify(m_raw)
        records.append({"序号": i, "父亲原始": f_raw.strip(),
                        "母亲原始": m_raw.strip(),
                        "父亲类别": f_cat or "无效/缺失",
                        "母亲类别": m_cat or "无效/缺失"})
    return records


# ----------------------------------------------------------------------
# 五、列联表与检验
# ----------------------------------------------------------------------
CAT_ORDER = ["党政机关", "事业单位", "企业", "个体经营/私营商业",
             "家务劳动/无业"]
SHORT = {"党政机关": "党政", "事业单位": "事业", "企业": "企业",
         "个体经营/私营商业": "个体", "家务劳动/无业": "家务/无业"}


def build_crosstab(records, cats_f, cats_m):
    table = [[0] * len(cats_m) for _ in cats_f]
    for r in records:
        if r["父亲类别"] in cats_f and r["母亲类别"] in cats_m:
            table[cats_f.index(r["父亲类别"])][cats_m.index(r["母亲类别"])] += 1
    return table


def chi2_test(table):
    n = sum(sum(row) for row in table)
    row_s = [sum(r) for r in table]
    col_s = [sum(table[i][j] for i in range(len(table))) for j in range(len(table[0]))]
    chi2 = 0.0
    expected = [[row_s[i] * col_s[j] / n for j in range(len(col_s))]
                for i in range(len(row_s))]
    for i, r in enumerate(table):
        for j, o in enumerate(r):
            e = expected[i][j]
            if e > 0:
                chi2 += (o - e) ** 2 / e
    df = (len(row_s) - 1) * (len(col_s) - 1)
    p = (chi2_sf(chi2, df) if not HAVE_SCIPY
         else float(_stats.chi2.sf(chi2, df)))
    v = math.sqrt(chi2 / (n * min(len(row_s) - 1, len(col_s) - 1))) if n else 0.0
    resid = [[(table[i][j] - expected[i][j]) / math.sqrt(expected[i][j])
              if expected[i][j] > 0 else float("nan")
              for j in range(len(col_s))] for i in range(len(row_s))]
    return {"chi2": chi2, "df": df, "p": p, "V": v, "n": n,
            "expected": expected, "resid": resid,
            "row_s": row_s, "col_s": col_s}


def fisher_from_table(table, cats_f, cats_m):
    """把体制内（党政+事业）与体制外（企业+个体+家务）压缩成 2x2。"""
    def inside(cats):
        return [c in ("党政机关", "事业单位") for c in cats]
    fi, mi = inside(cats_f), inside(cats_m)
    a = sum(table[i][j] for i in range(len(fi)) if fi[i]
            for j in range(len(mi)) if mi[j])
    b = sum(table[i][j] for i in range(len(fi)) if fi[i]
            for j in range(len(mi)) if not mi[j])
    c = sum(table[i][j] for i in range(len(fi)) if not fi[i]
            for j in range(len(mi)) if mi[j])
    d = sum(table[i][j] for i in range(len(fi)) if not fi[i]
            for j in range(len(mi)) if not mi[j])
    if HAVE_SCIPY:
        _, p = _stats.fisher_exact([[a, b], [c, d]])
    else:
        p = fisher_exact_2x2(a, b, c, d)
    n = a + b + c + d
    phi = abs(a * d - b * c) / math.sqrt(
        (a + b) * (c + d) * (a + c) * (b + d)) if n else 0.0
    return a, b, c, d, p, phi

# ----------------------------------------------------------------------
# 六、输出
# ----------------------------------------------------------------------
def main():
    print("=" * 66)
    print("类别变量练习：父母职业相关性分析（数据清理 -> 转化 -> 检验）")
    print("=" * 66)

    records = load_and_transform(DATA_PATH)
    n_raw = len(records)

    # ---- 清理报告 ----
    f_valid = [r for r in records if r["父亲类别"] != "无效/缺失"]
    m_valid = [r for r in records if r["母亲类别"] != "无效/缺失"]
    both = [r for r in records if r["父亲类别"] != "无效/缺失"
            and r["母亲类别"] != "无效/缺失"]
    print(f"\n[清理] 原始记录 {n_raw} 条；"
          f"父亲职业有效 {len(f_valid)} 条，母亲职业有效 {len(m_valid)} 条，"
          f"两者同时有效 {len(both)} 条（进入分析）")
    print(f"[清理] 剔除的无用填答：{[r['父亲原始'] or r['母亲原始'] for r in records if r['父亲类别'] == '无效/缺失' or r['母亲类别'] == '无效/缺失']}")

    # ---- 转化对照表 ----
    print("\n[转化] 单位名称 -> 职业类别（前 15 条示例）：")
    for r in both[:15]:
        print(f"  {r['序号']:>3}. {r['父亲原始']} -> {SHORT[r['父亲类别']]} | "
              f"{r['母亲原始']} -> {SHORT[r['母亲类别']]}")

    cats_f = [c for c in CAT_ORDER
              if any(r["父亲类别"] == c for r in both)]
    cats_m = [c for c in CAT_ORDER
              if any(r["母亲类别"] == c for r in both)]
    table = build_crosstab(both, cats_f, cats_m)

    # ---- 保存清理后数据与列联表 ----
    with open(OUT_CLEAN, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["序号", "父亲原始", "母亲原始",
                                          "父亲类别", "母亲类别"])
        w.writeheader()
        w.writerows(records)
    with open(OUT_TABLE, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["父亲\\母亲"] + [SHORT[c] for c in cats_m])
        for i, cf in enumerate(cats_f):
            w.writerow([SHORT[cf]] + table[i])

    # ---- 列联表 ----
    print("\n[列联表] 行=父亲职业类别，列=母亲职业类别：")
    head = "            " + "".join(f"{SHORT[c]:>8}" for c in cats_m)
    print(head)
    for i, cf in enumerate(cats_f):
        print(f"{SHORT[cf]:<10} " + "".join(f"{table[i][j]:>8}"
              for j in range(len(cats_m))))

    # ---- 卡方检验 ----
    res = chi2_test(table)
    lib = "scipy.stats.chi2.sf" if HAVE_SCIPY else "内置不完全Gamma实现"
    print(f"\n[卡方检验 5x{len(cats_m)}] chi2 = {res['chi2']:.3f}, "
          f"df = {res['df']}, p = {res['p']:.4f}  (p 值由 {lib} 计算)")
    print(f"[效应量]  Cramer's V = {res['V']:.3f}")
    n = res["n"]
    low_cells = sum(1 for row in res["expected"] for e in row if e < 5)
    print(f"[前提检查] 样本量 n={n}，期望频数<5 的单元格有 {low_cells}/"
          f"{len(table) * len(cats_m)} 个 -> 卡方近似偏乐观，结论需谨慎")

    # ---- 标准化残差 ----
    print("\n[标准化残差] （|值|>2 视为明显偏离独立模型）：")
    print("            " + "".join(f"{SHORT[c]:>8}" for c in cats_m))
    for i, cf in enumerate(cats_f):
        print(f"{SHORT[cf]:<10} " + "".join(
            f"{res['resid'][i][j]:>8.2f}" for j in range(len(cats_m))))

    # ---- Fisher 2x2 补充检验：体制内 vs 体制外 ----
    a, b, c, d, p_f, phi = fisher_from_table(table, cats_f, cats_m)
    print("\n[Fisher 精确检验 2x2] 父亲{体制内/外} x 母亲{体制内/外}")
    print(f"  体制内 = 党政机关 + 事业单位；体制外 = 企业 + 个体 + 家务/无业")
    print(f"  [[{a},{b}],[{c},{d}]]  双侧 p = {p_f:.4f}, phi = {phi:.3f}")

    # ---- 简要结论 ----
    print("\n[结论要点]")
    f_in = (a + b) / (a + b + c + d)
    m_in = (a + c) / (a + b + c + d)
    both_in = a / (a + b + c + d)
    print(f"  1. 父亲体制内比例 {f_in:.0%}，母亲体制内比例 {m_in:.0%}，"
          f"双体制内家庭占 {both_in:.0%}")
    if p_f < 0.05:
        print(f"  2. Fisher 检验 p={p_f:.4f} < 0.05：父母'体制属性'存在显著相关性，"
              f"呈现'体制内-体制内'的匹配（同质婚）倾向")
    else:
        print(f"  2. Fisher 检验 p={p_f:.4f} >= 0.05：在 0.05 水平上尚不能拒绝独立性")
    print(f"  3. 母亲'家务劳动/无业'比例明显高于父亲（性别分工差异），"
          f"是列联表中最突出的非对称结构")
    print(f"  4. 局限：n={n} 偏小、类别多、地域集中（多为白银市），"
          f"结论只能作为课堂练习层面的提示，不能外推到总体")
    print("\n[输出] 清理后数据 ->", OUT_CLEAN)
    print("[输出] 列联表   ->", OUT_TABLE)


if __name__ == "__main__":
    main()
