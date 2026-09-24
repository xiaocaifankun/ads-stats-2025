"""
03 表达式（Expression）：有值的代码单元
================================================================
学习目标
  1. 分清「表达式」与「语句」：表达式有值，语句是动作。
  2. 会用条件表达式（三元）、赋值表达式（海象运算符 :=）和推导式（comprehension）。
  3. 熟悉 len / sum / min / max / sorted / zip / enumerate / any / all 的常用用法。
  4. 记住两个常见陷阱：对象别名、复合表达式的求值顺序与短路。
运行方法
  VSCode 打开本文件点右上角 ▶；或在仓库根目录执行：
      python scripts/python-basics/03_expressions.py
提示
  末尾有「练习」与「参考答案」。想先自己做，就把「参考答案」那一段整体注释掉再运行。
================================================================
"""

# ==== 1. 表达式 vs 语句 ====
# 为什么：分清「有没有值」，后面理解推导式、海象运算符会顺很多。
# 是什么：表达式（expression）求值后得到结果；语句（statement）是让程序去做一件事。

print(1 + 2)             # -> 3      （1 + 2 是表达式，值就是 3）
print(len("abc"))        # -> 3      （函数调用也是表达式）
x = 1                    # 赋值语句：执行「把 1 绑定给名字 x」这个动作，本身没有可打印的值
# 下面两种写法都是语法错误，所以只写在注释里：
# print(x = 1)           # SyntaxError: invalid syntax
# y = (x = 1)            # SyntaxError（C/Java 允许赋值当表达式，Python 不允许）

# 【动手改】把 print(1 + 2) 改成 print("1" + "2")，看结果变成什么。

# ==== 2. 字面量也是表达式 ====
# 为什么：字面量看着「不像代码」，其实是表达式里最简单的一种——写出来自带一个值。
# 是什么：直接写在源码里的常量值。逐个用 type() 看它们真实的类型。

values = [1, 1.0, "1", True, None, [1, 2], (1,), {"a": 1}, {1, 2}]
for v in values:
    print(repr(v), "->", type(v).__name__)
# -> 1 -> int / 1.0 -> float / '1' -> str / True -> bool / None -> NoneType
# -> [1, 2] -> list / (1,) -> tuple / {'a': 1} -> dict / {1, 2} -> set

# 能直接当参数传给函数，也说明「字面量是表达式」
print(max(1, 2.0))       # -> 2.0    （整数和浮点数可以比大小）

# 【动手改】把 1.0 改成 "1.0"，看它的类型和 max 的结果怎么变。

# ==== 3. 条件表达式（三元）====
# 为什么：很多判断只是「二选一」，写 if/else 要四行，一行表达式就能搞定。
# 是什么：x if C else y。官方文档指出：它「首先对条件 C 求值」，而不是先算 x。

ctr = 0.032              # 某渠道点击率 3.2%
target = 0.03            # 达标线 3%
print("达标" if ctr >= target else "未达标")                          # -> 达标

# 用小函数记录求值顺序，验证「先算条件 C」
order = []
def pick(name, value):
    order.append(name)
    return value
result = pick("x", "选了 x") if pick("C", ctr >= target) else pick("y", "选了 y")
print(result, order)     # -> 选了 x ['C', 'x']

print("优秀" if ctr >= 0.05 else ("达标" if ctr >= target else "待优化"))   # -> 达标（嵌套要加括号）
print(f"点击率 {ctr:.1%}，状态：{'达标' if ctr >= target else '未达标'}")    # -> 点击率 3.2%，状态：达标

# 【动手改】把 ctr 改成 0.021 再跑，猜猜三处结果分别会变成什么。

# ==== 4. 赋值表达式 := （海象运算符，Python 3.8+）====
# 为什么：一个值既要「参与判断」又要「留下来用」，普通写法得算两遍。
# 是什么：语法 [identifier ":="] expression —— 既绑定名字，又返回这个值。名字取自它的形状（海象的眼和牙）。

# 用例一（官方例子的本地化）：迭代器边取边判，取空即停
queue = iter(["周一广告位", "周二广告位", "周三广告位"])
while (chunk := next(queue, None)) is not None:
    print("处理：", chunk)
# -> 处理： 周一广告位 / 处理： 周二广告位 / 处理： 周三广告位
print("队列已取空")       # -> 队列已取空

