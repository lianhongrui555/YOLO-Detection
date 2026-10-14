# 导入 argparse，用来支持测试参数。
import argparse

# 导入 sys，用来把 advanced 目录加入模块搜索路径。
import sys

# 导入 threading，用来在后台线程运行 Flask 服务器。
import threading

# 导入 time，用来做健康检查等待。
import time

# 导入 Path，用来定位项目目录。
from pathlib import Path

# 导入 urllib.request，用来检查服务是否已经启动。
import urllib.request

# 导入 webview，用来创建桌面窗口。
import webview

# 导入 make_server，用来在桌面程序内启动 Flask。
from werkzeug.serving import make_server

# 取得仓库根目录和 advanced 目录。
project_dir = Path(__file__).resolve().parent
advanced_dir = project_dir / "advanced"

# 把 advanced 目录加入导入路径，以便导入 web_app_v2。
sys.path.insert(0, str(advanced_dir))

# 导入已经加载好 YOLO 模型和 Flask 路由的应用对象。
from web_app_v2 import app


def start_server():
    """在后台线程启动 Flask，并返回服务器对象和随机端口。"""
    server = make_server("127.0.0.1", 0, app)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, port


def wait_health(port: int, timeout: int = 60) -> bool:
    """等待 Flask 健康检查通过。"""
    url = f"http://127.0.0.1:{port}/health"
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                if response.status == 200:
                    return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    """启动 YOLO 桌面窗口。"""
    parser = argparse.ArgumentParser(description="YOLO 实时检测桌面应用")
    parser.add_argument("--smoke-test", action="store_true", help="只启动服务并检查健康接口")
    args = parser.parse_args()

    server, port = start_server()
    try:
        if not wait_health(port):
            raise RuntimeError("YOLO 服务在规定时间内没有启动成功。")

        if args.smoke_test:
            print(f"YOLO_DESKTOP_SMOKE_OK port={port}")
            return

        webview.create_window(
            title="YOLO 实时检测 V2",
            url=f"http://127.0.0.1:{port}/",
            width=1280,
            height=860,
            min_size=(900, 650),
            text_select=True,
        )
        webview.start()
    finally:
        server.shutdown()


if __name__ == "__main__":
    main()