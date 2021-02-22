from typing import List, Tuple
from numpy.random import binomial
import random

#defining the base infectivity of a model virus - some float indicating the chance of spread per interaction



#define the type aliases

#Population follows a list indexed a person's id of person objects
Population = List['Person']

#link ties two nodes together along an edge through their id
Link = Tuple[int,int]



#the overall model - consisting of the nodemap and the virus

class Model(object):
    def __init__(self, virus : float):
        self.virus : float = virus

        





        
#defining geography - nodes and edges

class Node(object):
    def __init__(self, area_id: int, population: Population, interactivity: float):
        self.area_id : int = area_id

        #total population stored as a dictionary
        self.population: TotalPopulation = population

        #sets of infected, healthy people and recovered people (identified using personID) - on init all healthy
        #sets used as lookup and removal important
        self.infected: set[int] = set() 
        self.healthy: set[int] = set(list(range(0,len(population))))
        self.recovered : set[int] = set()

        #maybe include a queue of sets to track infection times - 14 long, FIFO - adds to recovered after 14 days automaticallyw

        #values dictating the current and base interactivity within a node
        #interactivity - the average number of people a person interacts with in a spreadable way
        #this is used as a measure of spreadability in conjunction with infection rate
        self.baseInteractivity: float = interactivity
        self.currentInteractivity: float = interactivity


    #changes the interactivity utilizing some scaling factor
    def change_interactivity(self, change : float):
        self.currentInteractivity = self.currentInteractivity * change


    #infects a set of people decided through both interactivity and infectivity
    #follows a binomial distribution with p = infectivity and n = total interactivity
    #interactivity is multiplied by the number of infected and some scaling factor (not every infected interacts with a unique set)
    def infect(self, virus : float):
        #scaling factor proportional to the number infected (more likely all with few infected)
        totalInteractivity = self.currentInteractivity * len(self.infected)
        if totalInteractivity > len(self.healthy):
            totalInteractivity = len(self.healthy)

        #the number of infected is sampled from the binomial distribution
        numInfected = binomial(totalInteractivity, virus) #biggest source of slowdown - maybe lose for high numbers?


        #randomly infects the number of people from the healthy population
        newInfected = set(random.sample(self.healthy, int(numInfected)))
        self.healthy = self.healthy - newInfected
        self.infected.update(newInfected)


    #starts the epidemic with some random patient zero
    def start(self):
        patient0 = random.choice(list(self.healthy))
        self.healthy.remove(patient0)
        self.infected.update({patient0})
        
        
        

class Edge(object):
    def __init__(self, edge_id: int, link: Link ,crossover: int, interactivity: float):
        self.edge_id : int = edge_id
        self.link : Link = link 

        #spreadiblity along an edge dictated by - the interactivity on the edge and the number of "people" on the edge

        #crossover - the number of people going to and from two nodes
        #doesn't represent actual movement of people - abstract representation of movement between nodes
        self.crossover = crossover
        

        #interactivity - the average number of people a person interacts with in a spreadable way
        self.baseInteractivity: float = interactivity
        self.currentInteractivity: float = interactivity



#implementation of a person - fairly barebones as more complexty is not needed for aggregate model
class Person(object):
    def __init__(self, person_id: int):
        self.person_id : int = person_id
        self.infected : bool = False

        #time infected needed - to uninfect people after a time
        self.infectionTick : int = None

        #recovery logged - for immunity - should be unnecessary with sets
        self.recovered : bool = False

        #contact - person_id of contact which transmitted virus - needed for contact tracing
        self.contact = None

    #infects a person - changes to infected and logs the infectionTick
    def infect(self, currentTime : int, contact : int):
        self.infected = True
        self.infectionTick = currentTime
        self.contact = int

    #recovered utilized to change a person to recovered - unneeded with set implementation    
    def recover(self):
        self.infected = False
        self.recovered = True



population = []
for i in range(0,7000000):
    population.append(Person(i))


node = Node(1,population,5)
tick = 0
node.start()

while(len(node.healthy) > 0):
    print(str(tick) + ": " + str(len(node.infected)))
    tick += 1
    node.infect(0.02)

print(str(tick) + ": " + str(len(node.infected)))
    
        
