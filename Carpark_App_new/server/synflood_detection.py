from scapy.all import *
import time
import numpy as np
import pickle
import collections

Traffic = collections.namedtuple("Traffic", ["pkt_count", "byte_count"])
ip_dict = {}
last_clear_time = time.time()
block_set = set()
TIME_INTERVAL = 240
THRESHOLD = 300000
latest_show_time = time.time()

if os.path.exists("blocked_ip.txt"):
    log_file = open('blocked_ip.txt', 'r')
    while True:
        line = log_file.readline()
        block_set.add(line.strip("\n"))
        if not line:
            break
self_ip = input("Please enter your ip address:")
log_file = open('blocked_ip.txt', 'a+')


def CallBack(packet):
    global ip_dict
    global block_set
    global latest_show_time
    global self_ip

    if "IP" not in packet:
        return

    src = packet["IP"].src
    if src == self_ip:
        return
    if src in block_set:
        print("The packet from " + src + " is blocked")
        return

    if src in ip_dict:
        pkt_count, byte_count = ip_dict[src]
        pkt_count += 1
        byte_count += len(packet)
        ip_dict[src] = Traffic(pkt_count, byte_count)
    else:
        ip_dict[src] = Traffic(1, len(packet))
    current_time = time.time()

    if current_time - latest_show_time >= 5:
        print(ip_dict)
        latest_show_time = current_time

    if ip_dict[src][0] >= THRESHOLD:
        block_set.add(src)
        print("A potential dos attack from " + src + " is detected")
        log_file.write(src + "\n")
        _, byte_count = ip_dict[src]
        ip_dict[src] = (-1e10, byte_count)


def clear_global_variables():
    global ip_dict
    global block_set
    ip_dict = {}
    block_set = set()


def ddos_detection():
    global ip_dict
    global block_set
    if not (os.path.exists("ddos_model.pickle") and os.path.exists("scaler.pickle")):
        print("No available pre-trained model")
        return
    else:
        clf = pickle.load(open('./ddos_model.pickle', 'rb'))
        scaler = pickle.load(open('./scaler.pickle', 'rb'))

        for key in ip_dict.keys():
            pkt_count, byte_count = ip_dict[key]
            # pktcount, bytecount, dur, ICMP, TCP, UDP
            input = np.array([[pkt_count, byte_count, TIME_INTERVAL, 0, 1, 0]])
            y_pred = clf.predict(scaler.transform(input))
            print(y_pred)
            print(key)
            if y_pred > 0.5:
                print("A potential ddos attack from " + key + " is detected")
                log_file.write(key + "\n")


if __name__ == "__main__":
    filter = "tcp"
    while True:
        sniff(filter=filter, prn=CallBack, iface='Software Loopback Interface 1', timeout=TIME_INTERVAL)
        ddos_detection()
        clear_global_variables()
