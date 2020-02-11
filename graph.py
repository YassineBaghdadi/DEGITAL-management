
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


class Bar_graph:
    def __init__(self, data, year):
        print(data)
        print(year)
        labels = {'01' : 'jan', '02' : 'feb', '03' : 'mar', '04' : 'apr', '05' : 'may', '06' : 'jun', '07' : 'jul', '08' : 'aug', '09' : 'sep', '10' : 'oct', '11' : 'nov', '12' : 'dec'}

        money = {'01' : 0, '02' : 0, '03' : 0, '04' : 0, '05' : 0, '06' : 0, '07' : 0, '08' : 0, '09' : 0, '10' : 0, '11' : 0, '12' : 0}
        if year == 'For All ...':
            for p, d in data:
                money[str(d).split('-')[1]] += int(str(p).split('(')[0])
        else:
            for p, d in data:
                if str(d).split('-')[0] == str(year):
                    money[str(d).split('-')[1]] += int(str(p).split('(')[0])

        ym = []
        xm = []
        for i in money:
            if money[i] > 0 :
                ym.append(money[i])
                xm.append(labels[i])

        # print(money)
        # print(ym)
        # print(xm)

        # labels = []
        # dt = []
        # for i in self.months:
        #     if i == '01':
        #         labels.append('jan')
        #         dt.append(self.months[i])
        #
        # print(labels)



        x = np.arange(len(xm))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        # rects1 = ax.bar(x - width/2, men_means, width, label='Men')
        rects2 = ax.bar(x + width / 2, ym, width)
        # rects2 = ax.bar(x + width/2, women_means, width, label='Women')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Money')
        ax.set_xlabel('Months')
        ax.set_title(f'Total money of {year}')
        ax.set_xticks(x)
        ax.set_xticklabels(xm)
        ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        # autolabel(rects1)
        autolabel(rects2)

        fig.tight_layout()



        plt.show()


# dd = Bar_graph((('200()', '2020-02-08 16:15:43'),
#                 ('4444()', '2020-02-08 16:18:26'),
#                 ('4444()', '2020-02-08 16:18:26'),
#                 ('888(sadasd)', '2020-02-08 16:26:18'),
#                 ('9000()', '2020-02-08 16:28:43'),
#                 ('444444()', '2020-02-08 16:31:27'),
#                 ('99999999()', '2020-02-08 16:31:27'),
#                 ('0()', '2020-02-08 16:35:46'),
#                 ('3333()', '2020-02-08 16:44:05'),
#                 ('0()', '2020-02-08 16:51:10'),
#                 ('0()', '2020-02-08 16:52:51'),
#                 ('0()', '2020-02-08 16:54:12'),
#                 ('7777()', '2020-02-08 17:02:05'),
#                 ('444444444()', '2020-02-08 17:33:24'),
#                 ('0()', '2020-02-08 17:36:32'),
#                 ('0()', '2020-02-08 17:46:56'),
#                 ('0()', '2020-02-08 17:49:43'),
#                 ('0()', '2020-02-08 17:55:33'),
#                 ('0()', '2020-02-08 18:02:46'),
#                 ('0()', '2020-02-08 18:02:46'),
#                 ('0()', '2020-02-08 18:10:15'),
#                 ('0()', '2020-02-08 21:05:58'),
#                 ('0()', '2020-02-08 21:09:47'),
#                 ('0()', '2020-02-08 21:22:33'),
#                 ('0()', '2020-02-08 21:23:57'),
#                 ('0()', '2020-02-09 14:45:53'),
#                 ('0()', '2020-02-09 16:26:02'),
#                 ('0()', '2020-02-09 16:34:32'),
#                 ('0()', '2020-02-09 16:39:50'),
#                 ('0()', '2020-02-09 16:43:50'),
#                 ('0()', '2020-02-09 16:43:50'),
#                 ('0()', '2020-02-09 16:58:45'),
#                 ('0()', '2020-02-09 16:58:45')),
#                2020)
