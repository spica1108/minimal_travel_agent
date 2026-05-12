# dataclass 是 Python 自带的一个小工具。
# 它可以帮我们快速创建“只用来存数据的类”。
# 这里的 TripRequest 就是用来保存一次旅行需求的数据。
from dataclasses import dataclass


@dataclass
class TripRequest:
    # 下面这 5 行叫“字段”。
    # 冒号后面的 str / int 是类型提示：
    # str 表示字符串，比如 "上海"、"日本"
    # int 表示整数，比如 5、8000
    departure: str
    destination: str
    days: int
    budget: int
    style: str


# 这是一个字典 dict。
# 你可以把它理解成 JavaScript 里的 object。
# 左边是国家/地区，右边是推荐城市列表。
DESTINATION_TIPS = {
    "日本": ["东京", "京都", "大阪"],
    "泰国": ["曼谷", "清迈", "普吉岛"],
    "韩国": ["首尔", "釜山", "济州岛"],
}


def recommend_destination(request: TripRequest) -> str:
    # 这是“推荐目的地工具”。
    # 参数 request 是 TripRequest，也就是用户的旅行需求。
    # -> str 表示这个函数最后会返回一个字符串。

    # 从 DESTINATION_TIPS 里按目的地查城市。
    # 例如 request.destination 是 "日本"，就会拿到 ["东京", "京都", "大阪"]。
    # 如果字典里找不到，就用 [request.destination] 当默认值。
    cities = DESTINATION_TIPS.get(request.destination, [request.destination])

    # "、".join(...) 会把列表拼成一个字符串。
    # 例如 ["东京", "京都", "大阪"] 会变成 "东京、京都、大阪"。
    city_list = "、".join(cities)

    # f"..." 是 Python 的格式化字符串，类似 JS 里的模板字符串 `${}`。
    # {city_list} 会被替换成变量 city_list 的值。
    # cities[0] 表示城市列表里的第一个城市。
    return f"推荐目的地：{city_list}。根据你的偏好「{request.style}」，建议主打 {cities[0]}。"


def estimate_budget(request: TripRequest) -> str:
    # 这是“预算估算工具”。
    # 现在先用固定规则估算：
    # 机票固定 2200 元，酒店/餐饮/活动按旅行天数计算。

    flight = 2200
    hotel = request.days * 550
    food = request.days * 220
    activities = request.days * 260

    # 把几项费用加起来，得到总预算。
    total = flight + hotel + food + activities

    # 这是 Python 的三元表达式，类似 JS 里的：
    # total <= request.budget ? "预算充足" : "预算偏紧"
    status = "预算充足" if total <= request.budget else "预算偏紧"

    # return 后面用括号包起来，是为了把很长的字符串拆成多行写。
    # Python 会自动把相邻的字符串拼起来。
    return (
        f"预算估算：机票 {flight} 元，酒店 {hotel} 元，餐饮 {food} 元，"
        f"活动 {activities} 元，总计约 {total} 元。结论：{status}。"
    )


def build_itinerary(request: TripRequest) -> str:
    # 这是“行程生成工具”。
    # 它会根据旅行天数，生成 Day 1、Day 2、Day 3... 这样的每日安排。

    # plan 是一个列表 list，用来一条一条保存每天的安排。
    plan = []

    # range(1, request.days + 1) 会生成从 1 到 days 的数字。
    # 如果 days 是 5，这里会依次得到 1、2、3、4、5。
    # 注意：Python 的 range 右边是不包含的，所以要写 days + 1。
    for day in range(1, request.days + 1):
        # 第一天：通常是出发和入住，所以安排轻一点。
        if day == 1:
            plan.append(f"Day {day}: 从{request.departure}出发，抵达后入住酒店，晚上轻松逛街。")

        # 最后一天：通常要返程，所以安排补逛和回家。
        elif day == request.days:
            plan.append(f"Day {day}: 上午补逛或买伴手礼，下午返程。")

        # 中间几天：安排景点和美食。
        else:
            plan.append(f"Day {day}: 安排一个核心景点，加一个本地美食区域，节奏按「{request.style}」来。")

    # "\n".join(plan) 会把列表里的每天安排拼成一段文字。
    # \n 表示换行。
    return "\n".join(plan)
