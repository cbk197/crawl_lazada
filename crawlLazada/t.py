import random 
import time 
start = time.time() 
end = 0 
while (True):
    start = time.time()
    random.seed(time.time()+70)
    a = random.randint(1,6)
    b = random.randint(1,6)
    c = random.randint(1,6)
    print(a+b+c)
    time.sleep(70 - time.time() + start)
