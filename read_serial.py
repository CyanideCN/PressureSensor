import time
import datetime

import serial
import numpy as np

com = serial.Serial("COM3", 9600, timeout=5)
buffer_size = 120
buffer = np.zeros(buffer_size, dtype=int)
data_pointer = 0


f = open(f'P_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.bin', 'wb')
# 数据格式
# 气压(Pa) int4
# 时间(s) int4
# 时间(ms) int4

while True:
    inp = com.readline().decode().strip()
    if not inp:
        continue
    val = int(inp)
    print(f'\r{val}', end='', flush=True)
    timestamp = time.time()
    if data_pointer < buffer_size - 2:
        buffer[data_pointer] = val
        data_pointer += 1
        buffer[data_pointer] = int(timestamp)
        data_pointer += 1
        buffer[data_pointer] = int(timestamp % 1 * 1000)
        data_pointer += 1
    else:
        f.write(buffer.tobytes())
        buffer = np.zeros(buffer_size, dtype=int)
        f.flush()
        data_pointer = 0
