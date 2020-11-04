from threading import Semaphore, Thread  
from time import sleep                  
import random                           

barrier = 4  
mutex_canoa= Semaphore(1)  
hackers = 0   
serfs = 0   
hackerQueue = Semaphore(0)    
serfQueue = Semaphore(0)   
global hackers,serfs

def hacker(number):                    
        mutex_canoa.acquire()           
        hackers += 1                    
        print("El hacker ya está en la canoa"%number)   
        if hackers == 4:                        
                for i in range (barrier):       
                        hackerQueue.release()   
                        hackers=0                
                        print("canoa en movimiento")    
        elif serfs >= 2 and hackers == 2:       
                for i in range (2):             
                        hackerQueue.release()  
                        SerfQueue.release()     
                        serfs-=2                
                        hackers=0              
                        print("canoa en movimiento")   
		mutex_canoa.release()                
        hackerQueue.acquiere()                 
                        

def serf(number):                             
        mutex_canoa.acquire()            
        print("El serfs ya está en la canoa"%number) 
		serfs += 1 		
        if serfs == 4:                        
                for i in range (barrier):                  
                        SerfQueue.release()           
                        serfs=0                       
                        print("canoa en movimiento")    
        elif hackers >= 2 and serfs == 2:              
                for i in range (2):                     
                        hackerQueue.release()           
                        hackers-=2                     
                        serfs=0                         
                        print("canoa en movimiento")   
        mutex_canoa.release()                           
        SerfQueue.acquiere()                            
        

for i in range (10):                                     
        Thread (target=hacker, args =[i]).start()
for i in range (10):                                     
        Thread (target=serf, args =[i]).start()              
