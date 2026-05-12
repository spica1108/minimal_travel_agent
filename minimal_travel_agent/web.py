# web.py 是这个项目的“网页服务”。
#
# 你可以把它理解成：
# 浏览器页面 <-> web.py <-> main.py 里的 agent
#
# 它负责两件事：
# 1. 把 HTML / CSS / JS 文件发给浏览器，让你看到网页
# 2. 接收网页提交的旅行需求，调用 agent，然后把结果返回给网页


# json 是 Python 自带模块，用来处理 JSON 数据。
# JSON 是前后端传数据常用的格式，长得很像 JavaScript 对象：
# {"departure": "上海", "days": 5}
import json

# http.server 是 Python 自带的简单网页服务模块。
# BaseHTTPRequestHandler 用来处理浏览器请求。
# ThreadingHTTPServer 用来启动一个本地 HTTP 服务。
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Path 是 Python 里处理文件路径的工具。
# 比手写字符串路径更清楚，也更不容易出错。
from pathlib import Path

# 从 main.py 引入 agent 主流程函数。
# web.py 收到网页请求后，最终就是调用这个函数生成行程。
from main import run_agent_from_request

# 从 tools.py 引入 TripRequest。
# 前端传来的表单数据，会先整理成 TripRequest，再交给 agent。
from tools import TripRequest


# __file__ 表示当前这个文件 web.py 的路径。
# Path(__file__).parent 表示 web.py 所在的文件夹。
# 也就是 minimal_travel_agent 这个目录。
ROOT = Path(__file__).parent

# STATIC_DIR 表示前端静态文件所在目录：
# minimal_travel_agent/static
#
# / 是 Path 的路径拼接写法。
STATIC_DIR = ROOT / "static"