# 用例二：长度先存进 n，判断之后 n 还能继续用
items = ["曝光", "点击", "转化", "成本"]
if (n := len(items)) > 3:
    print(f"指标有 {n} 个，超过 3 个")     # -> 指标有 4 个，超过 3 个
print("n 仍可用：", n)    # -> n 仍可用： 4

# 括号要求（最容易踩的坑，下面每条都实测过）：
#   1) 在 if / while 的「条件位置」可以不加括号：while chunk := next(queue, None):
#   2) 在下面这些位置必须用圆括号，否则是语法错误（只列举，不触发）：
#        n := 10                        # 表达式语句：要写 (n := 10)
#        nums[: i := 2]                 # 切片：要写 nums[: (i := 2)]
#        1 if v := 0 else 2             # 条件表达式：要写 1 if (v := 0) else 2
#        lambda: w := 1                 # lambda：要写 lambda: (w := 1)
#        f(x = y := 1)                  # 关键字参数：要写 f(x=(y := 1))；位置参数写 f(y := 1) 可以不加
#        [a for a in xs if b := a]      # 推导式的 if 子句：要写 if (b := a)
#        assert (z := 1)、with (m := open("d.txt")) as f、赋值语句的子表达式同理
#   记法：位置本身就是「判断条件」就不用括号，其余一律加括号。

# 【动手改】把 while 的条件换成 chunk != "周二广告位"，看循环何时停。

# ==== 5. 推导式（comprehension）====
# 为什么：把「遍历 + 过滤 + 收集」压成一行，是 Python 最常见的表达习惯。
# 是什么：用一条表达式从可迭代对象推出新的列表 / 字典 / 集合 / 生成器。本节与第 6 节共用下面这组数据。

channels = ["搜索", "信息流", "开屏", "短视频"]
clicks = [5200, 3100, 800, 4600]

print([x ** 2 for x in range(5)])                          # -> [0, 1, 4, 9, 16]
print([ch for ch, c in zip(channels, clicks) if c >= 1000])    # -> ['搜索', '信息流', '短视频']
print({ch: c for ch, c in zip(channels, clicks)})
# -> {'搜索': 5200, '信息流': 3100, '开屏': 800, '短视频': 4600}
print({len(ch) for ch in channels})                        # -> {2, 3}

# 生成器表达式用圆括号，是惰性（lazy）的：不立刻算，被消费时才逐个产出
squares = (x * x for x in range(5))
print(type(squares).__name__, sum(squares), sum(squares))
# -> generator 30 0   （第一次 sum 消费出 30，第二次已是空，得 0）

# 等价的 for 循环：结果一样，行数更多，但「先算后存」一目了然
result = []
for x in range(5):
    result.append(x ** 2)
print(result)                                              # -> [0, 1, 4, 9, 16]

# 结论：推导式不是必须的。逻辑一超过一层（带副作用、要 try），等价 for 循环更清楚，可读性优先。

# 【动手改】把第二个 print 的条件改成 c >= 3000，先猜结果再跑。

# ==== 6. 表达式里的常用内置函数 ====
# 为什么：统计日常就是「有多少、加起来、谁最大、排个序」，这些都有现成的内置函数（built-in）。
# 是什么：Python 自带、直接可用的函数。下面沿用第 5 节的 channels / clicks。

print(len(clicks))                                         # -> 4          （渠道个数）
print(sum(clicks))                                         # -> 13700      （总点击量）
print(min(clicks), max(clicks))                            # -> 800 5200   （最少 / 最多）
print(sorted(clicks))                                      # -> [800, 3100, 4600, 5200]

# sorted 的 key= 决定按什么排，reverse= 决定升序还是降序
ranking = sorted(zip(channels, clicks), key=lambda item: item[1], reverse=True)
print(ranking)
# -> [('搜索', 5200), ('短视频', 4600), ('信息流', 3100), ('开屏', 800)]
print(sorted(channels, key=len))                           # -> ['搜索', '开屏', '信息流', '短视频']

# zip 把两个序列拉成一格一格；enumerate 给每个元素配序号（默认从 0 开始）
print(list(zip(channels, clicks))[0])                      # -> ('搜索', 5200)
print(list(enumerate(channels, start=1)))
# -> [(1, '搜索'), (2, '信息流'), (3, '开屏'), (4, '短视频')]

# any 只要有一个满足就 True；all 必须全部满足才 True
target = 3000
print(any(c >= target for c in clicks))                    # -> True     （有渠道达标）
print(all(c >= target for c in clicks))                    # -> False    （开屏只有 800）

