import time
from time import struct_time

timeArray: struct_time = time.localtime(1579449603150 / 1000)
timeStr: str = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)

print(timeStr)