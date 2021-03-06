from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random
import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt
from deap import base
from deap import creator
from deap import tools


class MainStrategy(bt.Strategy):
    params = (
        ('datafeed', 'quandl'),
        ('printlog', False),
        ('detail', 4),
        ('chromosome', []),
        ('maUpperbounds', 4),
        ('maLowerbounds', 4),
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])


if __name__ == '__main__':

    cerebro = bt.Cerebro()
    cerebro.addstrategy(MainStrategy)

    if MainStrategy.params.datafeed=='quandl':
        data = bt.feeds.Quandl(
        dataname='AAPL',
        buffered=True
    )
    cerebro.adddata(data)
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())