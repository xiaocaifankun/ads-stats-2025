"""
04 流程控制（Control Flow）

学习目标：
  1. 理解「缩进就是语法」，会用 4 个空格书写代码块；
  2. 掌握 if / elif / else、while、for + range 的写法与适用场景；
  3. 会用 break / continue，以及循环末尾的 else 子句；
  4. 了解循环变量的陷阱，并初步认识 Python 3.10 的 match / case。

运行方法：
  在 VSCode 里打开本文件，点右上角 ▶ Run Python File；
  或在仓库根目录执行：python scripts/python-basics/04_control_flow.py

提示：文件末尾有「练习」与「参考答案」。想先自己动手，就把「参考答案」那一段注释掉再运行；本文件只用标准库、不联网、不读输入。
"""

# ==== 1. 缩进就是语法 ====
# 为什么：Python 用缩进（indentation）而非大括号划分代码块，缩进写错程序直接跑不起来。
# 是什么：行尾冒号表示「下面是一个代码块」，块内每行缩进必须相同（惯例 4 个空格）。
views = 1200
if views > 1000:
    print("曝光量达标")        # -> 曝光量达标
    print("可以进入下一步")    # -> 可以进入下一步
# 错误示范（只写在注释里，不要真的运行）：
# if views > 1000:
# print("缺少缩进")        # IndentationError: expected an indented block
# if views > 1000:
#     print("A")
#       print("B")           # IndentationError: unexpected indent
# 最容易踩的坑是混用 Tab 和空格：编辑器里看着对齐，解释器会抛 TabError。
# 【动手改】把上面第一行 print 的缩进改成 3 个空格再运行，看报什么错，然后改回 4 个空格。

# ==== 2. if / elif / else ====
# 为什么：程序要按条件走不同分支；条件判断的本质是做「真值测试」（truth testing）。
# 是什么：if 后跟表达式，为真就执行；否则依次试 elif；都不满足则走 else。
score = 87
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 60:
    grade = "及格"
else:
    grade = "不及格"
print("成绩分档:", grade)      # -> 成绩分档: 良好
# 官方口径：这些是假值（falsy），其余一切值都为真：False、None、数字零（0、0.0、0j）、
# 空字符串、空元组、空列表、空字典、空集合、空冻结集合（frozenset）。
falsy = [False, None, 0, 0.0, 0j, "", (), [], {}, set(), frozenset()]
print("上面都是假值:", all(not v for v in falsy))   # -> 上面都是假值: True
# elif 有顺序：条件互相包含时，顺序写错结果就错。
s = 95
if s >= 60:
    result = "及格"
elif s >= 90:
    result = "优秀"        # 永远轮不到：上面 >= 60 已经命中
print("顺序写错的结果:", result)      # -> 顺序写错的结果: 及格
# 【动手改】把上面两个条件对调，让 95 分输出「优秀」。

# ==== 3. while ====
# 为什么：只知道「条件满足就继续」、不确定循环多少次时，用 while 最自然。
# 是什么：每轮开始前重新判断条件，为真就执行循环体，直到条件变假。
day_views = 100.0
days = 0
while day_views < 200:
    day_views = day_views * 1.05
    days += 1
print("翻倍需要天数:", days, "最终曝光量:", round(day_views, 2))   # -> 翻倍需要天数: 15 最终曝光量: 207.89
# while True + break：先无条件循环，在合适的时候用 break 退出。
n = 0
while True:
    n += 1
    if n == 3:
        break
print("n 停在:", n)        # -> n 停在: 3
# 实际工作里「多少天翻倍」更常用 for 或公式 math.log(2, 1.05)，while 只是其中一种写法。
# 【动手改】把增长率 1.05 改成 1.10，看天数变成几。

# ==== 4. for + range ====
# 为什么：遍历一串现成的元素时 for 比 while 省心；range 生成等差整数序列，左闭右开（含 a 不含 b）。
# 是什么：for 变量 in 可迭代对象逐个取出；range 是惰性序列（lazy sequence），用 list() 才能看到内容。
print("range(5):", list(range(5)))                  # -> range(5): [0, 1, 2, 3, 4]
print("range(2, 6):", list(range(2, 6)))            # -> range(2, 6): [2, 3, 4, 5]
print("range(0, 10, 3):", list(range(0, 10, 3)))    # -> range(0, 10, 3): [0, 3, 6, 9]
print("直接打印:", range(5))                        # -> 直接打印: range(0, 5)
for ch in "广告":
    print(ch)                                       # -> 广，然后 告
clicks = [120, 98, 150]
total = 0
for c in clicks:
    total += c
print("点击总量:", total)          # -> 点击总量: 368
channel = {"搜索": 120, "信息流": 98}
for name, value in channel.items():
    print("渠道:", name, "点击:", value)   # -> 渠道: 搜索 点击: 120，然后 信息流 点击: 98
# 只要键可写 for name in channel.keys():（等价于 for name in channel:）。
# 【动手改】用 range(1, 6) 打印 1 到 5。

# ==== 5. break / continue / 循环的 else ====
# 为什么：「找到就停」和「跳过这一轮」是循环里的高频需求。
# 是什么：break 结束整个循环；continue 跳过本轮剩余代码；else 在循环正常结束后才执行。
channels = [("搜索", 4.1), ("信息流", 3.2), ("开屏", 5.0)]
for name, cvr in channels:
    if cvr >= 4.5:
        print("第一个达标渠道:", name)     # -> 第一个达标渠道: 开屏
        break
else:
    print("没有渠道达标")                # 有 break 命中，本行不执行
for name, cvr in channels:
    if cvr >= 9.0:
        break
else:
    print("一个都没找到")        # -> 一个都没找到
