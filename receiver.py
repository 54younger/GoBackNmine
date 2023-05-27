import time
import random
import socket
import select

packet_size = 2
lost_percent = 0
timeout = 10
window_size = 4
start_num =0

client_sender_address = (socket.gethostbyname(socket.gethostname()), 8001)
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.gethostbyname(socket.gethostname())
port = 8000
address = (ip, port)
sender.bind(address)
sender.setblocking(False)

def receive_window_packets():
    global start_num
    # 等待套接字准备就绪
    ready = select.select([sender], [], [], timeout)
    while True:
        if ready[0]:
            data, addr = sender.recvfrom(1024)
            seq_num, message = eval(data.decode())
            #如果丢包
            if random.random() < lost_percent:
                print(f"接收方: packet {seq_num} 丢失")
            else:
                #返回ACK
                if seq_num==start_num:
                  start_num +=1

                print(f"接收方: 收到packet {seq_num}, 内容为'{message} ,发送ACK {start_num-1}'")
                sender.sendto(chr(start_num-1).encode(), client_sender_address)


receive_window_packets()
