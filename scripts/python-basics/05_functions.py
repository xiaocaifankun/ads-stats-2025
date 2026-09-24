"""Python 基础 05：函数（Functions）

学习目标
1. 会定义函数、传参、收返回值，并知道没有 return 时函数返回 None。
2. 分清位置参数、关键字参数、默认参数，避开「可变默认参数」这个陷阱。
3. 会用 *args / **kwargs、多返回值、lambda，并理解 LEGB 作用域查找规则。
4. 能读懂类型注解与 docstring，了解递归的写法与终止条件。

运行方法：VSCode 里点右上角 ▶ Run Python File，或执行 python scripts/python-basics/05_functions.py
提示：末尾有练习与参考答案，想先自己做就把「参考答案」那一段注释掉。
"""

import sys  # 第 9 节演示递归层数上限时用到

# ==== 1. def 与调用：定义不执行，调用才执行 ====
# 为什么 -> 是什么：同一套计算要反复用，就起个名字包起来。def 只是「登记」，并不运行；
# 函数名加括号才算调用（call）。参数（parameter）把数据送进去，return 把结果送出来。
def calc_ctr(clicks, shows):
    """根据点击数和曝光数算出点击率 CTR（click-through rate）。"""
    return clicks / shows

print("函数已定义，但上面那行 return 一次都没执行过。")
print(calc_ctr(50, 1000))    # -> 0.05
print(calc_ctr(12, 400))     # -> 0.03

# 没有 return 的函数，默认返回 None（空值），所以打印出来是 None。
def log_title(title):
    "只打印渠道名，没有 return"
    print("渠道：", title)

print(log_title("信息流"))   # 函数体先打印一行，print 再把返回值打印出来：
# -> 渠道： 信息流
# -> None
# 【动手改】把 calc_ctr 的 return 改成 return round(clicks / shows, 3)，再跑一次。

# ==== 2. 三种参数：位置参数、关键字参数、默认参数 ====
# 为什么 -> 是什么：调用方有时只想改一个值，不想把参数全写一遍。位置参数按顺序对应，
# 关键字参数写成「名字=值」，默认参数在定义时先给初值；位置参数必须写在关键字参数前面。
def ctr_pct(clicks, shows, scale=100):
    "scale 默认 100，表示按百分比输出 CTR"
    return clicks / shows * scale

print(ctr_pct(50, 1000))                    # -> 5.0    只用位置参数
print(ctr_pct(50, 1000, 1))                 # -> 0.05   第三个也是位置参数
print(ctr_pct(clicks=50, shows=1000))       # -> 5.0    全用关键字
print(ctr_pct(50, shows=1000, scale=1))     # -> 0.05   混用：位置在前，关键字在后
# 错误示范（SyntaxError）：print(ctr_pct(clicks=50, 1000))
# 【动手改】给 ctr_pct 再加一个默认参数 unit="percent"，在返回值里带上它。

# ==== 3. 可变默认参数的陷阱（重点） ====
# 官方教程的警告：默认参数值只在「定义函数时」求值一次，所以默认值是列表、字典这类可变
# 对象（mutable）时，它会被多次调用共享，上一条数据会留到下一条里。
def add_channel(ch: str, box: list = []):
    "陷阱演示：这个 [] 在 def 那一刻就建好了，之后每次调用都用同一个"
    box.append(ch)
    return box

print(add_channel("信息流"))    # -> ['信息流']
print(add_channel("搜索"))      # -> ['信息流', '搜索']   第二次带着上一次的结果
print(add_channel("视频"))      # -> ['信息流', '搜索', '视频']

# 正确写法：默认值用不可变的 None，进函数后再新建列表。
def add_channel_ok(ch: str, box: list | None = None):
    if box is None:
        box = []
    box.append(ch)
    return box

print(add_channel_ok("信息流"))   # -> ['信息流']
print(add_channel_ok("搜索"))     # -> ['搜索']   每次都是全新的列表
# 【动手改】把 add_channel_ok 的 if 判断删掉，看它是否又变回陷阱。

