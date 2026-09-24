"""
《统计与数据分析》Python 基础 01：变量

学习目标：
  1. 理解 `=` 是把变量名绑定到对象，而不是把值装进盒子里。
  2. 知道变量本身没有类型，对象才有类型（动态类型）。
  3. 掌握合法标识符、命名惯例，以及常见内置类型长什么样。
  4. 会用多重赋值、解包、类型转换和 f-string 输出广告与统计指标。

运行方法：
  在 VSCode 里打开本文件，点右上角 ▶ Run Python File；
  或在命令行执行：python scripts/python-basics/01_variables.py

提示：文件末尾有练习与参考答案。想先自己做，就把「参考答案」那一段用 # 注释掉再运行。
"""

import keyword  # 标准库，用来查看 Python 的关键字列表

# ==== 1. 变量是什么 ====
# 为什么：同一份数据要反复使用，给它起个名字就不用重复写。
# 是什么：`=` 不复制值，只是让左边的名字指向右边那个对象。
campaign = "夏季促销"
alias = campaign
print("campaign =", campaign)                              # -> campaign = 夏季促销
print("id(campaign) == id(alias):", id(campaign) == id(alias))   # -> True

# 重新赋值只是让名字换个指向，原来的对象不受影响
alias = "618 大促"
print("campaign =", campaign)                              # -> campaign = 夏季促销
print("alias =", alias)                                    # -> alias = 618 大促

# 【动手改】把 alias = "618 大促" 改成 alias = campaign，重新运行看会怎样。

# ==== 2. 动态类型 ====
# 为什么：同一个名字后面可以换成别的东西，这是 Python 灵活的地方。
# 是什么：变量没有类型，类型跟着对象走，type() 看的是当前指向的对象。
metric = 0.032                # 点击率
print(type(metric))           # -> <class 'float'>
metric = "click_rate"
print(type(metric))           # -> <class 'str'>
metric = [0.032, 0.028, 0.041]
print(type(metric))           # -> <class 'list'>

# 【动手改】把 metric = [0.032, 0.028, 0.041] 改成 metric = 3，重新运行看会怎样。

# ==== 3. 命名规则与惯例 ====
# 为什么：名字写错会直接语法错误，团队里还要有统一的命名习惯。
# 是什么：标识符 (identifier) 由字母、数字、下划线组成，不能以数字开头，
#         区分大小写，并且不能是关键字 (keyword)。
valid_name = 1        # 合法：字母 + 下划线
_name2 = 2            # 合法：下划线开头
ClickRate = 3         # 合法，但不符合惯例，PEP 8 建议全小写
# 2clicks = 4        会报 SyntaxError: invalid syntax（不能数字开头）
# click-rate = 4     会报 SyntaxError（中划线会被当成减号）
# class = 4          会报 SyntaxError: invalid syntax（class 是关键字）

print(keyword.kwlist)             # -> ['False', 'None', 'True', 'and', 'as', ...] 共 35 个
print("关键字个数:", len(keyword.kwlist))   # -> 关键字个数: 35

clicks = 1000
CLICKS = 2000         # 大小写不同，就是两个不同的名字
print(clicks, CLICKS)             # -> 1000 2000

MAX_CLICKS = 5000     # 惯例：常量全大写 + 下划线
click_rate = 0.032    # 惯例：普通变量用 snake_case（小写 + 下划线）
print("MAX_CLICKS =", MAX_CLICKS)         # -> MAX_CLICKS = 5000

# 【动手改】把 valid_name 改成 validName，重新运行（不报错，但它不符合 PEP 8）。

# ==== 4. 内置类型一览 ====
# 为什么：数据长什么样，决定了你能对它做什么运算。
# 是什么：下面每一行都是一个对象，type() 直接告诉你它的类型。
impressions = 1200                        # int：整数，曝光量
ctr = 0.032                               # float：小数，点击率
product = "夏季促销"                       # str：字符串
is_running = True                         # bool：布尔值
logo = None                               # NoneType：空值，表示「还没有」
daily = [1200, 980, 1430]                 # list：列表，有序、可修改
rgb = (255, 128, 0)                       # tuple：元组，有序、不可修改
student = {"name": "小明", "score": 88}    # dict：字典，键值对
channels = {"微博", "抖音"}                # set：集合，不重复、无序

print(type(impressions))                  # -> <class 'int'>
print(type(ctr))                          # -> <class 'float'>
print(type(product))                      # -> <class 'str'>
print(type(is_running))                   # -> <class 'bool'>
print(type(logo))                         # -> <class 'NoneType'>
print(type(daily))                        # -> <class 'list'>
print(type(rgb))                          # -> <class 'tuple'>
print(type(student))                      # -> <class 'dict'>
print(type(channels))                     # -> <class 'set'>

# 【动手改】把 daily 改成 (1200, 980, 1430)，重新运行看 type() 变成了什么。

# ==== 5. 多重赋值与解包 ====
# 为什么：一次给多个名字赋值，比写好几行更短，也更不容易漏改。
# 是什么：右边全部算完之后，再按位置一一绑定到左边的名字。
impressions, clicks = 2000, 80
print("曝光量:", impressions, "点击量:", clicks)          # -> 曝光量: 2000 点击量: 80

clicks, impressions = impressions, clicks   # 交换：右边先算成元组 (2000, 80)，再分别绑定
print("曝光量:", impressions, "点击量:", clicks)          # -> 曝光量: 80 点击量: 2000

