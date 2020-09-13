import argparse
import socket

from colorama import init, Fore
from threading import Thread, Lock
from queue import Queue

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

N_THREADS = 200                         #Number of threads, you can change this as you wish
q = Queue()                             #threads queue
print_lock = Lock()

def port_scan(port):                       #scan port on the global variable
    try:
        s = socket.socket()
        s.connect((targetIP, port))
    except:
        with print_lock:
             print(f"{GRAY}{targetIP:15}:{port:5} is closed  {RESET}", end="\r")

    else:
        with print_lock:
            print(f"{GREEN}{targetIP:15}:{port:5} is open  {RESET}")

    finally:
        s.close()

def scan_thread():                          #Get port numb from the queue and scan it
    global q
    while True:
        worker = q.get()                       #scan ports from queue
        port_scan(worker)
        q.task_done()

def main(targetIP, ports):
    global q
    for t in range(N_THREADS):                      #start threads
        t = Thread(target=scan_thread)
        t.deamon = True                         #this will end when the main thread end
        t.start()                               #start deamon threads

    for worker in ports:                        #for each port, put that port into the queue
            q.put(worker)
                                                #wait the threads (port scanners ) to finish
    q.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simple port scanner")  #passed targetIP and port as a argument
    parser.add_argument("targetIP", help="targetIP to scan.")
    parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="Port range to scan, default is 1-65535 (all ports)")
    args = parser.parse_args()
    targetIP, port_range = args.targetIP, args.port_range

    startPort, endPort = port_range.split("-")                    #split startPort and endPort
    startPort, endPort = int(startPort), int(endPort)

    ports = [ p for p in range(startPort, endPort)]

    main(targetIP, ports)
