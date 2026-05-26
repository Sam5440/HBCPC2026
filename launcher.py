from __future__ import annotations

import socket
import threading
import time
import webbrowser

from web.app import SUBMISSIONS, app


def pick_port(start: int = 5000) -> int:
    for port in range(start, start + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                sock.bind(("127.0.0.1", port))
            except OSError:
                continue
            return port
    raise RuntimeError("No available local port found from 5000 to 5049.")


def open_browser(url: str) -> None:
    time.sleep(1.0)
    webbrowser.open(url)


def main() -> None:
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    port = pick_port()
    url = f"http://127.0.0.1:{port}/"
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    print(f"HBCPC Local Judge is running at {url}")
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