# ==== 4. *args 与 **kwargs：接收任意数量的参数 ====
# 为什么 -> 是什么：函数不知道调用方会传几个渠道，就用打包机制先收下来。*args 把位置
# 参数打包成元组（tuple），**kwargs 把关键字参数打包成字典（dict）；调用时反过来。
def report(*args, **kwargs):
    "args 是元组，kwargs 是字典"
    print(args, kwargs)

report("信息流", "搜索", days=7)
# -> ('信息流', '搜索') {'days': 7}
report(*["信息流", "搜索"], **{"days": 14})    # * 拆列表，** 拆字典
# -> ('信息流', '搜索') {'days': 14}

# 参数列表里的 * 与 / 分隔符：* 之后只允许关键字传参，/ 之前只允许位置传参。
def split_demo(a, /, b, *, c):
    return a + b + c

print(split_demo(1, 2, c=3))    # -> 6
# 错误示范（TypeError）：print(split_demo(a=1, b=2, c=3))   位置专用参数不能用关键字传
# 【动手改】给 report 再加一个普通参数 base=0，在函数里把 base 也打印出来。

# ==== 5. 返回多个值：本质是返回一个元组 ====
# 为什么 -> 是什么：一次统计常要同时拿到总量和均值。return a, b 实际打包成元组 (a, b)，
# 调用处可以一次性解包（unpack）成多个变量。
def click_stats(clicks):
    "返回总点击量与平均点击量"
    return sum(clicks), sum(clicks) / len(clicks)

print(click_stats([120, 80, 150]))          # -> (350, 116.66666666666667)   本质是元组
total, avg = click_stats([120, 80, 150])    # 解包成两个变量
print(total, round(avg, 2))                 # -> 350 116.67
# 【动手改】让 click_stats 多返回一个「样本天数」，即元组里加上 len(clicks)。

# ==== 6. 作用域 LEGB：一个变量名去哪儿找 ====
# 为什么 -> 是什么：函数内外可能有同名变量，必须清楚读到的是哪一个。查找顺序是
# Local（局部）-> Enclosing（外层函数）-> Global（模块）-> Builtin（内置）。
region = "全国"          # Global，模块级变量

def read_region():
    "函数内部可以读全局变量"
    return region

def shadow():
    "给同名变量赋值：新建局部变量，不改全局变量"
    region = "华东"
    return region

print(read_region(), shadow())   # -> 全国 华东
print(region)                    # -> 全国   全局变量没有被改动
# 注意：若在 shadow 里先 print(region)、再写 region = "华东"，Python 会把 region 当成
# 局部变量，于是读到未赋值的局部变量 -> UnboundLocalError。

# global：在函数内声明「我改的是全局那个 region」。
def set_region_global():
    global region
    region = "华南"

set_region_global()
print(region)            # -> 华南

# nonlocal：改外层函数的变量，只能写在嵌套函数里。
def make_counter():
    n = 0
    def step():
        nonlocal n
        n += 1
        return n
    return step

count = make_counter()
print(count(), count(), count())    # -> 1 2 3
# 【动手改】建两个计数器 count_a 和 count_b，验证它们各自独立计数。

# ==== 7. lambda 匿名函数：只能写一个表达式 ====
# 为什么 -> 是什么：sorted、max 需要一条「小规则」，专门 def 一个名字太啰嗦。
# lambda 参数: 表达式，等价于只 return 这一行的函数；不能写语句，不能有 return。
ads = [("信息流", 120), ("搜索", 300), ("视频", 80)]

print(sorted(ads, key=lambda item: item[1]))
# -> [('视频', 80), ('信息流', 120), ('搜索', 300)]
print(max(ads, key=lambda item: item[1]))         # -> ('搜索', 300)
print(list(map(lambda item: item[0], ads)))       # -> ['信息流', '搜索', '视频']
print(list(filter(lambda item: item[1] > 100, ads)))    # -> [('信息流', 120), ('搜索', 300)]
# 提醒：规则一旦有点复杂，就用 def 写清楚，可读性比少敲几个字符重要。
# 【动手改】用 lambda + sorted 把 ads 按点击量从高到低排（提示：加 reverse=True）。

