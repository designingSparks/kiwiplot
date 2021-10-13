from qt import *
import asyncio
import time
import numpy as np
from itertools import cycle
from prettyplot.pplogger import get_logger
logger = get_logger( __name__) 

x = np.arange(0, 2*np.pi, 2*np.pi/100)
x1 = np.split(x, 10) #list of 20 arrays
iter_x = cycle(x1)

class Worker(QObject):
    packet_received = Signal(object)

    def __init__(self, loop: asyncio.AbstractEventLoop, parent=None):
        super(Worker, self).__init__(parent)
        self.loop = loop
        self.serial_simulator = SerialSimulator()

    def work(self):
        self.task = asyncio.ensure_future(self.read_bytes(), loop=self.loop)
        # asyncio.ensure_future(self.work_test(), loop=self.loop)

    async def work_test(self):
        # task = asyncio.create_task(serial_interface.read_packet_test())
        logger.debug('Emitting packet')
        # result = await(task)
        result = '1234567890'
        self.packet_received.emit(result)

    def stop_work(self):
        print('Stopping work')
        self.task.cancel()

    async def read_bytes(self):
        gen = self.serial_simulator.read_packet(0.1)
        while(True):
            try:
                packet = await gen.__anext__()
            except StopAsyncIteration: 
                #The StopAsyncIteration error is thrown when the task is cancelled in self.stop_work()
                logger.debug('Stopping iteration')
                break
            self.packet_received.emit(packet)

            # print('New bytes recieved:', packet)
            # print('Number of bytes: {}'.format(len(packet)))


class SerialSimulator():
    def __init__(self):
        logger.debug('Initializing')
    
    def function1(self, x):
        return np.sin(x)

    async def read_packet(self, tinterval):
        '''
        async generator function that simulates incoming sequence of serial data
        There is no time drift.
        '''
        # num = 0
        starttime = time.time()
        while True:

            dt = (time.time() - starttime) % tinterval
            delay = tinterval - dt #Want to avoid time drift
            # num += 1
            x = next(iter_x)
            y = self.function1(x)
            yield y

            try:
                await asyncio.sleep(delay) #simulated IO delay
            except asyncio.CancelledError: #Raise when the task is cancelled
                print('Cancelled detected')
                break