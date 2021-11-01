'''
'''
import numpy as np
from constants import MAX_DATA_POINTS
from kiwiplot.klog import get_logger
logger = get_logger( __name__) 



class RollingData():

    def __init__(self, fig):
        self.ch1_data = np.array([])
        # self.ch2_data = np.array([])
        self.fig = fig

        #Initialize the curves
        self.fig.plot([],[])
        # self.fig.plot([],[])

    #@Slot
    def append(self, adc1):
        '''
        Appends adc1 to self.ch1_data and adc2 to self.ch2_data
        Based on np.concatenate, it is 10x faster than using lists.
        '''
        self.ch1_data = np.concatenate((self.ch1_data, adc1))
        # self.ch2_data = np.concatenate((self.ch2_data, adc2))
        len1 = len(self.ch1_data)
        # len2 = len(self.ch2_data)
        if len1 > MAX_DATA_POINTS:
            self.ch1_data = self.ch1_data[(len1-MAX_DATA_POINTS):]
        # if len2 > MAX_DATA_POINTS:
        #     self.ch2_data = self.ch2_data[(len2-MAX_DATA_POINTS):]

        #Update plot
        x = np.arange(len(self.ch1_data))
        self.fig.update_curve(0, x, self.ch1_data)
        # self.fig.update_curve(1, x, self.ch2_data)