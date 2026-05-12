import re

from tools import TripRequest, build_itinerary, estimate_budget, recommend_destination


def parse_request(user_input: str) -> TripRequest:
    days_match = re.search(r"(\d+)\s*天", user_input)
    budget_match = re.search(r"预算\s*(\d+)", user_input)
    destination = "日本"

    for place in ["日本", "泰国", "韩国"]:
        if place in user_input:
            destination = place
            break

    return TripRequest(
        departure="上海",
        destination=destination,
        days=int(days_match.group(1)) if days_match else 5,
        budget=int(budget_match.group(1)) if budget_match else 8000,
        style="轻松、不赶路、喜欢美食和城市散步" if "轻松" in user_input else "经典景点优先",
    )


def decide_next_step(done_steps: set[str]) -> str:
    if "destination" not in done_steps:
        return "destination"
    if "budget" not in done_steps:
        return "budget"
    if "itinerary" not in done_steps:
        return "itinerary"
    return "final"


def run_agent_from_request(request: TripRequest) -> str:
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


def run_agent(user_input: str) -> str:
    return run_agent_from_request(parse_request(user_input))


if __name__ == "__main__":
    task = input("请输入旅行需求：")
    print("\nAgent 正在规划...\n")
    print(run_agent(task))
