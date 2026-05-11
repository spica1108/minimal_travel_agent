from tools import TripRequest, build_itinerary, estimate_budget, recommend_destination


def parse_request(user_input: str) -> TripRequest:
    """先用固定示例解析，避免一开始被自然语言解析复杂度卡住。"""
    return TripRequest(
        departure="上海",
        destination="日本",
        days=5,
        budget=8000,
        style="轻松、不赶路、喜欢美食和城市散步",
    )


def decide_next_step(done_steps: set[str]) -> str:
    if "destination" not in done_steps:
        return "destination"
    if "budget" not in done_steps:
        return "budget"
    if "itinerary" not in done_steps:
        return "itinerary"
    return "final"


def run_agent(user_input: str) -> str:
    request = parse_request(user_input)
    done_steps: set[str] = set()
    notes: list[str] = []

    while True:
        next_step = decide_next_step(done_steps)

        if next_step == "destination":
            notes.append(recommend_destination(request))
            done_steps.add("destination")
            continue

        if next_step == "budget":
            notes.append(estimate_budget(request))
            done_steps.add("budget")
            continue

        if next_step == "itinerary":
            notes.append("行程草案：\n" + build_itinerary(request))
            done_steps.add("itinerary")
            continue

        break

    return "\n\n".join(notes)


if __name__ == "__main__":
    task = input("请输入旅行需求：")
    print("\nAgent 正在规划...\n")
    print(run_agent(task))
