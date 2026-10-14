import socket
import threading

HOST = "127.0.0.1"
PORT = 5050


def receive_loop(client_socket, stop_event):
    """Runs in its own thread: prints whatever the server sends, until told to stop."""
    while not stop_event.is_set():
        try:
            data = client_socket.recv(1024)
        except OSError:
            break  # socket closed elsewhere

        if not data:
            print("[CLIENT] Server closed the connection.")
            stop_event.set()
            break

        print(f"[CLIENT] From server: {data.decode('utf-8')}")


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("[CLIENT] Connected. Type messages to send. Type 'stop' to disconnect.")

    stop_event = threading.Event()
    receiver = threading.Thread(target=receive_loop, args=(client_socket, stop_event))
    receiver.daemon = True
    receiver.start()

    # Main thread: read typed input and send it
    try:
        while not stop_event.is_set():
            message = input()
            if stop_event.is_set():
                break
            client_socket.send(message.encode("utf-8"))
            if message.strip() == "stop":
                stop_event.set()
                break
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        client_socket.close()
        print("[CLIENT] Connection closed.")


if __name__ == "__main__":
    main()
