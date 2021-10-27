# coding: utf-8
'''

'''
import sys
from . qtWrapper import *
from . eng_notation import eng
from numpy import double
from .pplogger import *
logger = logging.getLogger('kiwiplot.' + __name__) 


class DataTable(QTableWidget):
    '''
    Creates a widget for displaying the results
    '''
    def __init__(self, rows, cols, parent=None):
        super(DataTable, self).__init__(len(rows), len(cols), parent=parent)
        self.setHorizontalHeaderLabels(cols)
        self.setVerticalHeaderLabels(rows)
#         self.horizontalHeader().setResizeMode(3, QHeaderView.Stretch )
        self.setAlternatingRowColors(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        
    def display_data(self, data):
        '''
        Populate the table. Called when the calculate button is pressed.
        '''
        #self.setRowCount(0)
        self.clearContents()
        self.setRowCount(len(data))

        for n in range(len(data)):  #len returns the number of rows
            self.setItem(n, 0, MyTableWidgetItem(eng(data[n][0])))
            self.setItem(n, 1, MyTableWidgetItem(eng(data[n][1])))
            self.setItem(n, 2, MyTableWidgetItem(eng(data[n][2])))
            accuracy = '%.3g' % data[n][3]
            self.setItem(n, 3, MyTableWidgetItem(accuracy))


        self.setSortingEnabled(True)
        self.sortItems(ACC_COL) #Apply a sort to the last column
                                                #There seems to be a bug in the table if you don't do this.
        
        # self.highlight_lowest_acc()

    @Slot(object, str)
    def update_data(self, data, name):
        xdata, ydata = data

        for row, x, y in zip(range(self.rowCount()), xdata, ydata):
            self.setItem(row, 0, MyTableWidgetItem(eng(x)))
            self.setItem(row, 1, MyTableWidgetItem(eng(y)))


    # def highlight_lowest_acc(self):
    #     lowest = 0
    #     best_acc = 1e6

    #     for n in range(self.rowCount()):
    #         acc = float(self.item(n, ACC_COL).text())
    #         if abs(acc) < abs(best_acc):
    #             lowest = n
    #             best_acc = acc
    #         else:
    #             break
    #     self.selectRow(lowest)
    #     self.setFocus() #Otherwise the row doesnt turn blue




class MyTableWidgetItem(QTableWidgetItem):

    def __lt__(self, other):
        '''Overrides the less than operator. Otherwise text sorting is used.
        '''
        return double(self.text()) < double(other.text())


