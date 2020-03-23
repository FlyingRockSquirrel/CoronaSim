import random
import networkx as nx


# TODO: take input for these parameters instead of hardcoding them, work on visualizer, potentially implement quarantine if time permits.
r_0 = 2.4
deathRate = 4
size = 10000
totalConnections = 10000
averageRecoveryTime = 10
initialPatients = 2000


# Will be node in the graph. Contains data specific to each person
class Person:
    def __init__(self, deathRate, recoveryTime, index, infected):

        self.index = index
        self.infected = infected
        self.immune = False
        self.alive = True
        self.recoveryTime = recoveryTime

        deathInt = random.uniform(0, 100)
        if deathInt <= deathRate:
            self.willDie = True
        else:
            self.willDie = False


def willRecoverToday(averageRecTime):
    return random.randint(1, averageRecTime) == 1


# determines if a given instance will actually infect another by modelling a
# binomial distribution with expected value r_0
def willInfect(rate, totCon, totSize, recTime):
    avgCon = totCon/totSize
    totalInfectionChances = avgCon*recTime
    infProb = rate/totalInfectionChances
    randomSample = random.random()
    return randomSample <= infProb


def __main__():
    people = []
    numDead = 0
    ticks = 0
    numInfected = initialPatients
    infectedPeople = set()

    # constructing nodes
    for i in range(0, size):
        isInfected = False
        if i < initialPatients:
            isInfected = True
        person = Person(deathRate, averageRecoveryTime, i, isInfected)
        people.append(person)
        if isInfected:
            infectedPeople.add(person)
    graph = nx.Graph()
    graph.add_nodes_from(people)

    # constructing edges for graph
    while len(set(graph.edges)) < totalConnections:
        n1 = random.randint(0, size - 1)
        n2 = random.randint(0, size - 1)
        p1 = people[n1]
        p2 = people[n2]
        while(p2 == p1):
            n2 = random.randint(0, size - 1)
            p2 = people[n2]
        graph.add_edge(p1, p2)

    while numInfected > 0:

        infectedToday = set()
        uninfectedToday = set()

        # Determining who is infected, who recovers, and who dies this iteration
        for patient in infectedPeople:
            for neighbor in graph.adj[patient]:
                if neighbor.alive and (not neighbor.immune) and (not neighbor.infected) and willInfect(r_0, totalConnections, size, averageRecoveryTime):
                    neighbor.infected = True
                    infectedToday.add(neighbor)

            if willRecoverToday(averageRecoveryTime):
                # Death logic
                if patient.willDie:
                    patient.alive = False
                    numDead += 1
                numInfected -= 1
                uninfectedToday.add(patient)
                patient.immune = True
                patient.infected = False

        ticks += 1

        # Adding those infected to the infected set
        for infected in infectedToday:
            infectedPeople.add(infected)
            numInfected += 1

        # Removing those no longer infected from the infected set
        for curedordead in uninfectedToday:
            infectedPeople.remove(curedordead)

    print(numDead)
    print(ticks)
    return


__main__()
