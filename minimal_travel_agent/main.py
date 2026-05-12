# main.py 是这个项目的“agent 大脑”。
#
# 你可以先这样理解：
# - tools.py 负责提供工具，比如推荐目的地、估算预算、生成行程
# - main.py 负责决定什么时候调用哪个工具
#
# 这个文件里最重要的是 run_agent_from_request()。
# 它里面的 while True 就是一个最小版 agent loop。


# import 表示“引入别的代码”。
# re 是 Python 自带的正则表达式模块，用来从文字里提取信息。
# 这里会用它从用户输入里找 “5天” 和 “预算8000”。
import re

# from tools import ... 表示从 tools.py 文件里拿这些东西来用。
# TripRequest 是旅行需求的数据结构。
# build_itinerary / estimate_budget / recommend_destination 是三个工具函数。
from tools import TripRequest, build_itinerary, estimate_budget, recommend_destination


def parse_request(user_input: str) -> TripRequest:
    # def 表示定义函数。
    #
    # parse_request 这个函数的作用是：
    # 把用户输入的一句话，整理成 TripRequest 这种结构化数据。
    #
    # user_input: str 表示参数 user_input 应该是字符串。
    # -> TripRequest 表示这个函数最后会返回一个 TripRequest。

    # re.search(...) 会在 user_input 这段文字里搜索符合规则的内容。
    #
    # r"(\d+)\s*天" 是一个正则表达式：
    # \d+ 表示一个或多个数字，比如 5、10
    # \s* 表示可能有空格，也可能没有空格
    # 天 表示文字里要出现“天”
    #
    # 所以它可以匹配：
    # "5天"
    # "5 天"
    days_match = re.search(r"(\d+)\s*天", user_input)

    # 这一行用来找预算。
    # r"预算\s*(\d+)" 可以匹配：
    # "预算8000"
    # "预算 8000"
    budget_match = re.search(r"预算\s*(\d+)", user_input)

    # 先给目的地一个默认值。
    # 如果用户没有写目的地，就默认用“日本”。
    destination = "日本"

    # for 表示循环。
    # 这里会依次检查 ["日本", "泰国", "韩国"] 里的每一个地方。
    for place in ["日本", "泰国", "韩国"]:
        # if 表示如果。
        # place in user_input 的意思是：
        # 如果用户输入里包含这个地方。
        if place in user_input:
            # 找到了，就把 destination 改成这个地方。
            destination = place

            # break 表示结束循环。
            # 既然已经找到目的地，就不用继续往下找了。
            break

    # return 表示返回结果。
    # 这里创建一个 TripRequest，把解析出来的信息放进去。
    return TripRequest(
        # 目前出发地先固定为上海。
        # 后面我们可以继续升级，让它也从用户输入里解析。
        departure="上海",

        # destination 是上面解析出来的目的地。
        destination=destination,

        # days_match.group(1) 表示拿到正则里第一组括号匹配到的内容。
        # 比如用户输入 "5天"，group(1) 就是 "5"。
        #
        # int(...) 会把字符串转成整数。
        # "5" -> 5
        #
        # if days_match else 5 是 Python 的简写：
        # 如果找到了天数，就用用户写的天数；
        # 否则默认用 5。
        days=int(days_match.group(1)) if days_match else 5,

        # 预算同理：
        # 找到了预算就用用户写的预算；
        # 没找到就默认 8000。
        budget=int(budget_match.group(1)) if budget_match else 8000,

        # 如果用户输入里包含“轻松”，就用轻松风格；
        # 否则默认经典景点优先。
        style="轻松、不赶路、喜欢美食和城市散步" if "轻松" in user_input else "经典景点优先",
    )


def decide_next_step(done_steps: set[str]) -> str:
    # 这个函数用来决定 agent 下一步该做什么。
    #
    # done_steps 是一个 set，中文可以叫“集合”。
    # 它用来记录哪些步骤已经做过。
    #
    # set 和 list 有点像，但 set 更适合用来判断“某个东西是否已经存在”。

    # 如果还没有做过 destination 这一步，就返回 "destination"。
    if "destination" not in done_steps:
        return "destination"

    # 如果目的地已经推荐过，但预算还没估算，就返回 "budget"。
    if "budget" not in done_steps:
        return "budget"

    # 如果预算也估算过，但行程还没生成，就返回 "itinerary"。
    if "itinerary" not in done_steps:
        return "itinerary"

    # 如果上面三步都做完了，就返回 "final"，表示可以结束。
    return "final"


def run_agent_with_trace(request: TripRequest) -> dict:
    # 这个函数和 run_agent_from_request 很像。
    #
    # 区别是：
    # run_agent_from_request 只返回最终结果字符串；
    # run_agent_with_trace 会同时返回：
    # - result: 最终结果
    # - traces: agent 每一步做了什么
    #
    # 这样前端页面就能显示 agent 的执行过程。
    done_steps: set[str] = set()
    notes: list[str] = []
    traces: list[str] = []

    while True:
        next_step = decide_next_step(done_steps)

        if next_step == "destination":
            traces.append("Step 1: 调用 recommend_destination 工具，推荐目的地。")
            notes.append(recommend_destination(request))
            done_steps.add("destination")
            continue

        if next_step == "budget":
            traces.append("Step 2: 调用 estimate_budget 工具，估算预算是否足够。")
            notes.append(estimate_budget(request))
            done_steps.add("budget")
            continue

        if next_step == "itinerary":
            traces.append("Step 3: 调用 build_itinerary 工具，生成每日行程。")
            notes.append("行程草案：\n" + build_itinerary(request))
            done_steps.add("itinerary")
            continue

        traces.append("Step 4: 所有工具调用完成，汇总最终答案。")
        break

    return {
        "result": "\n\n".join(notes),
        "traces": traces,
    }


def run_agent_from_request(request: TripRequest) -> str:
    # 这是整个项目最核心的函数。
    #
    # 它接收一个已经整理好的旅行需求 request，
    # 然后像 agent 一样：
    # 1. 判断下一步要做什么
    # 2. 调用对应工具
    # 3. 记录工具结果
    # 4. 继续判断下一步
    # 5. 最后输出完整结果

    # 这里复用 run_agent_with_trace，避免把 agent loop 写两遍。
    # ["result"] 表示从返回的字典里取最终结果。
    return run_agent_with_trace(request)["result"]

def run_agent(user_input: str) -> str:
    # 这个函数是给命令行版本用的。
    #
    # 它做两件事：
    # 1. parse_request(user_input)：把用户输入文字变成 TripRequest
    # 2. run_agent_from_request(...)：运行 agent 主流程
    return run_agent_from_request(parse_request(user_input))


if __name__ == "__main__":
    # 这行是 Python 常见写法，意思是：
    # 只有当你直接运行 python main.py 时，下面代码才会执行。
    #
    # 如果别的文件 import main.py，下面代码不会自动执行。

    # input(...) 会在终端里等待用户输入。
    # 用户输入完成并按回车后，内容会保存到 task 变量里。
    task = input("请输入旅行需求：")

    # print(...) 表示在终端输出文字。
    print("\nAgent 正在规划...\n")

    # run_agent(task) 会真正启动 agent。
    # 最外层 print 会把 agent 的最终结果输出到终端。
    print(run_agent(task))
