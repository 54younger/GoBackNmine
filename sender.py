import time
import random
import socket
import select

packet_size = 2
lost_percent = 0
timeout = 10
window_size = 4
start_num =0
message = "hello!world1234567890"
packets = [message[i:i+packet_size]
               for i in range(0, len(message), packet_size)]

client_receiver_address = (socket.gethostbyname(socket.gethostname()), 8000)

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = socket.gethostbyname(socket.gethostname())
port = 8001
address = (ip, port)
receiver.bind(address)
receiver.setblocking(False)

timer = [0.0] * len(packets)

def send_window_packets():
    seq_num = 0 # 记录序列号
    seq = []
    global timer_window,  start_num
    for j in range(start_num, min(start_num + window_size, len(packets))):
        time.sleep(1)
        print(
            f"发送方为起始packet号码为{start_num}的窗口: 发送packet {j}, 序列号为 {seq_num}, 内容为'{packets[j]}'")

        # 记录发送时间
        timer[j] = time.time()

        if random.uniform(0,1) < lost_percent:
            print(f"发送方: packet {j} 丢失")

        else:
            send_pkt=j,packets[j]
            # 发送packets[j]和j
            receiver.sendto(str(send_pkt).encode(), client_receiver_address)

        seq_num += 1
    receive_ACK()


def receive_ACK():
    global timer_window, start_num
    final_ack = start_num+window_size

    while True:
        ready = select.select([receiver], [], [], 1000)
        if time.time() - timer[start_num] < timeout:
            if ready[0]:
                ack, addr = receiver.recvfrom(1024)
                ack=ord(ack.decode())
                if ack>start_num:
                    # 重置定时器至最后一个未收到 ACK 的 packet
                    for i in range(start_num, ack):
                        timer[i] = time.time()
                start_num = ack+1
                print(f"收到ACK {ack}, 窗口左边界为{start_num}")
                if ack == final_ack:#超时或一个窗口内全部发送完毕
                    #不是最后一个包，继续发送
                    if start_num <= len(packets):
                        send_window_packets()
                        break
                    else:
                        break
                else :
                    while time.time() - timer[start_num] < timeout:
                        pass
                    if start_num <= len(packets):
                        send_window_packets()
                        break
                    else:
                        break

        else :
          if start_num <= len(packets):
            print(f"超时, 重传packet {start_num}")
            send_window_packets()
          break



send_window_packets()
receive_ACK()
