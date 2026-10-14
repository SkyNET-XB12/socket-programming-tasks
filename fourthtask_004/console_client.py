import json
import socket

HOST = "127.0.0.1"
PORT = 8080

# Predefined paths the assignment asks us to demonstrate
MENU = [
    ("GET",  "/",           None),
    ("GET",  "/about",      None),
    ("GET",  "/api/time",   None),
    ("GET",  "/api/status", None),
    ("POST", "/api/echo",   {"note": "hello from console client"}),
]


def send_request(method, path, json_body=None):
    """Build a raw HTTP request by hand and send it over a stream socket."""
    body_bytes = b""
    extra_headers = ""

    if json_body is not None:
        body_bytes = json.dumps(json_body).encode("utf-8")
        extra_headers = (
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(body_bytes)}\r\n"
        )

    request = (
        f"{method} {path} HTTP/1.1\r\n"
        f"Host: {HOST}:{PORT}\r\n"
        f"{extra_headers}"
        "Connection: close\r\n"
        "\r\n"
    ).encode() + body_bytes

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(request)

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

    return response.decode("utf-8", errors="replace")


def display(raw_response):
    head, _, body = raw_response.partition("\r\n\r\n")
    status_line = head.split("\r\n")[0]
    print(f"\n--- Response ---\n{status_line}")

    if "application/json" in head:
        try:
            parsed = json.loads(body)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(body)
    else:
        print(body)
    print("----------------\n")


def main():
    while True:
        print("Choose a request to send:")
        for i, (method, path, _) in enumerate(MENU, start=1):
            print(f"  {i}. {method} {path}")
        print("  0. Quit")

        choice = input("> ").strip()
        if choice == "0":
            break

        try:
            index = int(choice) - 1
            method, path, json_body = MENU[index]
        except (ValueError, IndexError):
            print("Invalid choice.\n")
            continue

        raw_response = send_request(method, path, json_body)
        display(raw_response)


if __name__ == "__main__":
    main()