for cvr in [3.2, 0.0, 5.0]:
    if cvr == 0.0:
        continue
    print("有效转化率:", cvr)    # -> 有效转化率: 3.2，然后 5.0
# 【动手改】把 4.5 这个阈值改成 6.0，观察上面的 else 分支会不会执行。

# ==== 6. 嵌套循环 ====
# 为什么：二维表（渠道 乘 日期）要外层走一行、内层走一格；break 只能跳出最内层那一层。
grid = {"搜索": [120, 98, 150], "信息流": [80, 210, 60]}
print("渠道 | 周一 | 周二 | 周三")        # -> 渠道 | 周一 | 周二 | 周三
for name in grid:
    row = " | ".join(str(v) for v in grid[name])
    print(name + " | " + row)         # -> 搜索 | 120 | 98 | 150，然后 信息流 | 80 | 210 | 60
# 中文是双宽字符，用 ljust 补空格会错位，所以这里用「竖线加空格」分隔，不做列对齐。
for i in range(2):
    for j in range(3):
        if j == 1:
            break
        print("i, j =", i, j)         # -> i, j = 0 0，然后 1 0
# 【动手改】把 j == 1 改成 j == 2，看输出行数变成几行。

# ==== 7. 循环变量的坑 ====
# 为什么：新手常以为「在循环体里改循环变量就能控制循环」，其实改不动；for 每轮都会用迭代器（iterator）的下一项覆盖循环变量。
# 是什么：出处 Python 语言参考 8.3（The for statement）；原文用 range(10)，这里换成 range(5) 让输出更短。
for i in range(5):
    print(i)          # -> 0 1 2 3 4（各占一行）
    i = 5             # 不会影响 for 循环
print("循环结束后 i =", i)        # -> 循环结束后 i = 5
# 想提前结束循环就写 break，而不是给循环变量赋值。
# 【动手改】把 i = 5 改成 i = 0，确认输出仍然是 0 到 4。

# ==== 8. match / case（Python 3.10 起可用） ====
# 为什么：「一个值有很多形态、每种形态做不同事」时，match 比一长串 elif 好读。
# 是什么：Python 3.10 引入的结构化模式匹配（structural pattern matching）。
def http_hint(code):
    match code:
        case 200 | 201:      # 或模式：竖线表示「或者」
            return "成功"
        case 404:
            return "页面不存在"
        case 500 | 502 | 503:
            return "服务器错误"
        case _:              # 通配符：总是匹配成功，必须放在最后一个 case
            return "其它状态"
for c in [200, 404, 503, 301]:
    print(c, "->", http_hint(c))    # -> 200 -> 成功；404 -> 页面不存在；503 -> 服务器错误；301 -> 其它状态
# if 守卫（guard）：case 后还能加 if 条件，进一步筛选。
def order_action(status, amount):
    match status:
        case "已支付" if amount > 0:
            return "发货"
        case "已支付":
            return "金额异常，人工核对"
        case _:
            return "无需处理"
print(order_action("已支付", 199))    # -> 发货
print(order_action("已支付", 0))      # -> 金额异常，人工核对
# 一句话：多数场景 if / elif 已经够用，match 在「一个值分多种形态」时才划算。
# 【动手改】在 case _ 前面加一行 case 418: return "我是茶壶"，再打印 http_hint(418)。

# ==== 9. 小综合 ====
# 为什么：把前面几节串起来：用 if 判断、for 遍历、真值测试，统计达标天数并找出最高点击在第几天。
daily_clicks = [120, 98, 150, 88, 210, 130, 175]
threshold = 150
hit_days = 0
best_day = 1
for day, value in enumerate(daily_clicks, start=1):
    if value >= threshold:
        hit_days += 1
    if value > daily_clicks[best_day - 1]:
        best_day = day
print("达标天数:", hit_days)              # -> 达标天数: 3
print("最高点击在第", best_day, "天")     # -> 最高点击在第 5 天
# enumerate(..., start=1) 同时给出「第几天」和「当天数值」，编号从 1 开始。
# 【动手改】把 threshold 改成 200，看达标天数变成几。

# ===== 练习 =====
# 共 4 题，先自己写，再对照末尾的参考答案。
# 1（if + 缩进）views = 1200，大于 1000 打印「曝光量达标」，否则打印「曝光量不足」。验证：应打印 曝光量达标
# 2（if / elif / else）score = 72，按 90 / 80 / 60 三档输出 优秀 / 良好 / 及格 / 不及格。验证：应打印 及格
# 3（while）点击量从 500 起步、每天增长 3%，多少天达到 800？验证：应打印 16
# 4（match / case）状态码 503 映射为「服务繁忙」，其它统一为「未知状态」。验证：应打印 服务繁忙

# ===== 参考答案（建议先自己写一遍）=====
print("=" * 40)

# 练习 1 参考答案
views = 1200
if views > 1000:
    print("参考答案 1:", "曝光量达标")      # -> 参考答案 1: 曝光量达标
else:
    print("参考答案 1:", "曝光量不足")

# 练习 2 参考答案
score = 72
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 60:
    grade = "及格"
else:
    grade = "不及格"
print("参考答案 2:", grade)                 # -> 参考答案 2: 及格

# 练习 3 参考答案
clicks = 500.0
days = 0
while clicks < 800:
    clicks = clicks * 1.03
    days += 1
print("参考答案 3:", days)                  # -> 参考答案 3: 16

# 练习 4 参考答案
def status_text(code):
    match code:
        case 503:
            return "服务繁忙"
        case _:
            return "未知状态"

print("参考答案 4:", status_text(503))      # -> 参考答案 4: 服务繁忙
