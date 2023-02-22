import asyncio
import time
import datetime

import aioserial
import aiofiles
import numpy as np

buffer_size = 120

async def main():
    serial = aioserial.AioSerial(port='COM3', baudrate=9600)
    buffer = np.zeros(buffer_size, dtype=int)
    data_pointer = 0
    async with aiofiles.open(f'P_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.bin', 'wb') as f:
        while True:
            data = await serial.readline_async()
            val = int(data.decode().strip())
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
                await f.write(buffer.tobytes())
                buffer = np.zeros(buffer_size, dtype=int)
                await f.flush()
                data_pointer = 0

loop = asyncio.get_event_loop()
loop.create_task(main())
loop.run_forever()