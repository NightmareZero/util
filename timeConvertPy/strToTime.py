#! /usr/bin/python3
import sys
import time

# CONFIG
FORMAT: str = "%Y-%m-%d %H:%M:%S"

inputArgs: list = sys.argv

if __name__ == '__main__':
    # 处理时间日期
    itTime: time.struct_time = time.strptime(inputArgs[1], FORMAT)
    # 转换为float
    pyTime: float = time.mktime(itTime)
    print("time is ",int(pyTime*1000))
