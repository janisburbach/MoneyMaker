
# coding: utf-8

# In[2]:


#Beschreibung des Optimierungsproblems http://tracer.lcc.uma.es/problems/onemax/onemax.html

import random
from deap import algorithms, base, creator, tools

# Definition der Fitnessfunktion
def evalOneMax(individual):
    #print (individual)
    #print (sum(individual))
    return (sum(individual),)
# erster Parameter  = name der neuen Klasse, der zweite die Oberklasse
#Bei weight wird das optimierungsziel festgelegt 1.0 = nur ein Ziel, dass maximiert wird
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
#diese Klasse kapselt die Individuals, sie erbt von python standard Liste
creator.create("Individual", list, fitness= creator.FitnessMax)
toolbox = base.Toolbox()
# wird für für die bitfunktion 
toolbox.register("bit", random.randint, 0, 1)
# n ist hier die Länge des bitvectors
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.bit, n=200)
# n legt fest, wie viele individuen es am Anfang gibt, die Anzahl wird dann immer kleiner
toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=100)
# der toolbox wird die Evaluationsfunktion übergeben
toolbox.register("evaluate", evalOneMax)
# two point crossover wird eingestellt
toolbox.register("mate", tools.cxTwoPoint)
# Bit Flip mit einer Wahrscheinlichkeit von 5%
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# tournament selection aus 3 migliedern --> ka was das ist
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("map", map)
CXPB, MUTPB, NGEN = 0.5, 0.2, 100
pop = toolbox.population()
pop = algorithms.eaSimple(pop, toolbox, CXPB, MUTPB, NGEN)

