'''
Partly inspired by 
https://github.com/spyder-ide/qtpy/blob/master/qtpy/__init__.py
'''
import os
from .klog import *
logger = logging.getLogger('kiwiplot.' + __name__) 

api_list = ['PYSIDE2', 'PYQT5']


if 'QT_API' in os.environ:
    api = os.environ['QT_API'].upper()
    if api in api_list:
        if api == 'PYSIDE2':
            from PySide2.QtCore import *
            from PySide2.QtGui import *
            from PySide2.QtWidgets import *
            print('Qt backend set to PySide2.')
        elif api == 'PYQT5':
            from PyQt5.QtCore import *
            from PyQt5.QtGui import *
            from PyQt5.QtWidgets import *
            Signal = pyqtSignal
            Slot = pyqtSlot
            print('Qt backend set to PyQt5.')
        else:
            raise Exception("Invalid Qt API defined in os.environ['QT_API']. QT_API must be one of ['PYSIDE2', 'PYQT5'].")
else:
    print('Qt API not defined. Attempting to detect Qt backend automatically.')
    api = None
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        os.environ['QT_API'] = 'pyside2'
        logger.debug("Setting os.environ['QT_API'] to 'PYSIDE2'.")
    except ImportError as e:
        logger.debug('Could not import PySide2.')

    if 'QT_API' not in os.environ:
        try:
            from PyQt5.QtCore import *
            from PyQt5.QtGui import *
            from PyQt5.QtWidgets import *
            Signal = pyqtSignal
            Slot = pyqtSlot
            os.environ['QT_API'] = 'pyqt5'
            logger.debug("Setting os.environ['QT_API'] to 'PYQT5'.")
        except ImportError as e:
            logger.debug('Could not import PyQt5.')
            raise Exception('No default QT backends installed.')