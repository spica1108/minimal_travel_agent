from dataclasses import dataclass


@dataclass
class TripRequest:
    departure: str
    destination: str
    days: int
    budget: int
    style: str


DESTINATION_TIPS = {
    "日本": ["东京", "京都", "大阪"],
    "泰国": ["曼谷", "清迈", "普吉岛"],
    "韩国": ["首尔", "釜山", "济州岛"],
}


def recommend_destination(request: TripRequest) -> str:
    cities = DESTINATION_TIPS.get(request.destination, [request.destination])
    city_list = "、".join(cities)
    return f"推荐目的地：{city_list}。根据你的偏好「{request.style}」，建议主打 {cities[0]}。"


def estimate_budget(request: TripRequest) -> str:
    flight = 2200
    hotel = request.days * 550
    food = request.days * 220
    activities = request.days * 260
    total = flight + hotel + food + activities
    status = "预算充足" if total <= request.budget else "预算偏紧"
    return (
        f"预算估算：机票 {flight} 元，酒店 {hotel} 元，餐饮 {food} 元，"
        f"活动 {activities} 元，总计约 {total} 元。结论：{status}。"
    )


def build_itinerary(request: TripRequest) -> str:
    plan = []
    for day in range(1, request.days + 1):
        if day == 1:
            plan.append(f"Day {day}: 从{request.departure}出发，抵达后入住酒店，晚上轻松逛街。")
        elif day == request.days:
            plan.append(f"Day {day}: 上午补逛或买伴手礼，下午返程。")
        else:
            plan.append(f"Day {day}: 安排一个核心景点，加一个本地美食区域，节奏按「{request.style}」来。")
    return "\n".join(plan)