class TravelAgentHandler(BaseHTTPRequestHandler):
    # class 表示定义一个类。
    #
    # 这里 TravelAgentHandler 是“请求处理器”。
    # 浏览器每访问一次网页，Python 就会用这个类来处理请求。
    #
    # BaseHTTPRequestHandler 是 Python 提供的基础类。
    # 我们继承它，然后重写 do_GET 和 do_POST。

    def do_GET(self):
        # do_GET 用来处理 GET 请求。
        #
        # GET 一般表示“我要拿一个东西”。
        # 比如浏览器打开 http://127.0.0.1:8000
        # 就是在发 GET 请求。
        #
        # self.path 是浏览器请求的路径。
        # 例如：
        # /              首页
        # /index.html    HTML 文件
        # /styles.css    CSS 样式文件
        # /app.js        JS 文件

        # 如果访问的是首页 / 或 /index.html，
        # 就把 static/index.html 发给浏览器。
        if self.path in ["/", "/index.html"]:
            self._send_file(STATIC_DIR / "index.html", "text/html; charset=utf-8")
            return

        # 如果浏览器请求 /styles.css，
        # 就把 CSS 文件发给浏览器。
        if self.path == "/styles.css":
            self._send_file(STATIC_DIR / "styles.css", "text/css; charset=utf-8")
            return

        # 如果浏览器请求 /app.js，
        # 就把 JavaScript 文件发给浏览器。
        if self.path == "/app.js":
            self._send_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")
            return

        # 如果请求的路径上面都没匹配到，就返回 404。
        # 404 的意思是：这个资源不存在。
        self.send_error(404)

    def do_POST(self):
        # do_POST 用来处理 POST 请求。
        #
        # POST 一般表示“我要提交一些数据”。
        # 在这个项目里，前端点击“生成行程”时，
        # app.js 会把表单数据 POST 到 /api/plan。

        # 如果 POST 的路径不是 /api/plan，
        # 说明不是我们支持的接口，返回 404。
        if self.path != "/api/plan":
            self.send_error(404)
            return

        # 浏览器提交 JSON 数据时，请求体里会有内容。
        # Content-Length 表示请求体有多少字节。
        #
        # self.headers.get("Content-Length", "0") 的意思是：
        # 从请求头里拿 Content-Length；
        # 如果没有，就默认用 "0"。
        #
        # int(...) 把字符串转成数字。
        length = int(self.headers.get("Content-Length", "0"))

        # self.rfile.read(length) 会读取请求体里的原始数据。
        # decode("utf-8") 把字节转换成字符串。
        # json.loads(...) 把 JSON 字符串转换成 Python 字典 dict。
        #
        # payload 最后大概长这样：
        # {
        #   "departure": "上海",
        #   "destination": "日本",
        #   "days": 5,
        #   "budget": 8000,
        #   "style": "轻松、不赶路"
        # }
        payload = json.loads(self.rfile.read(length).decode("utf-8"))

        # 把前端传来的 payload 字典，整理成 TripRequest。
        #
        # payload.get("departure", "上海") 的意思是：
        # 取 departure 这个字段；
        # 如果没有，就用默认值 "上海"。
        request = TripRequest(
            departure=payload.get("departure", "上海"),
            destination=payload.get("destination", "日本"),
            days=int(payload.get("days", 5)),
            budget=int(payload.get("budget", 8000)),
            style=payload.get("style", "轻松、不赶路、喜欢美食和城市散步"),
        )

        # 这里是真正调用 agent 的地方。
        # run_agent_from_request 在 main.py 里定义。
        #
        # web.py 本身不负责规划，它只是把数据交给 agent。
        result = run_agent_from_request(request)

        # 把 agent 生成的结果包装成 JSON 返回给前端。
        # 前端 app.js 会拿到 result，然后显示在页面上。
        self._send_json({"result": result})

    def log_message(self, format, *args):
        # 默认情况下，Python HTTP server 会在终端打印很多访问日志。
        # 这里重写 log_message，并且什么都不做，
        # 是为了让终端输出更干净。
        #
        # *args 表示可以接收任意数量的额外参数。
        return

    def _send_file(self, path: Path, content_type: str):
        # 这是我们自己写的辅助方法。
        # 方法名前面的 _ 表示：
        # 这个方法主要给类内部自己用，不是给外面直接调用的。

        # read_bytes() 会把文件内容读取成字节。
        # 网页服务最终发送给浏览器的就是字节。
        content = path.read_bytes()

        # send_response(200) 表示请求成功。
        # HTTP 状态码 200 的意思就是 OK。
        self.send_response(200)

        # Content-Type 告诉浏览器：
        # 我返回的是什么类型的文件。
        # 例如 text/html、text/css、application/javascript。
        self.send_header("Content-Type", content_type)

        # Content-Length 告诉浏览器：
        # 这次返回的内容有多少字节。
        self.send_header("Content-Length", str(len(content)))

        # end_headers() 表示响应头写完了。
        # 接下来就开始写真正的文件内容。
        self.end_headers()

        # wfile.write(...) 把文件内容写回给浏览器。
        self.wfile.write(content)

    def _send_json(self, data: dict):
        # 这是另一个辅助方法，用来返回 JSON 数据。
        #
        # data: dict 表示参数 data 应该是一个字典。

        # json.dumps(...) 把 Python 字典转换成 JSON 字符串。
        #
        # ensure_ascii=False 表示中文不要转成 \u4e0a 这种编码，
        # 而是保持可读的中文。
        #
        # encode("utf-8") 把字符串转换成字节，方便通过 HTTP 返回。
        content = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def main():
    # 这是启动网页服务的函数。
    #
    # ("127.0.0.1", 8000) 表示服务地址：
    # 127.0.0.1 是本机地址，只能在你自己的电脑访问。
    # 8000 是端口号。
    #
    # TravelAgentHandler 表示：
    # 所有请求都交给上面这个类来处理。
    server = ThreadingHTTPServer(("127.0.0.1", 8000), TravelAgentHandler)

    # 打印访问地址，方便你知道去浏览器打开哪里。
    print("Travel Agent web app: http://127.0.0.1:8000")

    # serve_forever() 表示服务一直运行。
    # 只要这个命令行窗口不关，网页就能访问。
    #
    # 按 Ctrl + C 可以停止服务。
    server.serve_forever()


if __name__ == "__main__":
    # 只有直接运行 python web.py 时，才会执行 main()。
    # 如果别的文件 import web.py，这里不会自动启动服务。
    main()
