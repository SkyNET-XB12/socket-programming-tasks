import socket
from datetime import datetime

HOST = "127.0.0.1"
PORT = 8080


def build_response(request_text):
    """Parse the request line and build a valid HTTP/1.1 response."""
    # The request's first line looks like: "GET /path HTTP/1.1"
    request_line = request_text.split("\r\n")[0]
    print(f"[SERVER] Request line: {request_line}")

    parts = request_line.split()
    method = parts[0] if len(parts) > 0 else ""
    path = parts[1] if len(parts) > 1 else "/"

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = (
        "<html><body>"
        f"<h1>Hello from the socket HTTP server!</h1>"
        f"<p>Method: {method}</p>"
        f"<p>Path: {path}</p>"
        f"<p>Server time: {now}</p>"
        "</body></html>"
    )
    body_bytes = body.encode("utf-8")

    # An HTTP response = status line + headers + blank line + body
    headers = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/html; charset=utf-8\r\n"
        f"Content-Length: {len(body_bytes)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    return headers.encode("utf-8") + body_bytes


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] HTTP server running at http://{HOST}:{PORT}/  (Ctrl+C to stop)")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request_data = client_socket.recv(4096)
                if not request_data:
                    continue

                request_text = request_data.decode("utf-8", errors="replace")
                response = build_response(request_text)
                client_socket.sendall(response)
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
