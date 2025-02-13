import socket
import threading
import struct

# STUN 消息类型
BINDING_REQUEST = 0x0001
BINDING_RESPONSE = 0x0101
MAGIC_COOKIE = 0x2112A442
PORT = 5000
def handle_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', PORT))
    print("STUN UDP服务器正在运行，监听端口5000")

    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(f"收到来自{addr}的UDP数据")

        if len(data) >= 20:
            msg_type, msg_length, msg_magic, trans_id = struct.unpack('!HHI12s', data[:20])
            if msg_type == BINDING_REQUEST and msg_magic == MAGIC_COOKIE:
                response = struct.pack('!HHI12s', BINDING_RESPONSE, 8, msg_magic, trans_id)

                family = 0x01  # IPv4
                port = addr[1]
                ip_addr = struct.unpack("!I", socket.inet_aton(addr[0]))[0]

                mapped_addr = struct.pack('!HHBBH4s', 0x0001, 8, 0, family, port, socket.inet_aton(addr[0]))
                response += mapped_addr

                udp_socket.sendto(response, addr)
                print(f"已发送UDP响应给{addr}")

def handle_tcp(client_socket, addr):
    print(f"TCP连接已建立：{addr}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"收到来自{addr}的TCP数据")

        if len(data) >= 20:
            msg_type, msg_length, msg_magic, trans_id = struct.unpack('!HHI12s', data[:20])
            if msg_type == BINDING_REQUEST and msg_magic == MAGIC_COOKIE:
                response = struct.pack('!HHI12s', BINDING_RESPONSE, 8, msg_magic, trans_id)

                family = 0x01  # IPv4
                port = addr[1]
                ip_addr = struct.unpack("!I", socket.inet_aton(addr[0]))[0]

                mapped_addr = struct.pack('!HHBBH4s', 0x0001, 8, 0, family, port, socket.inet_aton(addr[0]))
                response += mapped_addr

                client_socket.sendall(response)
                print(f"已发送TCP响应给{addr}")

    client_socket.close()
    print(f"TCP连接已关闭：{addr}")

def start_tcp_server():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind(('0.0.0.0', PORT))
    tcp_socket.listen(5)
    print("STUN TCP服务器正在运行，监听端口5000")

    while True:
        client_socket, addr = tcp_socket.accept()
        threading.Thread(target=handle_tcp, args=(client_socket, addr)).start()

udp_thread = threading.Thread(target=handle_udp)
udp_thread.start()

start_tcp_server()
