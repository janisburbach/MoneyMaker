from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import backtrader as bt

import random
from deap import base, creator
from deap import tools
import multiprocessing


IND_SIZE = 20

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("bit", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.bit, n=IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    return runstrat(individual),

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=10)
toolbox.register("evaluate", evaluate)


class MainStrategy(bt.Strategy):
    params = (
        ('printlog', False),
        ('detail', 4),
        ('chromosome', []),
        ('maUpperbounds', 4),
        ('maLowerbounds', 4)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
#        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        pass
#        self.log('Close, %.2f' % self.dataclose[0])

def runstrat(chromosome):

# TODO: chromosome needs to be parsed to different upper and lower bounds and paramter values
    
    
    params = (
        ('datafeed', 'quandl')
    )
    cerebro = bt.Cerebro()
    cerebro.addstrategy(MainStrategy)

#    if params.datafeed == 'quandl':
    data = bt.feeds.Quandl(
        dataname='AAPL',
        buffered=True
    )

    cerebro.adddata(data)
    cerebro.broker.setcash(10000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    
    return (cerebro.broker.getvalue())

if __name__ == '__main__':

    
    
    CXPB, MUTPB, NGEN, NPOP = 0.5, 0.2, 20, 10
    
    # wir erstellen eine Population von Individuals der Größe NPOP
    pop = toolbox.population(n=NPOP)
    
    # create multiprocessing pool
    pool = multiprocessing.Pool()
    
    # Evaluate the entire population
    fitnesses = pool.imap(toolbox.evaluate, pop)
    
    
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
    
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        
        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        
        # The population is entirely replaced by the offspring
        pop[:] = offspring