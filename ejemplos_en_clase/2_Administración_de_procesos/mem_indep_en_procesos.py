#!/usr/bin/python
import os
import time

var = 5

print("La variable en un principio es ", var)
pid = os.fork()
for i in range(5):
    if pid == 0:
        var = var * 4
    
    print("Y ahora la variable vale ", var)
    time.sleep(0.2)
