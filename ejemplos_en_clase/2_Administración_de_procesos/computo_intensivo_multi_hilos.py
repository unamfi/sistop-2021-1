#!/usr/bin/python
import threading
import time

def trabaja(id):
    i = 0
    while True:
        i = i + 1
        if i > 10000000:
            print(id)
            i = 0

for i in range(8):
    threading.Thread(target=trabaja, args=[i]).start()

time.sleep(100)

