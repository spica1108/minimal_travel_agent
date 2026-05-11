# Minimal Travel Agent

这是一个零依赖的 Python 迷你旅游 agent，用来理解 agent 的基本结构。

## 运行

```bash
cd minimal_travel_agent
python main.py
```

输入示例：

```text
帮我规划一个上海出发、5天、预算8000的日本旅行，想轻松一点
```

## 思路

这个版本故意不使用 LangChain、数据库、前端或真实 API。

它只保留 agent 最核心的结构：

```text
用户输入
  -> 解析需求
  -> 决定下一步
  -> 调用工具
  -> 保存工具结果
  -> 继续决定下一步
  -> 输出最终结果
```

对应代码：

- `main.py`: agent 循环和任务编排
- `tools.py`: 旅游相关工具，比如推荐目的地、估算预算、生成行程

后续可以把 `decide_next_step()` 换成真正的大模型调用。
