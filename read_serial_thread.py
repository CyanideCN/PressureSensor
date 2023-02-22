import time
import datetime
import threading
import queue
import sys
import struct

import serial

com = serial.Serial("COM3", 9600, timeout=5)

# 数据格式
# 气压(Pa) int4
# 时间(s) int4
# 时间(ms) int4

data_queue = queue.Queue()
stop_event = threading.Event()

f = open(f'P_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.bin', 'wb')

def read_data():
    time.sleep(1)
    while not stop_event.is_set():
        inp = com.readline().decode().strip()
        if not inp:
            continue
        timestamp = time.time()
        val = int(inp)
        if val not in range(90000, 105000):
            continue
        print(f'\r{val}', end='', flush=True)
        data = (val, int(timestamp), int(timestamp % 1 * 1000))
        data_queue.put(data)

def write_data():
    data_pointer = 0
    while not stop_event.is_set():
        data = data_queue.get()
        f.write(struct.pack('iii', *data))
        data_pointer += 1
        if data_pointer == 20:
            f.flush()
            data_pointer = 0

def start_reading_thread():
    thread = threading.Thread(target=read_data)
    thread.start()
    return thread

def start_writing_thread():
    thread = threading.Thread(target=write_data)
    thread.start()
    return thread

if __name__ == '__main__':
    t1 = start_reading_thread()
    t2 = start_writing_thread()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        stop_event.set()
        sys.exit(0)