import json
import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080


def parse_request(request_text):
    """Split raw HTTP request text into method, path, headers, and body."""
    head, _, body = request_text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, path, _version = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if ":" in line:
            key, _, value = line.partition(":")
            headers[key.strip().lower()] = value.strip()

    return method, path, headers, body


def make_response(status_code, status_text, content_type, body_bytes):
    headers = (
        f"HTTP/1.1 {status_code} {status_text}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body_bytes


def html_response(html):
    return make_response(200, "OK", "text/html; charset=utf-8", html.encode("utf-8"))


def json_response(data, status_code=200, status_text="OK"):
    body = json.dumps(data).encode("utf-8")
    return make_response(status_code, status_text, "application/json", body)


def route(method, path, headers, body):
    """The routing table: decide what to send back based on method + path."""

    if method == "GET" and path == "/":
        return html_response(
            "<html><body><h1>Welcome</h1>"
            "<p>Socket HTTP server. Try /about, /api/time, /api/status.</p>"
            "</body></html>"
        )

    if method == "GET" and path == "/about":
        return html_response(
            "<html><body><h1>About</h1>"
            "<p>Built with Python's socket module for GIT Plus Ltd internship.</p>"
            "</body></html>"
        )

    if method == "GET" and path == "/api/time":
        return json_response({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

    if method == "GET" and path == "/api/status":
        return json_response({"status": "ok", "server": "socket-http-server"})

    if method == "POST" and path == "/api/echo":
        # Try to parse the posted body as JSON; fall back to raw text
        try:
            parsed = json.loads(body) if body else {}
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return json_response({"you_sent": parsed})

    # No route matched
    return json_response({"error": "Not Found", "path": path}, 404, "Not Found")


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Running at http://{HOST}:{PORT}/  (Ctrl+C to stop)")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request_data = client_socket.recv(4096)
                if not request_data:
                    continue

                request_text = request_data.decode("utf-8", errors="replace")
                method, path, headers, body = parse_request(request_text)
                print(f"[SERVER] {method} {path}")

                response = route(method, path, headers, body)
                client_socket.sendall(response)
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
