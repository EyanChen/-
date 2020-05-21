# coding : utf-8
import socket


def main():
    sock = socket.socket()
    host = socket.gethostname()  # 拿到主机名
    port = 12312  # 定义端口

    sock.connect((host, port))
    sock.send("Hello server!".encode('utf-8'))

    with open("Received_file", "wb") as out_file:
        print("File opened")
        print("Receiving data...")
        while True:
            data = sock.recv(1024)
            print(f"data={data}")
            if not data:
                break
            out_file.write(data)  # 写数据

    print("Successfully got the file")
    sock.close()
    print("Connection closed")


if __name__ == '__main__':
    main()