# ==== 8. 文档字符串与类型注解 ====
# 为什么 -> 是什么：别人（包括三个月后的你）要能一眼看出函数收什么、返回什么。
# docstring 写在函数体第一行；类型注解写在参数后和 -> 后，只是「给人看、给工具看」的
# 提示，运行时不强制、也不做类型检查。
def ctr(clicks: int, shows: int) -> float:
    """计算点击率 CTR：clicks 是点击数，shows 是曝光数，返回小数结果。"""
    return clicks / shows

print(ctr(50, 1000))                    # -> 0.05
print(ctr.__doc__.splitlines()[0])      # -> 计算点击率 CTR：clicks 是点击数，shows 是曝光数，返回小数结果。
print(ctr(50.0, 1000.0))                # -> 0.05   传浮点数照样能跑
# 注解不强制：print(ctr("50", "1000")) 传了字符串 Python 不拦，运行时才报 TypeError。
# 【动手改】把中间那行 print 换成 help(ctr)，看看终端里显示的完整文档。

# ==== 9. 递归（了解）：函数调用自己 ====
# 为什么 -> 是什么：有些结构天生「自己包含自己」，比如阶乘 n! = n * (n-1)!。函数体里
# 再调用自己，但必须有终止条件（base case），否则一直下钻并报 RecursionError。
def factorial(n):
    "阶乘：终止条件是 n == 0 时返回 1"
    if n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(5))                  # -> 120

def fib(n):
    "斐波那契：前两项是 0 和 1，之后每项等于前两项之和"
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(8)])    # -> [0, 1, 1, 2, 3, 5, 8, 13]
# 递归层数有上限，超了就报 RecursionError（默认约 1000 层）。
print(sys.getrecursionlimit())       # -> 1000
# 【动手改】故意删掉 factorial 的终止条件，看报错信息里 RecursionError 的样子。

# ==== 10. 小综合：把前面几节串起来 ====
# 用到的知识：多返回值的思想、默认参数、字典、列表推导式、docstring。
def summarize(clicks: list, target: int = 100) -> dict:
    """汇总一组每日点击量：总数、均值、最高、最低、达标天数。"""
    return {
        "total": sum(clicks), "avg": round(sum(clicks) / len(clicks), 2),
        "max": max(clicks), "min": min(clicks),
        "ok_days": len([c for c in clicks if c >= target]),
    }

week = [120, 90, 150, 60, 200, 110, 80]
print(summarize(week))
# -> {'total': 810, 'avg': 115.71, 'max': 200, 'min': 60, 'ok_days': 4}
# 【动手改】把 target 改成 150 再跑，看 ok_days 变成几。

# ===== 练习 =====
# 1. 写函数 avg_click(clicks) 返回平均点击量。验证：avg_click([100, 200, 300]) 得 200.0。
# 2. 写函数 tag(channel, prefix="渠道") 返回 "渠道-信息流" 这样的字符串；再用关键字参数把
#    两个实参的书写顺序调换一次，确认结果不变。验证：tag("信息流") 得 渠道-信息流。
# 3. 用 lambda + sorted 把 [("搜索", 0.06), ("信息流", 0.03)] 按 CTR 从高到低排序。
#    验证：结果第一项应是 ('搜索', 0.06)。
# 4. 写递归函数 power_two(n) 返回 2 的 n 次方，终止条件为 n == 0。验证：power_two(6) 得 64。

# ===== 参考答案（建议先自己写一遍）=====

def avg_click(clicks):
    "练习 1"
    return sum(clicks) / len(clicks)

print(avg_click([100, 200, 300]))    # -> 200.0

def tag(channel, prefix="渠道"):
    "练习 2"
    return f"{prefix}-{channel}"

print(tag("信息流"))                              # -> 渠道-信息流
print(tag(prefix="渠道", channel="信息流"))        # -> 渠道-信息流  关键字参数与顺序无关
print(sorted([("搜索", 0.06), ("信息流", 0.03)], key=lambda x: x[1], reverse=True))
# -> [('搜索', 0.06), ('信息流', 0.03)]

def power_two(n):
    "练习 4"
    if n == 0:
        return 1
    return 2 * power_two(n - 1)

print(power_two(6))                  # -> 64
