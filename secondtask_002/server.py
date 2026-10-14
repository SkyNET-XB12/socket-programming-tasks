import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 5050


def send_datetime_loop(client_socket, stop_event):
    """Runs in its own thread: sends the current datetime every 20 seconds."""
    while not stop_event.is_set():
        # Wait up to 20s, but wake up early if stop_event gets set
        if stop_event.wait(timeout=20):
            break
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_socket.send(now.encode("utf-8"))
            print(f"[SERVER] Sent: {now}")
        except OSError:
            break  # socket already closed


def handle_client(client_socket, client_address):
    print(f"[SERVER] Connection from {client_address}")
    stop_event = threading.Event()

    # Start the background sender thread
    sender = threading.Thread(target=send_datetime_loop, args=(client_socket, stop_event))
    sender.daemon = True
    sender.start()

    # Main loop for THIS client: keep receiving until "stop"
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # client disconnected abruptly

            message = data.decode("utf-8").strip()
            print(f"[SERVER] Received: {message}")

            if message == "stop":
                print("[SERVER] 'stop' received. Closing connection.")
                break
    finally:
        stop_event.set()      # tell the sender thread to stop
        sender.join(timeout=1)
        client_socket.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[SERVER] Listening on {HOST}:{PORT} ... (Ctrl+C to stop)")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            handle_client(client_socket, client_address)
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
