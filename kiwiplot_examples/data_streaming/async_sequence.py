#https://gist.github.com/designingSparks/76dc8fb245808562fd365a1600ab310f
import  asyncio

import time
rx_data = list()
EOT = 20

async def serial_sequence(tinterval):
    '''
    async generator function that simulates incoming sequence of serial data
    There is no time drift.
    '''
    num = 0
    starttime = time.time()
    while True:
        dt = (time.time() - starttime) % tinterval
        delay = tinterval - dt #Want to avoid time drift
        try:
            await asyncio.sleep(delay) #simulated IO delay
        except asyncio.CancelledError:
            print('cancelled')
            break
        num += 1
        yield num


async def read_serial1():
    gen = serial_sequence(0.5)
    while(True):
        data = await gen.__anext__()
        rx_data.append(data)
        print('read_serial1:', data)
        if data == EOT:
            break
    return rx_data

async def main():
    start = time.time()
    task1 = asyncio.create_task(read_serial1())
    await(task1)
    stop = time.time()
    print('Elapsed: {}'.format(stop-start))

if __name__ == '__main__':
    asyncio.run(main())