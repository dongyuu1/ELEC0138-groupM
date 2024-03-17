from scapy.all import *
import time

ip_dict = {}
last_clear_time = time.time()
block_set = set()
TIME_INTERVAL = 30
THRESHOLD = 50

if os.path.exists("blocked_ip.txt"):
    log_file = open('blocked_ip.txt', 'r')
    while True:
        line = log_file.readline()
        block_set.add(line.strip("\n"))
        if not line:
            break

log_file = open('blocked_ip.txt', 'a+')


def CallBack(packet):
    global ip_dict
    global last_clear_time
    global block_set

    if packet["IP"] is None:
        return

    current_time = time.time()

    if current_time - last_clear_time > TIME_INTERVAL:
        ip_dict = {}
        last_clear_time = current_time

    src = packet["IP"].src

    if src in block_set:
        print("The packet from " + src + " is blocked")
        return

    if src in ip_dict:
        ip_dict[src] += 1
    else:
        ip_dict[src] = 1

    if ip_dict[src] >= THRESHOLD:
        block_set.add(src)
        print("A potential dos attack from " + src + " is detected")
        log_file.write(src + "\n")
        ip_dict[src] = -1e10



if __name__ == "__main__":
    filter = "tcp or udp or icmp"
    sniff(filter=filter, prn=CallBack, iface='WLAN', count=0)
