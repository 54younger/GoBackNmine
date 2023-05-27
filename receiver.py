import time
import random
import socket
import select

packet_size = 2
lost_percent = 0.2
timeout = 10
window_size = 4
ack_num =0

client_sender_address = (socket.gethostbyname(socket.gethostname()), 8001)
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.gethostbyname(socket.gethostname())
port = 8000
address = (ip, port)
sender.bind(address)
sender.setblocking(False)

def receive_window_packets():
    global ack_num
    # 等待套接字准备就绪
    while True:
        ready = select.select([sender], [], [], 60)
        if ready[0]:
            data, addr = sender.recvfrom(1024)
            seq_num, message = eval(data.decode())
            #返回ACK
            print(f"接收方: 收到packet {seq_num}, 内容为'{message} ,发送ACK {seq_num}'")
            if random.uniform(0,1) < lost_percent:
                print(f"packet {seq_num}的ACK丢失")
            else:
                sender.sendto(chr(seq_num).encode(), client_sender_address)
            if seq_num==ack_num:#从未丢包
                ack_num+=1
            else:#丢包
                pass

receive_window_packets()
