#!/usr/bin/python
import threading
import time

var = 5

def trabaja():
    global var
    for i in range(5):
        var = var * 4
        print("Y ahora la variable vale ", var)
        time.sleep(0.2)

print("La variable en un principio es ", var)
threading.Thread(target=trabaja).start()

for i in range(5):
    print("Y ahora la variable vale ", var)
    time.sleep(0.2)