# 【动手改】把 target 改成 1000，先猜两行输出，再跑。

# ==== 7. 别名陷阱：a = b = [] 与 [[0] * 2] * 3 ====
# 为什么：Python 的变量是「名字贴在对象上」，不是「盒子装值」；一次给两个名字赋值，贴的是同一个对象。
# 是什么：值可变（mutable，如 list / dict / set）时，改一个名字会波及另一个，这叫别名（alias）。

a = b = []               # a、b 指向同一个空列表
a.append("曝光")
print(a, b)              # -> ['曝光'] ['曝光']
print(a is b, id(a) == id(b))    # -> True True   （is 比对象身份，id() 给出内存地址编号）

# 更隐蔽的坑：* 复制的是「引用」，三行其实是同一个列表
grid = [[0] * 2] * 3
grid[0][0] = 9
print(grid, grid[0] is grid[1])  # -> [[9, 0], [9, 0], [9, 0]] True

# 正确写法：用推导式，每轮新建一个列表
safe = [[0] * 2 for _ in range(3)]
safe[0][0] = 9
print(safe, safe[0] is safe[1])  # -> [[9, 0], [0, 0], [0, 0]] False

# 【动手改】把 a = b = [] 拆成 a = []、b = [] 两行，再看 a is b 的结果。

# ==== 8. 复合表达式的求值顺序 ====
# 为什么：一行里塞了几个函数调用时，谁先谁后决定结果和副作用（side effect）。
# 是什么：Python 从左到右求值；and / or 会短路（short-circuit）——结果已定，右边根本不会被求值。

def step(name, value):
    print(f"  求值 {name}")
    return value

print(step("X", 1) + step("Y", 2))                # -> 求值 X / 求值 Y / 3         （从左到右）
print(step("A", True) or step("B", True))         # -> 求值 A / True               （or 短路，B 不算）
print(step("C", False) or step("D", "兜底"))       # -> 求值 C / 求值 D / 兜底       （返回右边的值）
print(step("E", False) and step("F", True))       # -> 求值 E / False              （and 短路，F 不算）

# and / or「到底返回哪个值」的规则见同目录 02_operators.py，这里只强调顺序与短路。

# 【动手改】把上面 E 的 False 改成 True，预测会多打印哪一行。

# ===== 练习 =====
# 先自己做，再对照文末参考答案；每题都给了验证方式（预期输出）。
# 1. 条件表达式：ctr = 0.021，达标线 0.03、优秀线 0.05。
#    用一个条件表达式（不要用 if 语句）算出等级并打印。验证：输出应为 待优化
# 2. 海象运算符：exposures = iter([1000, 2000, 500, 1500])。
#    用 while + := 依次取值累加，取完为止（next(..., None) 判断结束），打印总曝光量。验证：5000
# 3. 推导式 + 内置函数：沿用上面的 channels / clicks。
#    挑出点击量 >= 1000 的渠道名，并求这些渠道的点击量之和。验证：['搜索', '信息流', '短视频'] 与 12900
# 4. 别名陷阱：说明 [[0] * 2] * 3 的危险，并给出安全的 3 行 2 列网格写法。
#    用 is 或 id() 证明「危险写法里三行是同一个对象」，且安全写法改一行不影响其它行。
#    验证：危险写法打印 True，安全写法改动后应为 [[7, 0], [0, 0], [0, 0]]

# ===== 参考答案（建议先自己写一遍）=====

# 第 1 题
ctr = 0.021
print("优秀" if ctr >= 0.05 else ("达标" if ctr >= 0.03 else "待优化"))   # -> 待优化

# 第 2 题
exposures = iter([1000, 2000, 500, 1500])
total = 0
while (v := next(exposures, None)) is not None:
    total += v
print(total)                             # -> 5000

# 第 3 题
hot = [ch for ch, c in zip(channels, clicks) if c >= 1000]
print(hot, sum(c for ch, c in zip(channels, clicks) if c >= 1000))
# -> ['搜索', '信息流', '短视频'] 12900

# 第 4 题
risky_grid = [[0] * 2] * 3
print(risky_grid[0] is risky_grid[1] is risky_grid[2])                    # -> True
safe_grid = [[0] * 2 for _ in range(3)]
safe_grid[0][0] = 7
print(safe_grid)                         # -> [[7, 0], [0, 0], [0, 0]]
