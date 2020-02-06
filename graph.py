
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from pylab import *

from pylab import *

class Graph:
    def __init__(self, title_, data_, labels, explode):
            # make a square figure and axes
            figure(1, figsize=(6, 6))
            # ax = axes([0.1, 0.1, 0.8, 0.8])

            # The slices will be ordered and plotted counter-clockwise.




            pie(data_, explode=explode, labels=labels,
                autopct='%1.1f%%', startangle=90)

            title(str(title_), bbox={'facecolor': '0.8', 'pad': 5})

            show()


