'''
'''
#Ref: https://github.com/CabbageDevelopment/qasync/blob/master/examples/aiohttp_fetch.py
import asyncio
import functools
import sys
from prettyplot.qtWrapper import *
import qasync
from qasync import asyncClose 
from serial_worker import Worker
from rolling_data import RollingData
from prettyplot import PrettyPlot
from prettyplot.pplogger import get_logger
logger = get_logger( __name__) 


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Data streaming using asyncio')
        self.setStyleSheet('QToolBar{spacing:5px;};') #QStatusBar.item {border: none;}
        self.plotwidget1 = PrettyPlot()
        self.plotwidget1.grid(True)
        self.plotwidget1.linewidth = 1
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.plotwidget1)
        widget1 = QWidget()
        widget1.setLayout(vbox1)
        self.setCentralWidget(widget1)
        self.rolling_data = RollingData(self.plotwidget1)
        self.start_task()


    def start_task(self):
        '''
        Starts the asyncio loop
        '''
        loop = asyncio.get_event_loop()
        self.serial_worker = Worker(loop)
        self.serial_worker.packet_received.connect(self.rolling_data.append)
        self.serial_worker.work()
    
    @asyncClose
    async def closeEvent(self, event):
        logger.debug('Closing') #Cleanup connections
        self.serial_worker.stop_work()
        #Alternative
        # pending = asyncio.Task.all_tasks()
        # for task in pending:
        #     task.cancel()

async def main():
    def close_future(future, loop):
        loop.call_later(10, future.cancel)
        future.cancel()

    loop = asyncio.get_event_loop()
    future = asyncio.Future()

    app = QApplication.instance()
    if hasattr(app, 'aboutToQuit'):
        getattr(app, 'aboutToQuit')\
            .connect(functools.partial(close_future, future, loop))

    mainWindow = MainWindow()
    mainWindow.show()
    await future
    return True


if __name__ == "__main__":
    try:
        qasync.run(main())
    except asyncio.exceptions.CancelledError:
        sys.exit(0)
