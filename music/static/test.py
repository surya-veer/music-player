import socket
import threading
from queue import Queue
import time

print_lock = threading.Lock()
q = Queue()

server = 'pythonprogramming.net'


def pscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        con = s.connect((server, port))
        with print_lock:
            print("Port " + str(port) + " is open")
        con.close()
    except:


def threader():
    while True:
        worker = q.get()
        pscan(worker)
        q.task_done()


for x in range(50):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

start_time = time.time()

for work in range(1, 100):
    q.put(work)

q.join()

print('Task complete in:' + str(time.time() - start_time))