first_week, *rest_weeks = [120, 135, 128, 150]   # * 收集剩下的全部
print(first_week)                                        # -> 120
print(rest_weeks)                                        # -> [135, 128, 150]

mon, _, fri = 12, 15, 20     # _ 是惯例，表示「这个值我不要」
print(mon, fri)                                          # -> 12 20
# a, b = 1, 2, 3            会报 ValueError: too many values to unpack (expected 2)

# 【动手改】把 first_week, *rest_weeks 改成 first_week, rest_weeks，重新运行看会怎样。

# ==== 6. 可变与不可变 ====
# 为什么：当两个名字指向同一份数据时，改一个会不会影响另一个，取决于数据能不能就地修改。
# 是什么：int/float/str/tuple 不可变 (immutable)，list/dict/set 可变 (mutable)。

a = 10
b = a
a = a + 1        # a 指向了一个新对象 11，b 还指向原来的 10
print(a, b)                                              # -> 11 10

title = "夏季"
title_copy = title
title = title + "促销"    # 字符串不可改，这里生成了新字符串
print(title_copy, title)                                 # -> 夏季 夏季促销

campaigns = ["搜索", "信息流"]
other = campaigns        # 没有复制，两个名字指向同一个 list
other.append("开屏")
print(campaigns)                                         # -> ['搜索', '信息流', '开屏']
print(id(campaigns) == id(other))                        # -> True

safe_copy = list(campaigns)   # 想拿到独立的一份，就显式复制
safe_copy.append("banner")
print(campaigns)                                         # -> ['搜索', '信息流', '开屏']
print(safe_copy)                                         # -> ['搜索', '信息流', '开屏', 'banner']

# 想判断两个名字是不是同一个对象？下一节 02_operators.py 讲 `is` 和 `==`。

# 【动手改】把 other.append("开屏") 改成 other = ["开屏"]，重新运行看会怎样。

# ==== 7. 类型转换 ====
# 为什么：从输入或文件里读到的数字其实都是字符串，要算数就得先转成数字。
# 是什么：把类型名当函数调用，就得到一个新类型的对象。
clicks_str = "1200"
clicks_int = int(clicks_str)
print(clicks_int + 1)          # -> 1201
print(type(clicks_int))        # -> <class 'int'>
# int("12.5")                会报 ValueError: invalid literal for int() with base 10: '12.5'
# int("abc")                 会报 ValueError: invalid literal for int() with base 10: 'abc'
# float("abc")               会报 ValueError: could not convert string to float: 'abc'
print(int(float("12.5")))      # -> 12   先转 float 再取整（截断，不四舍五入）

print(float("0.032"))          # -> 0.032
print(str(1200) + "%")         # -> 1200%   字符串相加是拼接
print(type(str(1200)))         # -> <class 'str'>

print(bool(""), bool(0), bool([]), bool(None))    # -> False False False False
print(bool("0"), bool(-1), bool("False"))         # -> True True True   非空字符串都算 True

# 【动手改】把 print(int(float("12.5"))) 改成 print(float("12.5"))，重新运行看有什么不同。

# ==== 8. f-string 快速上手 ====
# 为什么：用 + 拼字符串很啰嗦，f-string 可以直接把变量塞进句子里并顺手格式化。
# 是什么：字符串前加 f，里面用 {} 放变量或表达式，冒号后面写格式。
product = "夏日冰饮"
price = 19.9
rate = 0.0325
print(f"商品：{product}，价格：{price:.2f} 元")    # -> 商品：夏日冰饮，价格：19.90 元
print(f"点击率：{rate:.2%}")                      # -> 点击率：3.25%
print(f"{product=}")                              # -> product='夏日冰饮'
print(f"曝光加点击：{1200 + 300}")                 # -> 曝光加点击：1500
# product = input("请输入商品名：")               会停下来等你敲键盘，所以这里只写不做

# 【动手改】把 {rate:.2%} 改成 {rate:.1%}，重新运行看会怎样。

# ===== 练习 =====
# 1. 建三个变量：ad_name = "开学季"，impressions = 50000，clicks = 1250，
#    再用一个 f-string 一次打印「广告 开学季：曝光 50000，点击 1250」。
#    验证方式：屏幕上出现  广告 开学季：曝光 50000，点击 1250
# 2. 计算点击率 ctr = clicks / impressions，用 f-string 保留 2 位小数并按百分比打印。
#    验证方式：屏幕上出现  2.50%
# 3. 用一次多重赋值交换 impressions 和 clicks，交换前后各打印一次这两个值。
#    验证方式：第一次打印 50000 1250，交换后打印 1250 50000
# 4. 先自己猜哪些是 False，再打印验证：bool(0.0)、bool(" ")、bool([])、bool(None)、bool(0)
#    验证方式：bool(0.0)、bool([])、bool(None)、bool(0) 都是 False；bool(" ") 是 True（空格也是字符）

# ===== 参考答案（建议先自己写一遍）=====
print("=" * 50)

# 第 1 题
ad_name = "开学季"
impressions = 50000
clicks = 1250
print(f"广告 {ad_name}：曝光 {impressions}，点击 {clicks}")   # -> 广告 开学季：曝光 50000，点击 1250

# 第 2 题
ctr = clicks / impressions
print(f"{ctr:.2%}")                                          # -> 2.50%

# 第 3 题
print(impressions, clicks)                                   # -> 50000 1250
impressions, clicks = clicks, impressions
print(impressions, clicks)                                   # -> 1250 50000

# 第 4 题
print(bool(0.0), bool(" "), bool([]), bool(None), bool(0))    # -> False True False False False
