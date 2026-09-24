"""
Python 基础 02：运算符 (operators)

学习目标：
1. 分清 / 与 // 的区别，理解 // 的「向下取整」和 % 的结果符号规则。
2. 理解浮点数比较的陷阱，会用链式比较和 math.isclose 做判断。
3. 掌握 and / or 的短路求值，以及「返回最后被求值的操作数本身」这一特性。
4. 认识成员、身份、位运算符，并知道优先级拿不准时就加括号。

运行方法：在 VSCode 里点右上角 ▶ 运行，或执行 python scripts/python-basics/02_operators.py

提示：文件末尾有练习与参考答案，想先自己做就把「参考答案」那一段用 # 注释掉再运行。
"""

import math

# ==== 1. 算术运算符 + - * / // % ** ====

# 为什么：点击率、转化率都是「除」出来的，除法结果是小数还是整数会直接影响后续计算。
# 是什么：/ 永远返回浮点数 (float)；// 向下取整（向负无穷方向）；% 取余；** 是幂。

impressions = 2000   # 曝光量 (impressions)
clicks = 300         # 点击量 (clicks)

# / 永远返回 float，哪怕能整除
print(7 / 2, 4 / 2)          # -> 3.5 2.0
print(type(7 / 2))           # -> <class 'float'>
# // 向下取整：正数好理解，但 -7 // 2 是 -4（往更小的方向取），不是 -3
print(7 // 2)                # -> 3
print(-7 // 2)               # -> -4
# % 取余：结果的符号跟随「除数」，而不是被除数
print(7 % 3)                 # -> 1
print(-7 % 3)                # -> 2
print(7 % -3)                # -> -2
# ** 幂：运算数可以是负数和浮点，并且它是右结合的
print(2 ** 10)               # -> 1024
print(2 ** -1)               # -> 0.5     负指数得到倒数
print(4 ** 0.5)              # -> 2.0     0.5 次方就是开平方
print(2 ** 3 ** 2)           # -> 512     先算 3**2=9，再算 2**9=512

# 用真实的投放数据算点击率 (CTR, click-through rate)
ctr = clicks / impressions
print(ctr)                   # -> 0.15
print(round(ctr * 100, 1))   # -> 15.0    换算成百分比
# 【动手改】把 impressions 改成 2350、clicks 改成 47，重新运行看 CTR 的变化。

# ==== 2. 比较运算符 == != > < >= <= ====

# 为什么：判断「效果是否达标」「两次计算是否相等」都依赖比较，而浮点数比较有坑。
# 是什么：比较运算返回布尔值 (bool)；多个比较可以用链式写法连起来。

# 浮点表示误差：0.1 + 0.2 并不精确等于 0.3
print(0.1 + 0.2)                       # -> 0.30000000000000004
print(0.1 + 0.2 == 0.3)                # -> False
print(round(0.1 + 0.2, 1) == 0.3)      # -> True    四舍五入到可接受精度再比
print(math.isclose(0.1 + 0.2, 0.3))    # -> True    判断「足够接近」

# 链式比较：0 < x < 10 官方定义是「等价于 0 < x and x < 10，不同点在于中间表达式最多只被求值一次」。
rate = 0.15
print(0 < rate < 1)                    # -> True
print(0 < rate < 0.1)                  # -> False

# == 比的是「值」，is 比的是「是不是同一个对象」
print([1, 2] == [1, 2])                # -> True    内容一样
print([1, 2] is [1, 2])                # -> False   是两个不同的列表对象
# 小整数缓存：CPython 把 -5 到 256 的小整数缓存复用，所以下面为 True
a = 256
b = 256
print(a is b)                          # -> True
# 注意：这是实现细节，不要依赖；换解释器、换写法结果就可能变了。
# 【动手改】把 rate 改成 1.5，看两个链式比较的结果变成什么。

# ==== 3. 逻辑运算符 and / or / not ====

# 为什么：给参数设默认值、组合多个条件时都会用到，但 and / or 的行为和很多语言不同。
# 是什么：二者都会短路求值，并返回「最后被求值的那个操作数本身」，不一定是布尔值。
# 官方原文：「请注意 and 和 or 都不限制其返回的值和类型必须为 False 和 True，
# 而是返回最后被求值的操作数」。

print(0 and "abc")          # -> 0        左边为假，直接返回 0
print("abc" and "def")      # -> def      左边为真，返回右边
print(0 or "匿名")           # -> 匿名     左边为假，返回右边
print("小明" or "匿名")       # -> 小明     左边为真，直接返回左边

# 惯用法：user_input 为空字符串时，用 or 兜一个默认值
user_input = ""             # 假装用户什么都没填
name = user_input or "匿名"
print(name)                 # -> 匿名

# 短路求值：左边一旦能确定结果，右边根本不会执行。
# 下面两行放在注释里，避免真去触发（否则会报 ZeroDivisionError）：
# print(True or (1 / 0))
# print(False and (1 / 0))

# not 一定返回布尔值，不会原样返回操作数
print(not "foo")            # -> False    不是 ''
print(not "")               # -> True
print(type(not "foo"))      # -> <class 'bool'>
# 【动手改】把 user_input 改成 "双十一"，看 name 打印出什么。

# ==== 4. 赋值运算符 += -= *= /= //= %= **= ====

# 为什么：累加统计量、反复更新同一个变量时能少写一遍变量名。
# 是什么：a += 1 等价于 a = a + 1；但对列表来说，+= 是「原地扩展」。

total = 100          # 销售额基数
total += 1
print(total)         # -> 101
total -= 1
print(total)         # -> 100
total *= 2
print(total)         # -> 200
total //= 3
print(total)         # -> 66       200 // 3 向下取整
total **= 2
print(total)         # -> 4356
total %= 1000
print(total)         # -> 356
avg = 300
avg /= 4
print(avg)           # -> 75.0     /= 的结果一定是 float

# 列表的 += 是原地扩展（相当于 extend），不新建对象；lst = lst + [1] 会新建对象
lst = [1, 2]
pid = id(lst)
lst += [3]
print(lst, id(lst) == pid)              # -> [1, 2, 3] True    还是同一个对象
other = [1, 2]
qid = id(other)
other = other + [3]
print(other, id(other) == qid)          # -> [1, 2, 3] False   换成新对象了
# 【动手改】把 total 的初值改成 7，重新跑一遍，看看每一行的结果。

# ==== 5. 成员与身份运算符 in / not in / is / is not ====

# 为什么：判断「某渠道是否在名单里」「某值是不是 None」是最常见的数据清洗动作。
# 是什么：in 检查成员关系；is 检查是不是同一个对象。

channels = ["抖音", "微信", "小红书"]
print("抖音" in channels)          # -> True
print("微博" not in channels)      # -> True
text = "广告,统计,Python"
print("统计" in text)              # -> True    字符串也能用 in 找子串
scores = {"抖音": 90, "微信": 85}
print("抖音" in scores)             # -> True    字典用 in 判的是「键」
print(90 in scores)                # -> False   值不算
tags = {"低龄", "高收入"}
print("低龄" in tags)               # -> True

# 判空一定要用 is None，不要用 == None
value = None
print(value is None)               # -> True
print(value == None)               # -> True    能跑通，但不推荐
# 原因：None 是单例 (singleton)，全程序只有一个 None 对象；
# 用 is 判断更快、语义更准，也不会被自定义的 __eq__ 干扰。
# 【动手改】往 channels 里加一个 "B站"，观察前两行结果的变化。

# ==== 6. 位运算符（了解即可）& | ^ ~ << >> ====

# 为什么：权限开关、渠道开关这类「一位代表一个状态」的场景偶尔会用到。
# 是什么：操作的是整数的二进制位，日常业务代码很少直接用到。

CAN_TARGET = 1   # 0001  可投放
HAS_BID = 2      # 0010  已出价
CONVERTED = 4    # 0100  已转化

# 用 | 把几个状态组合成一个数；用 & 检测某一位是否打开（结果非 0 就表示「是」）
status = CAN_TARGET | HAS_BID
print(status)                      # -> 3        0001 | 0010 = 0011
print(status & HAS_BID)            # -> 2
print(bool(status & CONVERTED))    # -> False    这一位是 0
# 用 ^ 翻转某一位；用 ~ 按位取反，结果是 -(x + 1)
print(status ^ HAS_BID)            # -> 1
print(~status)                     # -> -4
# << 左移：1 << n 可表示「第 n 个渠道」（从 0 开始数）；>> 是右移
print(1 << 3, 8 >> 3)              # -> 8 1
# 【动手改】把 status 加上 CONVERTED，再跑一遍上面的 & 检测。

# ==== 7. 优先级与括号 ====

# 为什么：表达式一长就容易看错，知道优先级顺序才能读懂别人的代码。
# 从低到高（左边结合最松）：:= < lambda < 条件表达式 < or < and < not
#   < 比较运算 (in / is / == / < 等同级) < | < ^ < & < 移位 < 加减
#   < 乘除取余 < 一元 +x -x ~x < ** < 取值 [] / 调用 () / 属性 .

print(2 + 3 * 4)          # -> 14      先乘后加
print((2 + 3) * 4)        # -> 20      括号优先
print(-2 ** 2)            # -> -4      ** 比一元负号结合更紧，等价于 -(2 ** 2)
print((-2) ** 2)          # -> 4
print(not True or True)   # -> True    先算 not，再算 or
print(2 ** -1)            # -> 0.5

# 结论一句话：拿不准就加括号。
# 【动手改】把 -2 ** 2 改成 -2 ** 3，先猜结果再运行。

# ===== 练习 =====
# 4 道题先自己写，再对照末尾的参考答案。
# 1（算术）曝光 4000、点击 128，求 CTR 并保留 4 位小数。验证：结果应为 0.032。
# 2（比较）x = 0.1 + 0.2，用 math.isclose 判断是否等于 0.3。验证：结果应为 True。
# 3（逻辑）raw = ""，用 or 让它取到默认值 "未命名活动"。验证：打印出 未命名活动。
# 4（位运算）构造「可投放 | 已转化」的状态数，再检测「已转化」「已出价」两位；
#   验证：状态数为 5，两个检测结果分别为 True 和 False。

# ===== 参考答案（建议先自己写一遍）=====
# 练习 1
impressions_2, clicks_2 = 4000, 128
ctr_2 = clicks_2 / impressions_2
print("练习1:", round(ctr_2, 4))        # -> 0.032

# 练习 2
x = 0.1 + 0.2
print("练习2:", math.isclose(x, 0.3))   # -> True

# 练习 3
raw = ""
print("练习3:", raw or "未命名活动")     # -> 未命名活动

# 练习 4
flag = 1 | 4                            # 可投放 | 已转化
print("练习4:", flag, bool(flag & 4), bool(flag & 2))   # -> 5 True False
