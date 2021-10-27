'''
Configuration of the logger for the kiwiplot module.
Example:
from pplogger import *
logger = logging.getLogger('kiwiplot.' + __name__) 
#logger.setLevel(logger.WARNING) #can customize the logger level for each file individually
'''

import logging
console = logging.StreamHandler()
# console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)d    %(name)-12s:%(lineno)-4d %(message)s', '%H:%M:%S') #includes ms
# formatter = logging.Formatter('%(name)-12s:%(lineno)-4d %(message)s') 
# formatter = logging.Formatter('%(asctime)s.%(msecs)d    %(name)-12s %(levelname)-8s %(message)s', '%H:%M:%S') #includes ms
# formatter = logging.Formatter('%(name)-20s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
root_logger = logging.getLogger('kiwiplot') #set to '' if you want to display logs of other modules
root_logger.addHandler(console) 
root_logger.setLevel(logging.DEBUG) #Uncomment to enable logging. Default level is WARNING

def get_logger(name):
    return logging.getLogger('kiwiplot.' + name)