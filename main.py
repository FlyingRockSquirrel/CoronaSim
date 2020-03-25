import random
import networkx as nx
import matplotlib.pyplot as plt


# TODO: improve visualizer, potentially implement quarantine if time permits,
# do some sort of reinforcement learning to optimize quarantine.


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


def draw(gr, pos, labeler, colors):
    nx.draw(gr, nodelist=list(gr.nodes), pos=pos,
            labels=labeler, node_color=colors)
    plt.show()


# determines if a given instance will actually infect another by modelling a
# binomial distribution with expected value r_0
def willInfect(rate, totCon, totSize, recTime):
    avgCon = totCon/totSize
    totalInfectionChances = avgCon*recTime
    infProb = rate/totalInfectionChances
    randomSample = random.random()
    return randomSample <= infProb


def main():

    # Inputs for game initialization
    print("Please enter the R_0 value: ")
    r_0 = float(input())
    print("Please enter the death rate: ")
    deathRate = float(input())
    print("Please enter the total number of people: ")
    size = int(input())
    print("Please enter then total number of connections: ")
    totalConnections = int(input())
    print("Please enter the average recovery time for this disease: ")
    averageRecoveryTime = int(input())
    print("Please enter the number of initial patients: ")
    initialPatients = int(input())
    print("Do you want to visualize? (y/n) \n WARNING: This may cause program to run slowly")
    doprint = False
    response = input()
    if response == 'y':
        doprint = True

    # game state information initialization
    people = []
    labeler = {}
    numDead = 0
    ticks = 0
    numInfected = initialPatients
    infectedPeople = set()
    totInfections = initialPatients
    colorList = []

    # constructing nodes
    for i in range(0, size):
        if i < initialPatients:
            isInfected = True
            colorList.append('r')
        else:
            isInfected = False
            colorList.append('green')
        person = Person(deathRate, averageRecoveryTime, i, isInfected)
        people.append(person)
        if isInfected:
            infectedPeople.add(person)
            labeler[person] = str(i)
        else:
            labeler[person] = str(i)
    graph = nx.Graph()
    graph.add_nodes_from(people)
    pos = nx.spring_layout(graph)

    # constructing edges for graph
    # TODO: make this more efficient somehow. It takes forever for large graphs
    while len(set(graph.edges)) < totalConnections:
        n1 = random.randint(0, size - 1)
        n2 = random.randint(0, size - 1)
        p1 = people[n1]
        p2 = people[n2]
        while(p2 == p1):
            n2 = random.randint(0, size - 1)
            p2 = people[n2]
        graph.add_edge(p1, p2)

    if doprint:
        draw(graph, pos, labeler, colorList)

    while numInfected > 0:

        infectedToday = set()
        uninfectedToday = set()

        # Determining who is infected, who recovers, and who dies this iteration
        for patient in infectedPeople:
            for neighbor in graph.adj[patient]:
                if neighbor.alive and \
                   (not neighbor.immune) and (not neighbor.infected) and \
                        willInfect(r_0, totalConnections, size, averageRecoveryTime):
                    neighbor.infected = True
                    infectedToday.add(neighbor)

            if willRecoverToday(averageRecoveryTime):
                # Death logic
                if patient.willDie:
                    patient.alive = False
                    numDead += 1
                    colorList[patient.index] = 'black'
                else:
                    colorList[patient.index] = 'blue'
                numInfected -= 1
                uninfectedToday.add(patient)
                patient.immune = True
                patient.infected = False

        ticks += 1

        # Adding those infected to the infected set
        for infected in infectedToday:
            infectedPeople.add(infected)
            numInfected += 1
            totInfections += 1
            colorList[infected.index] = 'red'

        # Removing those no longer infected from the infected set
        for curedordead in uninfectedToday:
            infectedPeople.remove(curedordead)

        if doprint:
            draw(graph, pos, labeler, colorList)

    print("\n")
    print(str(numDead) + " people died")
    print(str(ticks) + " days since initial infection")
    print(str(totInfections) + " people were infected out of " +
          str(size) + " total people")

    return


main()
