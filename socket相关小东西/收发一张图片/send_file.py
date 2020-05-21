import socket


def main():
    ONE_CONNECTION_ONLY = (
        True  # 如果希望继续接受连接，请将此设置为False
    )

    filename = "123.png"
    port = 12312  # Reserve a port for your service.
    sock = socket.socket()  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    sock.bind((host, port))  # Bind to the port
    sock.listen(5)  # Now wait for client connection.

    print("Server listening....")

    while True:
        conn, addr = sock.accept()  # Establish connection with client.
        print(f"Got connection from {addr}")
        data = conn.recv(1024)
        print(f"Server received {data}")

        with open(filename, "rb") as in_file:
            data = in_file.read(1024)
            while data:
                conn.send(data)
                print(f"Sent {data!r}")
                data = in_file.read(1024)

        print("Done sending")
        conn.close()
        if (
                ONE_CONNECTION_ONLY
        ):  # 测试用,ONE_CONNECTION_ONLY 为 True,就接收一次数据,跳出
            break

    sock.shutdown(1)
    sock.close()


if __name__ == '__main__':
    main()
