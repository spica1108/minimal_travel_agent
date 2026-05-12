const form = document.querySelector("#plan-form");
const result = document.querySelector("#result");
const traces = document.querySelector("#traces");
const button = form.querySelector("button");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  button.textContent = "生成中...";
  result.textContent = "Agent 正在规划...";
  traces.innerHTML = "<li>等待 agent 调用工具...</li>";

  const data = Object.fromEntries(new FormData(form).entries());
  data.days = Number(data.days);
  data.budget = Number(data.budget);

  try {
    const response = await fetch("/api/plan", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });
    const payload = await response.json();
    result.textContent = payload.result;
    traces.innerHTML = payload.traces.map((trace) => `<li>${trace}</li>`).join("");
  } catch (error) {
    result.textContent = "生成失败，请检查服务是否还在运行。";
    traces.innerHTML = "<li>请求失败。</li>";
  } finally {
    button.disabled = false;
    button.textContent = "生成行程";
  }
});
