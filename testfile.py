
import time

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(int(current_time[:2]))
